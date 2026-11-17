"""Exercise installation in temporary directories, never the real user profile."""

import contextlib
import io
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from install import install


class InstallTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "download with spaces"
        self.profile = self.root / "user"
        for name in ("custom", "dependency"):
            skill = self.repo / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Example skill\n")
        references = self.repo / "skills/custom/references"
        references.mkdir()
        (references / "guide.md").write_text("Use ../../dependency/SKILL.md\n")
        output = contextlib.redirect_stdout(io.StringIO())
        output.__enter__()
        self.addCleanup(output.__exit__, None, None, None)

    def link(self, target, source):
        try:
            target.symlink_to(source, target_is_directory=source.is_dir())
        except (OSError, NotImplementedError):
            self.skipTest("This platform does not permit symlink fixtures")

    def test_copies_survive_download_move_and_removal(self):
        with patch.object(Path, "symlink_to", side_effect=AssertionError("No links allowed")):
            install(self.repo, self.profile)
            install(self.repo, self.profile)
        moved = self.root / "renamed download"
        self.repo.rename(moved)
        shutil.rmtree(moved)
        target = self.profile / ".agents/skills"
        for name in ("custom", "dependency"):
            self.assertFalse((target / name).is_symlink())
            self.assertEqual((target / name / "SKILL.md").read_text(), "Example skill\n")
        reference = target / "custom/references/guide.md"
        self.assertEqual(reference.read_text(), "Use ../../dependency/SKILL.md\n")
        self.assertTrue((reference.parent / "../../dependency/SKILL.md").is_file())
        self.assertFalse((self.profile / ".claude").exists())
        self.assertFalse((self.profile / ".cursor").exists())

    def test_source_changes_do_not_change_installed_copy(self):
        install(self.repo, self.profile)
        (self.repo / "skills/custom/SKILL.md").write_text("New release\n")
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile)
        self.assertEqual((self.profile / ".agents/skills/custom/SKILL.md").read_text(), "Example skill\n")

    def test_explicit_hosts_select_only_their_roots(self):
        for host, expected in (
            ("codex", {".agents"}), ("claude", {".claude"}),
            ("cursor", {".agents"}), ("all", {".agents", ".claude"}),
        ):
            with self.subTest(host=host):
                profile = self.root / host
                install(self.repo, profile, host=host)
                install(self.repo, profile, host=host)
                self.assertEqual({path.name for path in profile.iterdir()}, expected)
                for product in expected:
                    folders = list((profile / product / "skills").iterdir())
                    self.assertEqual({path.name for path in folders}, {"custom", "dependency"})
                    self.assertTrue(all(path.is_dir() and not path.is_symlink() for path in folders))

    def test_cursor_reuses_codex_copies(self):
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

    def test_existing_different_directory_prevents_all_writes(self):
        existing = self.profile / ".claude/skills/custom"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("Local edits\n")
        for dry_run in (False, True):
            with self.assertRaises(FileExistsError):
                install(self.repo, self.profile, host="all", dry_run=dry_run)
        self.assertEqual((existing / "SKILL.md").read_text(), "Local edits\n")
        self.assertFalse((self.profile / ".agents").exists())

    def test_local_added_resource_prevents_new_skill_installation(self):
        install(self.repo, self.profile)
        extra = self.profile / ".agents/skills/custom/local.md"
        extra.write_text("Preserve my notes\n")
        new = self.repo / "skills/new"
        new.mkdir()
        (new / "SKILL.md").write_text("New skill\n")
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile)
        self.assertEqual(extra.read_text(), "Preserve my notes\n")
        self.assertFalse((self.profile / ".agents/skills/new").exists())

    def test_legacy_and_dangling_links_are_preserved(self):
        for name, source in (("legacy", self.repo / "skills/custom"), ("dangling", self.root / "missing")):
            with self.subTest(kind=name):
                profile = self.root / name
                target = profile / ".agents/skills/custom"
                target.parent.mkdir(parents=True)
                self.link(target, source)
                with self.assertRaises(FileExistsError):
                    install(self.repo, profile)
                self.assertEqual(target.readlink(), source)
                self.assertFalse((target.parent / "dependency").exists())

    def test_parent_file_prevents_all_writes(self):
        self.profile.mkdir()
        (self.profile / ".claude").write_text("Keep me\n")
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile, host="all")
        self.assertFalse((self.profile / ".agents").exists())

    def test_linked_parent_is_not_followed(self):
        self.profile.mkdir()
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        self.link(self.profile / ".agents", elsewhere)
        with self.assertRaises(FileExistsError):
            install(self.repo, self.profile)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_generated_and_private_files_are_excluded_on_copy_and_comparison(self):
        source = self.repo / "skills/custom"
        for filename in ("__pycache__/module.pyc", ".env", ".env.local", ".DS_Store", "._guide.md",
                         "Thumbs.db", "references/project-memory.json", "skill-inventory.json", "work-journal.md"):
            path = source / filename
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Never distribute\n")
        install(self.repo, self.profile)
        target = self.profile / ".agents/skills/custom"
        self.assertEqual({str(path.relative_to(target)) for path in target.rglob("*") if path.is_file()},
                         {"SKILL.md", "references/guide.md"})
        private = target / "references/project-memory.json"
        private.write_text("Private installed state\n")
        install(self.repo, self.profile)
        self.assertEqual(private.read_text(), "Private installed state\n")

    def test_source_resource_link_is_rejected_before_writes(self):
        self.link(self.repo / "skills/dependency/linked.md", self.repo / "skills/custom/SKILL.md")
        with self.assertRaises(ValueError):
            install(self.repo, self.profile)
        self.assertFalse(self.profile.exists())

    def test_source_skill_link_is_rejected_before_writes(self):
        self.link(self.repo / "skills/linked", self.repo / "skills/custom")
        with self.assertRaises(ValueError):
            install(self.repo, self.profile)
        self.assertFalse(self.profile.exists())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "Requires a FIFO fixture")
    def test_source_special_file_is_rejected_before_writes(self):
        os.mkfifo(self.repo / "skills/dependency/pipe")
        with self.assertRaises(ValueError):
            install(self.repo, self.profile)
        self.assertFalse(self.profile.exists())

    def test_source_read_failure_prevents_all_writes(self):
        read_bytes = Path.read_bytes
        def fail(path):
            if path == self.repo / "skills/dependency/SKILL.md":
                raise PermissionError("fixture source unavailable")
            return read_bytes(path)
        with patch.object(Path, "read_bytes", fail), self.assertRaises(PermissionError):
            install(self.repo, self.profile)
        self.assertFalse(self.profile.exists())

    def test_copy_failure_preserves_partial_folder_without_entrypoint(self):
        original_open = Path.open
        blocked = self.profile.resolve() / ".agents/skills/custom/references/guide.md"
        def fail(path, *args, **kwargs):
            if path == blocked:
                raise PermissionError("fixture destination unavailable")
            return original_open(path, *args, **kwargs)
        with patch.object(Path, "open", fail), self.assertRaisesRegex(OSError, "partial folder may remain"):
            install(self.repo, self.profile)
        self.assertFalse((self.profile / ".agents/skills/custom/SKILL.md").exists())
        self.assertFalse((self.profile / ".agents/skills/dependency").exists())
        self.assertTrue((self.repo / "skills/custom/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
