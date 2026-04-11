import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPSERT_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/upsert_codex_stop_hook.py"
STOP_HOOK_PATH = REPO_ROOT / "skills/arch-step/scripts/arch_controller_stop_hook.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CodexStopHookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.upsert_module = load_module(UPSERT_HOOK_PATH, "arch_skill_upsert_codex_stop_hook")

    def test_install_hook_preserves_unrelated_and_collapses_repo_managed_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            hooks_file = temp_root / "hooks.json"
            skills_dir = temp_root / "installed-skills"
            hooks_file.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/third-party-hook.py",
                                            "timeoutSec": 30,
                                            "statusMessage": "third-party hook",
                                        }
                                    ]
                                },
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/implement_loop_stop_hook.py",
                                            "timeoutSec": 1200,
                                            "statusMessage": (
                                                "arch-step automatic controller is running; planning continuations "
                                                "are quick, fresh implement-loop audits can take a few minutes"
                                            ),
                                        }
                                    ]
                                },
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/audit_loop_stop_hook.py",
                                            "timeoutSec": 1200,
                                            "statusMessage": (
                                                "audit-loop automatic controller is running; fresh review passes "
                                                "can take a few minutes"
                                            ),
                                        }
                                    ]
                                },
                            ]
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            self.upsert_module.install_hook(hooks_file, skills_dir)
            written = json.loads(hooks_file.read_text(encoding="utf-8"))
            stop_groups = written["hooks"]["Stop"]

            self.assertEqual(len(stop_groups), 2)
            self.assertEqual(
                stop_groups[0]["hooks"][0]["command"],
                "python3 /tmp/third-party-hook.py",
            )

            managed_groups = self.upsert_module.repo_managed_groups(stop_groups)
            self.assertEqual(len(managed_groups), 1)
            self.assertEqual(
                managed_groups[0],
                self.upsert_module.expected_group(self.upsert_module.expected_command(skills_dir)),
            )

            self.upsert_module.verify_hook(hooks_file, skills_dir)

    def test_verify_hook_fails_when_multiple_repo_managed_entries_remain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            hooks_file = temp_root / "hooks.json"
            skills_dir = temp_root / "installed-skills"
            expected_group = self.upsert_module.expected_group(
                self.upsert_module.expected_command(skills_dir)
            )
            hooks_file.write_text(
                json.dumps(
                    {
                        "hooks": {
                            "Stop": [
                                expected_group,
                                {
                                    "hooks": [
                                        {
                                            "type": "command",
                                            "command": "python3 /tmp/audit_loop_stop_hook.py",
                                            "timeoutSec": 1200,
                                            "statusMessage": (
                                                "audit-loop automatic controller is running; fresh review passes "
                                                "can take a few minutes"
                                            ),
                                        }
                                    ]
                                },
                            ]
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(SystemExit) as raised:
                self.upsert_module.verify_hook(hooks_file, skills_dir)
            self.assertIn("expected exactly one arch_skill-managed Stop hook entry", str(raised.exception))

    def test_stop_hook_blocks_when_multiple_controller_states_are_armed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            state_dir = repo_root / ".codex"
            state_dir.mkdir()
            (state_dir / "implement-loop-state.json").write_text(
                json.dumps({"command": "implement-loop", "doc_path": "docs/PLAN.md"}, indent=2) + "\n",
                encoding="utf-8",
            )
            (state_dir / "audit-loop-state.json").write_text(
                json.dumps({"command": "auto", "ledger_path": "_audit_ledger.md"}, indent=2) + "\n",
                encoding="utf-8",
            )

            process = subprocess.run(
                [sys.executable, str(STOP_HOOK_PATH)],
                input=json.dumps({"cwd": str(repo_root), "session_id": "session-1"}),
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(process.returncode, 0, msg=process.stderr)
            payload = json.loads(process.stdout)
            self.assertFalse(payload["continue"])
            self.assertIn(".codex/implement-loop-state.json", payload["stopReason"])
            self.assertIn(".codex/audit-loop-state.json", payload["stopReason"])


if __name__ == "__main__":
    unittest.main()
