import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_repo_text(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class MiniarchPromptContractTests(unittest.TestCase):
    def test_runtime_surfaces_drop_small_and_faster_positioning(self) -> None:
        skill_text = read_repo_text("skills/miniarch-step/SKILL.md").lower()
        agent_text = read_repo_text("skills/miniarch-step/agents/openai.yaml").lower()
        auto_plan_text = read_repo_text("skills/miniarch-step/references/arch-auto-plan.md").lower()
        implement_loop_text = read_repo_text("skills/miniarch-step/references/arch-implement-loop.md").lower()

        banned_phrases = [
            "faster standalone full-arch workflow",
            "faster full-arch workflow",
            "smaller well-defined",
            "small enough and well-defined enough",
            "faster core arc",
            "mini core arc",
            "faster planning arc",
        ]
        for phrase in banned_phrases:
            self.assertNotIn(phrase, skill_text)
            self.assertNotIn(phrase, agent_text)
            self.assertNotIn(phrase, auto_plan_text)
            self.assertNotIn(phrase, implement_loop_text)

        self.assertIn("trimmed public command surface", skill_text)
        self.assertIn("not a lower-effort workflow", skill_text)
        self.assertIn("trimmed full-arch workflow", agent_text)
        self.assertIn("not a lower-effort workflow", agent_text)

    def test_public_docs_mirror_trimmed_surface_language(self) -> None:
        readme_text = read_repo_text("README.md").lower()
        guide_text = read_repo_text("docs/arch_skill_usage_guide.md").lower()

        banned_phrases = [
            "faster full-arch middle tier",
            "smaller well-defined features",
            "small and well-defined enough",
            "small and crisp enough",
            "do the faster full arch flow",
            "smaller well-defined full-arch work",
            "faster full-arch tier",
        ]
        for phrase in banned_phrases:
            self.assertNotIn(phrase, readme_text)
            self.assertNotIn(phrase, guide_text)

        self.assertIn("trimmed full-arch surface", readme_text)
        self.assertIn("trimmed command surface", readme_text)
        self.assertIn("trimmed command surface", guide_text)


if __name__ == "__main__":
    unittest.main()
