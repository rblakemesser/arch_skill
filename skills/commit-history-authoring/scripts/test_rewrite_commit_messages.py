from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("rewrite_commit_messages.py")


class RewriteCommitMessagesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.origin = self.root / "origin.git"
        self.work = self.root / "work"
        self.git_raw(["init", "--bare", str(self.origin)], cwd=self.root)
        self.git_raw(["clone", str(self.origin), str(self.work)], cwd=self.root)
        self.git(["config", "user.name", "Test User"])
        self.git(["config", "user.email", "test@example.com"])
        self.git(["checkout", "-b", "main"])
        self.commit_file("README.md", "root\n", "initial commit")
        self.git(["push", "-u", "origin", "main"])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def git_raw(
        self,
        args: list[str],
        *,
        cwd: Path | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            ["git", *args],
            cwd=cwd or self.work,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if check and proc.returncode != 0:
            self.fail(
                f"git {' '.join(args)} failed\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
            )
        return proc

    def git(self, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.git_raw(args, cwd=self.work, check=check)

    def git_stdout(self, args: list[str]) -> str:
        return self.git(args).stdout.strip()

    def commit_file(self, relative_path: str, content: str, message: str) -> str:
        path = self.work / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        self.git(["add", relative_path])
        self.git(["commit", "-m", message])
        return self.git_stdout(["rev-parse", "HEAD"])

    def checkout_feature_from_main(self, branch: str = "feature") -> None:
        self.git(["checkout", "-b", branch, "origin/main"])

    def inspect(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "inspect", "--repo", str(self.work), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if check and proc.returncode != 0:
            self.fail(f"inspect failed\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        return proc

    def inspect_json(self, *args: str) -> dict[str, object]:
        proc = self.inspect(*args)
        return json.loads(proc.stdout)

    def apply_rewrite(self, messages_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "apply",
                "--repo",
                str(self.work),
                "--messages-dir",
                str(messages_dir),
                *args,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            self.fail(f"apply failed\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
        return proc

    def test_auto_parent_allows_pushed_current_branch_commits(self) -> None:
        self.checkout_feature_from_main()
        self.commit_file("feature.txt", "feature\n", "WIP feature")
        self.git(["push", "-u", "origin", "feature"])

        state = self.inspect_json()

        self.assertEqual(state["range_mode"], "auto_parent")
        self.assertEqual(state["parent_ref"], "origin/main")
        self.assertEqual(state["commit_count"], 1)
        self.assertEqual(state["allowed_current_branch_remote_refs"], ["origin/feature"])

    def test_apply_rewrites_pushed_current_branch_message(self) -> None:
        self.checkout_feature_from_main()
        old_head = self.commit_file("feature.txt", "feature\n", "WIP feature")
        old_tree = self.git_stdout(["rev-parse", f"{old_head}^{{tree}}"])
        self.git(["push", "-u", "origin", "feature"])
        state = self.inspect_json()

        messages_dir = self.root / "messages"
        messages_dir.mkdir()
        for commit in state["commits"]:
            sha = commit["sha"]
            (messages_dir / f"{sha}.msg").write_text(
                "Explain feature commit\n\nPreserve the patch while clarifying the story.\n",
                encoding="utf-8",
            )

        result = json.loads(self.apply_rewrite(messages_dir).stdout)
        new_head = result["new_head"]

        self.assertTrue(result["tree_equivalent"])
        self.assertNotEqual(old_head, new_head)
        self.assertEqual(self.git_stdout(["log", "-1", "--format=%s"]), "Explain feature commit")
        self.assertEqual(self.git_stdout(["rev-parse", f"{new_head}^{{tree}}"]), old_tree)

    def test_nearest_parent_branch_beats_main(self) -> None:
        self.git(["checkout", "-b", "topic-base", "origin/main"])
        self.commit_file("topic.txt", "topic\n", "Add topic base")
        self.git(["push", "-u", "origin", "topic-base"])
        self.git(["checkout", "-b", "child"])
        self.commit_file("child.txt", "child\n", "WIP child")
        self.git(["push", "-u", "origin", "child"])

        state = self.inspect_json()

        self.assertEqual(state["parent_ref"], "origin/topic-base")
        self.assertEqual(state["commit_count"], 1)
        self.assertEqual(state["allowed_current_branch_remote_refs"], ["origin/child"])

    def test_unrelated_remote_ref_blocks_rewrite(self) -> None:
        self.checkout_feature_from_main()
        self.commit_file("feature.txt", "feature\n", "WIP feature")
        self.git(["push", "-u", "origin", "feature"])
        self.git(["push", "origin", "HEAD:other"])

        proc = self.inspect(check=False)

        self.assertEqual(proc.returncode, 2)
        self.assertIn("shared remote ref origin/other", proc.stderr)

    def test_current_branch_remote_ahead_blocks_rewrite(self) -> None:
        self.checkout_feature_from_main()
        self.commit_file("feature.txt", "feature\n", "WIP feature")
        self.git(["push", "-u", "origin", "feature"])
        self.commit_file("feature.txt", "feature\nremote\n", "Remote-only follow-up")
        self.git(["push"])
        self.git(["reset", "--hard", "HEAD~1"])

        proc = self.inspect(check=False)

        self.assertEqual(proc.returncode, 2)
        self.assertIn("current branch remote origin/feature is ahead", proc.stderr)

    def test_parent_override_uses_requested_parent(self) -> None:
        self.checkout_feature_from_main()
        self.commit_file("feature.txt", "feature\n", "WIP feature")
        self.git(["push", "-u", "origin", "feature"])

        state = self.inspect_json("--parent", "origin/main")

        self.assertEqual(state["range_mode"], "explicit_parent")
        self.assertEqual(state["parent_ref"], "origin/main")
        self.assertEqual(state["commit_count"], 1)

    def test_base_override_uses_exact_boundary(self) -> None:
        self.checkout_feature_from_main()
        self.commit_file("feature.txt", "feature\n", "WIP feature")
        self.git(["push", "-u", "origin", "feature"])

        state = self.inspect_json("--base", "origin/main")

        self.assertEqual(state["range_mode"], "explicit_base")
        self.assertIsNone(state["parent_ref"])
        self.assertEqual(state["base_ref"], "origin/main")
        self.assertEqual(state["commit_count"], 1)

    def test_merge_commit_in_range_is_blocked(self) -> None:
        self.checkout_feature_from_main()
        self.commit_file("feature.txt", "feature\n", "Feature step")
        self.git(["checkout", "-b", "side", "origin/main"])
        self.commit_file("side.txt", "side\n", "Side step")
        self.git(["checkout", "feature"])
        self.git(["merge", "--no-ff", "side", "-m", "Merge side"])

        proc = self.inspect(check=False)

        self.assertEqual(proc.returncode, 2)
        self.assertIn("target range contains merge commit", proc.stderr)

    def test_protected_branch_is_blocked_by_default(self) -> None:
        proc = self.inspect(check=False)

        self.assertEqual(proc.returncode, 2)
        self.assertIn("current branch 'main' is protected", proc.stderr)


if __name__ == "__main__":
    unittest.main()
