"""Offline fixtures for the local-history fallback; never read real history."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import sqlite3
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location("ai_sessions", Path(__file__).with_name("ai_sessions.py"))
history = importlib.util.module_from_spec(spec)
spec.loader.exec_module(history)


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.codex = root / "codex"
        self.claude = root / "claude"
        for key, value in {"CODEX": str(self.codex), "CLAUDE_ROOT": str(self.claude),
                           "CLAUDE_GLOB": str(self.claude / "*" / "*.jsonl")}.items():
            item = patch.object(history, key, value)
            item.start()
            self.addCleanup(item.stop)

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", ["ai_sessions", *args]), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            history.main()
        return out.getvalue(), err.getvalue()

    def test_entrypoint_without_sigpipe_support(self):
        signals = SimpleNamespace(signal=Mock(), SIG_DFL=0)
        out = io.StringIO()
        with patch.dict(sys.modules, {"signal": signals}), \
                patch.object(sys, "argv", ["ai_sessions.py", "--help"]), \
                contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as result:
            runpy.run_path(str(Path(__file__).with_name("ai_sessions.py")), run_name="__main__")
        self.assertEqual(result.exception.code, 0)
        self.assertIn("usage:", out.getvalue())
        signals.signal.assert_not_called()

    def test_missing_sources_report_gaps(self):
        out, err = self.run_cli("list", "--since", "2026-01-01", "--until", "2026-01-02")
        self.assertEqual(out, "")
        self.assertIn("Claude local history unavailable", err)
        self.assertIn("Codex local history unavailable", err)

    def test_codex_messages_preserve_xml_and_full_text(self):
        self.codex.mkdir()
        path = self.codex / "rollout.jsonl"
        message = "<request>Review AGENTS.md</request> " + "x" * 1600
        record = {"type": "response_item", "timestamp": "2026-01-01T12:00:00Z", "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": message}]}}
        path.write_text(json.dumps(record) + "\n")
        out, _ = self.run_cli("show", str(path), "--max-chars", "0", "--source", "codex")
        self.assertIn(message, out)

    def test_codex_schema_and_archive_filter_are_read_only(self):
        self.codex.mkdir()
        db = self.codex / "state_5.sqlite"
        with sqlite3.connect(db) as con:
            con.execute("create table threads (id,title,cwd,created_at,updated_at,archived,rollout_path,first_user_message,git_branch,source)")
            for archived in (0, 1):
                con.execute("insert into threads values (?,?,?,?,?,?,?,?,?,?)", (str(archived), "Example", "/example/app", 1767268800, 1767268800, archived, "unused", "request", "main", "cli"))
        before = db.read_bytes()
        self.assertEqual(len(list(history.codex_sessions(False))), 1)
        self.assertEqual(len(list(history.codex_sessions(True))), 2)
        self.assertEqual(db.read_bytes(), before)

    def test_unsupported_schema_is_not_empty_success(self):
        self.codex.mkdir()
        sqlite3.connect(self.codex / "state_5.sqlite").close()
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(list(history.codex_sessions(False)), [])
        self.assertIn("schema is unsupported", err.getvalue())

    def test_claude_and_ambiguous_prefix(self):
        project = self.claude / "example"
        project.mkdir(parents=True)
        record = {"type": "user", "timestamp": "2026-01-01T12:00:00Z", "cwd": "/example", "message": {"content": "Review the example"}}
        for suffix in ("one", "two"):
            (project / f"session-{suffix}.jsonl").write_text(json.dumps(record) + "\n")
        self.assertEqual(len(list(history.claude_sessions())), 2)
        with self.assertRaises(SystemExit):
            self.run_cli("show", "session-")

    def test_out_of_order_claude_records_match_both_days(self):
        project = self.claude / "example"
        project.mkdir(parents=True)
        path = project / "midnight-session.jsonl"
        records = [
            {"type": "user", "timestamp": "2026-01-02T00:00:01Z",
             "message": {"content": "Review the example"}},
            {"type": "assistant", "timestamp": "2026-01-01T23:59:59Z",
             "message": {"content": "Earlier response"}},
        ]
        path.write_text("".join(json.dumps(record) + "\n" for record in records))
        before = path.read_bytes()
        for date, expected in (("2026-01-01", 1), ("2026-01-02", 1),
                               ("2025-12-31", 0), ("2026-01-03", 0)):
            with self.subTest(date=date):
                out, err = self.run_cli("list", "--source", "claude",
                                        "--since", date, "--until", date)
                self.assertEqual(out.count("midnight-session"), expected)
                self.assertIn(f"claude={expected}", err)
        self.assertEqual(path.read_bytes(), before)

    def test_wal_without_shm_is_refused_without_source_writes(self):
        self.codex.mkdir()
        live = Path(self.tmp.name) / "live.sqlite"
        writer = sqlite3.connect(live)
        self.addCleanup(writer.close)
        writer.execute("pragma journal_mode=WAL")
        writer.execute("create table threads (id,title,cwd,created_at,updated_at,archived,rollout_path,first_user_message,git_branch,source)")
        writer.execute("insert into threads values (?,?,?,?,?,?,?,?,?,?)", ("wal-only", "Recent correction", "/example", 1767268800, 1767268800, 0, "unused", "Rejected", "main", "cli"))
        writer.commit()
        self.assertEqual(writer.execute("select count(*) from threads").fetchone()[0], 1)
        db = self.codex / "state_5.sqlite"
        db.write_bytes(live.read_bytes())
        Path(str(db) + "-wal").write_bytes(Path(str(live) + "-wal").read_bytes())
        before = {p.name: p.read_bytes() for p in self.codex.iterdir()}
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(list(history.codex_sessions(False)), [])
        self.assertIn("WAL-mode", err.getvalue())
        with self.assertRaises(ValueError):
            history.codex_path("example")
        self.assertEqual({p.name: p.read_bytes() for p in self.codex.iterdir()}, before)
        self.assertFalse(Path(str(db) + "-shm").exists())

    def test_wal_header_without_sidecars_is_also_refused(self):
        self.codex.mkdir()
        db = self.codex / "state_5.sqlite"
        con = sqlite3.connect(db)
        con.execute("pragma journal_mode=WAL")
        con.execute("create table example (value)")
        con.commit()
        con.close()
        before = {p.name: p.read_bytes() for p in self.codex.iterdir()}
        with self.assertRaises(ValueError):
            history.query_codex("select * from example")
        self.assertEqual({p.name: p.read_bytes() for p in self.codex.iterdir()}, before)

    def test_missing_transcript_reports_partial_deep_search(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            found = history.deep_hit({"source": "codex", "path": str(self.codex / "missing.jsonl")}, "rejected")
        self.assertFalse(found)
        self.assertIn("transcript is missing", err.getvalue())
        self.assertIn("partial", err.getvalue())

    def test_malformed_records_and_wrapped_correction_remain_visible(self):
        self.codex.mkdir()
        path = self.codex / "example.jsonl"
        message = "<user_instructions>I reject this result. Do not publish.</user_instructions>"
        record = {"type": "response_item", "timestamp": "2026-01-01T12:00:00Z", "payload": {
            "type": "message", "role": "user", "content": [{"type": "input_text", "text": message}]}}
        path.write_text(json.dumps(record) + "\n{broken\n")
        out, err = self.run_cli("show", str(path), "--max-chars", "0", "--source", "codex")
        self.assertIn(message, out)
        self.assertIn("malformed transcript record at line 2", err)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertTrue(history.deep_hit({"source": "codex", "path": str(path)}, "reject"))
        self.assertIn("partial", err.getvalue())

    def test_claude_malformed_record_is_not_silent(self):
        project = self.claude / "example"
        project.mkdir(parents=True)
        path = project / "session.jsonl"
        path.write_text('{broken\n' + json.dumps({"type": "user", "timestamp": "2026-01-01T12:00:00Z", "message": {"content": "<user_instructions>Rejected</user_instructions>"}}) + "\n")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            sessions = list(history.claude_sessions())
            turns = list(history.claude_turns(path))
        self.assertEqual(len(sessions), 1)
        self.assertIn("Rejected", turns[0][2])
        self.assertIn("malformed transcript record", err.getvalue())


if __name__ == "__main__":
    unittest.main()
