import json
import tempfile
import unittest
from pathlib import Path

from scripts.pipeline import complete_phase, init_run, record_evidence, record_feedback, record_pilot
from scripts.skill_registry import resolve_skill


class PipelineTests(unittest.TestCase):
    def test_registry_resolves_from_an_explicit_portable_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "skills"
            skill_path = root / "target-trial" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text("---\nname: target-trial\n---\n", encoding="utf-8")
            result = resolve_skill("target-trial", [root])
            self.assertEqual(result["status"], "found")
            self.assertEqual(Path(result["path"]), skill_path.resolve())

    def test_pipeline_initialization_creates_state_and_handoffs(self):
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp) / "run"
            state = init_run("先查心衰研究空白和文献，再决定是否进入 TTE 协议", workdir, [])
            self.assertEqual(state["current_phase"], "intake")
            self.assertTrue((workdir / "research-state.json").is_file())
            self.assertTrue((workdir / "evidence-map.json").is_file())
            self.assertTrue((workdir / "evidence-ledger.json").is_file())
            self.assertTrue((workdir / "handoffs" / "00-intake.md").is_file())
            persisted = json.loads((workdir / "research-state.json").read_text(encoding="utf-8"))
            self.assertEqual(persisted["status"], "planned")
            self.assertIn("skill_resolution", persisted["route"])

    def test_record_evidence_writes_a_source_to_claim_row(self):
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp) / "run"
            init_run("先查文献，再决定 TTE 设计", workdir, [])
            result = record_evidence(
                workdir,
                "时间零点必须与资格和治疗分配对齐",
                "The eligibility, treatment assignment, and start of follow-up coincide.",
                "https://example.org/methods",
                "2026-10-25",
                "方法学来源；尚未与临床队列交叉验证",
                "single-source",
            )
            self.assertEqual(result["ledger"]["status"], "in_progress")
            self.assertEqual(len(result["ledger"]["records"]), 1)
            self.assertEqual(result["ledger"]["records"][0]["status"], "single-source")

    def test_literature_cannot_close_without_an_evidence_record(self):
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp) / "run"
            init_run("先查文献，再决定 TTE 设计", workdir, [])
            intake = workdir / "intake.md"
            intake.write_text("question", encoding="utf-8")
            complete_phase(workdir, "intake", "intake.md", "")
            evidence_map = json.loads((workdir / "evidence-map.json").read_text(encoding="utf-8"))
            evidence_map["status"] = "completed"
            (workdir / "evidence-map.json").write_text(json.dumps(evidence_map), encoding="utf-8")
            with self.assertRaises(SystemExit):
                complete_phase(workdir, "literature", "evidence-map.json", "")

    def test_pilot_and_feedback_update_next_action(self):
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp) / "run"
            init_run("协议已冻结，先做 pilot 再估计 TTE", workdir, [])
            state = record_pilot(workdir, "proceed", "队列、暴露和结局均有可观测记录")
            self.assertEqual(state["current_phase"], "execution")
            state = record_feedback(workdir, "assumption_violation", "权重出现极端值", "回到数据支持阶段并重审共同支持")
            self.assertEqual(state["current_phase"], "feedback")
            self.assertEqual(state["next_action"], "回到数据支持阶段并重审共同支持")
            self.assertTrue((workdir / "feedback.jsonl").is_file())

    def test_complete_phase_requires_a_real_artifact_and_advances(self):
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp) / "run"
            init_run("用 TTE 设计心衰目标试验", workdir, [])
            artifact = workdir / "intake.md"
            artifact.write_text("intake", encoding="utf-8")
            state = complete_phase(workdir, "intake", "intake.md", "临床决策已记录")
            self.assertEqual(state["current_phase"], "literature")
            self.assertEqual(state["phases"]["intake"]["status"], "completed")

    def test_initial_evidence_template_cannot_be_marked_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            workdir = Path(temp) / "run"
            init_run("先查文献，再决定 TTE 设计", workdir, [])
            with self.assertRaises(SystemExit):
                complete_phase(workdir, "literature", "evidence-map.json", "")


if __name__ == "__main__":
    unittest.main()
