import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ARCH_EPIC = REPO_ROOT / "skills" / "arch-epic"


def read(relpath: str) -> str:
    return (ARCH_EPIC / relpath).read_text(encoding="utf-8")


def squash(text: str) -> str:
    return " ".join(text.split())


class ArchEpicScopeLockTests(unittest.TestCase):
    def test_epic_verdict_schema_has_no_scope_reduction_values(self):
        schema_path = ARCH_EPIC / "references" / "epic-verdict-schema.json"
        schema_text = schema_path.read_text(encoding="utf-8")
        schema = json.loads(schema_text)
        item_schema = schema["properties"]["discovered_items"]["items"]

        self.assertIn("scope_relationship", item_schema["required"])
        self.assertNotIn("must_have_or_nice", item_schema["required"])
        self.assertEqual(
            item_schema["properties"]["scope_relationship"]["enum"],
            ["required_for_approved_scope"],
        )
        self.assertEqual(
            item_schema["properties"]["recommendation"]["enum"],
            ["extend_current", "new_sub_plan"],
        )
        self.assertNotIn("nice_to_have", schema_text)
        self.assertNotIn('"defer"', schema_text)
        self.assertNotIn('"drop"', schema_text)

    def test_scope_change_discipline_teaches_locked_scope(self):
        text = read("references/scope-change-discipline.md")
        compact = squash(text)

        for phrase in [
            "the epic scope is the epic scope",
            "Automatic mode must not cut, narrow, park, drop, or move approved scope",
            "There is no `defer` recommendation",
            "There is no `drop` recommendation",
            "no `nice_to_have` classification",
            "Automatic mode never auto-applies a scope disposition",
            "extend the current sub-plan",
            "insert a new sub-plan",
        ]:
            self.assertIn(phrase, compact)

    def test_auto_harness_prompts_forbid_out_of_scope_classification(self):
        text = read("references/auto-harness-prompts.md")
        compact = squash(text)

        for phrase in [
            "treat approved epic scope as locked",
            "The epic scope is the epic scope",
            "owned here, already satisfied, or assigned",
            "Do not solve the gap by calling it out of scope",
            "Missing approved work is a blocker, not a scope decision",
            "do not invent any defer/drop/out-of-scope compromise",
        ]:
            self.assertIn(phrase, compact)
        self.assertNotIn("out of scope with a reason", compact)
        self.assertNotIn("must-have or nice-to-have", compact)
        self.assertNotIn("defer, or drop", compact)

    def test_critic_prompt_rejects_decision_log_only_scope_reduction(self):
        text = read("references/critic-prompt.md")
        compact = squash(text)

        for phrase in [
            "Agent-written Decision Log notes do not authorize scope reduction",
            "A missing, skipped, parked, or narrowed item is a fail",
            "scope_relationship: required_for_approved_scope",
            "Do not report nice-to-have observations as scope changes",
        ]:
            self.assertIn(phrase, compact)
        self.assertNotIn("must_have_or_nice", compact)
        self.assertNotIn("explicitly deferred", compact)
        self.assertNotIn("recommendation`: - defer", compact)

    def test_workflow_and_examples_no_longer_auto_defer_or_drop_scope(self):
        workflow = read("references/workflow-contract.md")
        integration = read("references/arch-step-integration.md")
        examples = read("references/examples.md")

        self.assertIn("extend_current or new_sub_plan", workflow)
        self.assertIn("There is no auto-defer, auto-drop", integration)
        self.assertIn("Harmless improvement ignored, no scope action", examples)
        for text in [workflow, integration, examples]:
            self.assertNotIn("nice-to-have + defer-or-drop", text)
            self.assertNotIn("auto-applies (all items nice_to_have", text)
            self.assertNotIn("recommendation: defer", text)
            self.assertNotIn("recommendation: drop", text)


if __name__ == "__main__":
    unittest.main()
