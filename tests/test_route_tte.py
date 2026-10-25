import unittest

from scripts.route_tte import route


class RouteTests(unittest.TestCase):
    def test_heart_failure_protocol_routes_design_and_competing_events(self):
        result = route("用TTE为心衰患者设计利尿维持与减量的目标试验，定义T0、剂量和死亡/出院结局")
        self.assertEqual(
            result["selected"],
            ["target-trial", "time-zero", "sustained-strategies", "competing-events"],
        )
        self.assertEqual(result["stage"], "emulation")

    def test_tte_signal_with_strategy_starts_at_protocol_design(self):
        result = route("用 TTE 评估心衰肾功能恶化后的利尿维持与减量")
        self.assertEqual(result["selected"], ["target-trial", "time-zero", "sustained-strategies"])

    def test_question_discovery_routes_evidence_support_before_protocol(self):
        result = route("我想找心衰肾功能恶化后的利尿策略研究空白和文献反思")
        self.assertEqual(result["intent"], "question_discovery")
        self.assertEqual(result["selected"], [])
        self.assertEqual(result["next_handoff"], "target-trial")
        self.assertIn("auto-inspire-paper-topic-discovery", result["supporting_skills"])
        self.assertEqual(len(result["evidence_tasks"]), 3)
        self.assertIn("evidence-ledger.json", result["pipeline"]["handoff_artifacts"])

    def test_literature_request_does_not_leak_strategy_keywords_to_tte(self):
        result = route("先查心衰肾功能恶化后利尿维持与减量的文献，再决定是否进入 TTE 协议")
        self.assertEqual(result["intent"], "question_discovery")
        self.assertEqual(result["selected"], [])
        self.assertTrue(result["pipeline"]["pilot_required_before_estimate"])

    def test_general_causal_question_does_not_auto_select_tte(self):
        result = route("做一个因果推断研究，分析肥胖对心肌梗死预后的影响")
        self.assertEqual(result["intent"], "question_discovery")
        self.assertEqual(result["selected"], [])
        self.assertIn("auto-inspire-causal-inference", result["supporting_skills"])

    def test_sequential_cloning_routes_sustained_strategy(self):
        result = route("同一个人在多个入组时点可能属于两个策略，需要 sequential trial 和 cloning")
        self.assertEqual(result["selected"], ["target-trial", "time-zero", "sustained-strategies"])

    def test_frozen_per_protocol_routes_estimation(self):
        result = route("协议已冻结，完成数据映射并估计 per-protocol effect")
        self.assertEqual(result["intent"], "analysis")
        self.assertEqual(result["selected"], ["tte-estimate"])
        self.assertEqual(result["prerequisites"], [])

    def test_statistical_method_request_keeps_estimand_gate(self):
        result = route("TTE 中心衰住院结局有死亡和出院，应该选择什么统计方法")
        self.assertEqual(result["intent"], "question_discovery")
        self.assertIn("auto-inspire-stat-method-selector", result["supporting_skills"])
        self.assertIn("competing-events", result["selected"])

    def test_frozen_protocol_estimate_routes_analysis(self):
        result = route("协议已冻结，运行 tte-estimate 并生成效应估计")
        self.assertEqual(result["selected"], ["tte-estimate"])
        self.assertEqual(result["stage"], "analysis")
        self.assertEqual(result["prerequisites"], [])

    def test_checking_requires_existing_analysis_object(self):
        result = route("检查IPW权重、共同支持和负对照")
        self.assertEqual(result["selected"], ["emulate-randomization", "check-emulation"])
        self.assertTrue(any("analysis object" in item for item in result["prerequisites"]))

    def test_non_tte_work_is_not_routed(self):
        result = route("翻译一段普通文档")
        self.assertEqual(result["selected"], [])
        self.assertEqual(result["stage"], "none")

    def test_generic_report_and_committee_do_not_trigger(self):
        self.assertEqual(route("写一篇普通报告")["selected"], [])
        self.assertEqual(route("committee meeting notes")["selected"], [])


if __name__ == "__main__":
    unittest.main()
