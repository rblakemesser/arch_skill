import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "plan-swarm"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def make_var_words(makefile: str, variable: str) -> list[str]:
    match = re.search(rf"^{variable} := (.*)$", makefile, re.MULTILINE)
    assert match is not None, variable
    return match.group(1).split()


class PlanSwarmSkillTests(unittest.TestCase):
    def test_skill_package_shape_is_present(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").is_file())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").is_file())
        self.assertFalse((SKILL_DIR / "scripts").exists())

        for relpath in [
            "references/workflow-contract.md",
            "references/phase-contract.md",
            "references/decomposition-and-scheduling.md",
            "references/worker-prompt-contract.md",
            "references/arbiter-and-review.md",
            "references/resource-leases.md",
            "references/session-reuse.md",
            "references/run-state-and-artifacts.md",
            "references/examples.md",
        ]:
            self.assertTrue((SKILL_DIR / relpath).is_file(), relpath)

    def test_description_is_valid_and_names_boundaries(self):
        body = read(SKILL_DIR / "SKILL.md")
        description = re.search(r'^description: "(.*)"$', body, re.MULTILINE)

        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)
        self.assertIn("The plan doc remains source of truth", body)
        self.assertIn("Cursor Agent implementation defaults to `composer-2.5-fast`", body)
        self.assertIn("Thermonuclear maintainability review is required", body)
        self.assertIn("Never claim completion from worker self-certification alone", body)
        self.assertIn("`$agent-delegate`", body)

    def test_contract_is_prompt_first(self):
        workflow = read(SKILL_DIR / "references" / "workflow-contract.md")
        state = read(SKILL_DIR / "references" / "run-state-and-artifacts.md")

        self.assertIn("Parent Agent Owns Orchestration", workflow)
        self.assertIn("Parallelism is part of the parent agent's normal work", workflow)
        self.assertIn("swarm-ledger.md", state)
        self.assertNotIn("spawn-wave", state)
        self.assertNotIn(".arch_skill/plan-swarm/", state)

    def test_progress_tables_are_required(self):
        body = read(SKILL_DIR / "SKILL.md")
        state = read(SKILL_DIR / "references" / "run-state-and-artifacts.md")
        scheduling = read(SKILL_DIR / "references" / "decomposition-and-scheduling.md")
        examples = read(SKILL_DIR / "references" / "examples.md")

        for text in [body, state, examples]:
            self.assertIn("Phase Progress", text)
            self.assertIn("Current Phase Work Slices", text)
            self.assertIn("Workers Now", text)

        for column in ["Phase", "Scope", "%", "Evidence", "Note"]:
            self.assertIn(column, body)
        for column in ["Slice", "Goal", "Worker", "Parallelization", "Proof"]:
            self.assertIn(column, state)
        for column in ["Runtime/Model", "Current Task", "Session"]:
            self.assertIn(column, state)

        self.assertIn("periodic Markdown table updates", body)
        self.assertIn("Progress Snapshot", state)
        self.assertIn("parallelization strategy", scheduling)

    def test_docs_and_install_surfaces_include_plan_swarm(self):
        readme = read(REPO_ROOT / "README.md")
        usage = read(REPO_ROOT / "docs" / "arch_skill_usage_guide.md")
        agents = read(REPO_ROOT / "AGENTS.md")
        makefile = read(REPO_ROOT / "Makefile")
        gitignore = read(REPO_ROOT / ".gitignore")

        for doc in [readme, usage]:
            self.assertIn("`plan-swarm`", doc)
            self.assertIn("~/.agents/skills/plan-swarm/", doc)
            self.assertIn("prompt-first", doc)
            self.assertNotIn("plan-swarm` is script-backed", doc)

        self.assertIn("Use `$plan-swarm`", agents)
        self.assertNotIn(".arch_skill/plan-swarm/", gitignore)

        for variable in ["SKILLS", "CLAUDE_SKILLS", "GEMINI_SKILLS"]:
            self.assertIn("plan-swarm", make_var_words(makefile, variable))


if __name__ == "__main__":
    unittest.main()
