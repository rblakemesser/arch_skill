import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_POLICY = REPO_ROOT / "skills/_shared/agent-orchestration-policy.md"


def run_make(target: str, home: Path, overrides: dict[str, Path]):
    env = os.environ.copy()
    env["HOME"] = str(home)
    args = ["make", target]
    args.extend(f"{name}={path}" for name, path in overrides.items())
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )


class SharedPolicyInstallTests(unittest.TestCase):
    def test_verify_rejects_stale_policy_for_primary_runtime_roots(self) -> None:
        cases = [
            ("agents_install_skill", "verify_agents_install", "AGENTS_SKILLS_DIR"),
            ("claude_install_skill", "verify_claude_install", "CLAUDE_SKILLS_DIR"),
            ("gemini_install_skill", "verify_gemini_install", "GEMINI_SKILLS_DIR"),
        ]

        for install_target, verify_target, destination_var in cases:
            with (
                self.subTest(destination=destination_var),
                tempfile.TemporaryDirectory() as tmpdir,
            ):
                home = Path(tmpdir)
                overrides = {
                    "AGENTS_SKILLS_DIR": home / ".agents/skills",
                    "CODEX_SKILLS_DIR": home / ".codex/skills",
                    "CODEX_HOOKS_FILE": home / ".codex/hooks.json",
                    "CLAUDE_SKILLS_DIR": home / ".claude/skills",
                    "CLAUDE_SETTINGS_FILE": home / ".claude/settings.json",
                    "GEMINI_SKILLS_DIR": home / ".gemini/skills",
                }

                install = run_make(install_target, home, overrides)
                self.assertEqual(install.returncode, 0, install.stderr)

                policy = (
                    overrides[destination_var]
                    / "_shared/agent-orchestration-policy.md"
                )
                self.assertEqual(policy.read_bytes(), SOURCE_POLICY.read_bytes())

                policy.write_text("stale policy\n", encoding="utf-8")
                verify = run_make(verify_target, home, overrides)

                self.assertNotEqual(verify.returncode, 0)
                self.assertIn(f"ERROR: missing or stale {policy}", verify.stdout)


if __name__ == "__main__":
    unittest.main()
