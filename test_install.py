"""Exercise installation in temporary directories, never the real user profile."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from install import install


class InstallTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "repo with spaces"
        self.profile = self.root / "user"
        for name in ("custom", "dependency"):
            skill = self.repo / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Example skill\n")
        output = contextlib.redirect_stdout(io.StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)

    def test_links_are_global_repeatable_and_include_dependencies(self):
        install(self.repo, self.profile)
        install(self.repo, self.profile)
        for name in ("custom", "dependency"):
            target = self.profile / ".agents/skills" / name
            self.assertTrue(target.is_symlink())
            self.assertEqual(target.resolve(), (self.repo / "skills" / name).resolve())
        self.assertFalse((self.profile / ".claude").exists())
        self.assertFalse((self.profile / ".cursor").exists())
        self.assertFalse((self.repo / ".agents").exists())
        (self.repo / "skills/custom/SKILL.md").write_text("Updated\n")
        self.assertEqual((self.profile / ".agents/skills/custom/SKILL.md").read_text(), "Updated\n")

    def test_explicit_hosts_select_only_their_roots(self):
        for host, expected in (
            ("codex", {".agents"}),
            ("claude", {".claude"}),
            ("cursor", {".agents"}),
            ("all", {".agents", ".claude"}),
        ):
            with self.subTest(host=host):
                profile = self.root / host
                install(self.repo, profile, host=host)
                install(self.repo, profile, host=host)
                self.assertEqual({path.name for path in profile.iterdir()}, expected)
                for product in expected:
                    links = list((profile / product / "skills").iterdir())
                    self.assertEqual({path.name for path in links}, {"custom", "dependency"})
                    for link in links:
                        self.assertTrue(link.is_symlink())
                        self.assertEqual(link.resolve(), (self.repo / "skills" / link.name).resolve())

    def test_cursor_reuses_codex_links(self):
        install(self.repo, self.profile)
        install(self.repo, self.profile, host="cursor")
        self.assertEqual({path.name for path in self.profile.iterdir()}, {".agents"})

    def test_unselected_host_is_untouched(self):
        self.profile.mkdir()
        (self.profile / ".claude").write_text("Keep me\n")
        install(self.repo, self.profile)
        self.assertEqual((self.profile / ".claude").read_text(), "Keep me\n")

    def test_unknown_host_writes_nothing(self):
        with self.assertRaises(ValueError):
            install(self.repo, self.profile, host="unknown")
        self.assertFalse(self.profile.exists())

    def test_dry_run_writes_nothing(self):
        for host in ("codex", "claude", "cursor", "all"):
            install(self.repo, self.profile, host=host, dry_run=True)
        self.assertFalse(self.profile.exists())

    def test_existing_directory_prevents_all_writes(self):
        existing = self.profile / ".claude/skills/custom"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("Local edits\n")
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile, host="all")
        self.assertEqual((existing / "SKILL.md").read_text(), "Local edits\n")
        self.assertFalse((self.profile / ".agents").exists())

    def test_dangling_link_is_preserved(self):
        target = self.profile / ".agents/skills/custom"
        target.parent.mkdir(parents=True)
        target.symlink_to(self.root / "missing")
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile)
        self.assertEqual(target.readlink(), self.root / "missing")
        self.assertFalse((self.profile / ".claude").exists())

    def test_parent_file_prevents_all_writes(self):
        self.profile.mkdir()
        (self.profile / ".claude").write_text("Keep me\n")
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile, host="all")
        self.assertFalse((self.profile / ".agents").exists())


if __name__ == "__main__":
    unittest.main()
