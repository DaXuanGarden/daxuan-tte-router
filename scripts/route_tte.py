#!/usr/bin/env python3
"""Suggest an evidence-aware route for a TTE research request.

The router is deterministic and dependency-free. It classifies the user's
intent, suggests research-support skills when a question is still being
formed, and selects the smallest TTE_CC specialist set. The companion
``pipeline.py`` resolves installed skills and persists the staged handoff;
this module itself never reads data, fetches literature, or makes a clinical
decision.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Rule:
    name: str
    stage: str
    reason: str
    patterns: tuple[str, ...]


CANONICAL_ORDER = (
    "target-trial",
    "time-zero",
    "sustained-strategies",
    "emulate-randomization",
    "competing-events",
    "tte-estimate",
    "check-emulation",
    "tte-report",
)

RESEARCH_SUPPORT_ORDER = (
    "clinical-research-session",
    "multi-database-literature-collector",
    "auto-inspire-literature-workflow-orchestrator",
    "medical-research-gap-finder",
    "auto-inspire-scientific-problem-selection",
    "auto-inspire-paper-topic-discovery",
    "auto-inspire-academic-literature-search",
    "clinical-research-pitfalls",
    "auto-inspire-causal-inference",
    "auto-inspire-stat-method-selector",
    "auto-inspire-survival-epi",
    "clinical-research-analysis-framework",
)

RULES = (
    Rule(
        "target-trial",
        "design",
        "defines the population, treatment strategies, outcome, horizon, T0, and estimand",
        (
            "target trial",
            "target-trial",
            "目标试验",
            "目标模拟",
            "研究问题",
            "研究方案",
            "protocol",
            "causal question",
            "因果问题",
        ),
    ),
    Rule(
        "time-zero",
        "design",
        "aligns eligibility, assignment, follow-up, and the decision time",
        (
            "time-zero",
            "time zero",
            "t0",
            "时间零点",
            "起始时间",
            "不死时间",
            "immortal time",
            "sequential trial",
            "序贯试验",
            "多个入组",
            "multiple eligibility",
            "cloning",
            "clone-censor-weight",
            "克隆",
        ),
    ),
    Rule(
        "sustained-strategies",
        "design",
        "defines duration, continuation, stopping, dose, timing, or repeated treatment decisions",
        (
            "sustained-strategies",
            "持续策略",
            "持续治疗",
            "维持",
            "减量",
            "停用",
            "持续利尿",
            "利尿策略",
            "治疗窗口",
            "剂量",
            "dose",
            "duration",
            "continuation",
            "repeated treatment",
            "动态策略",
            "dynamic strategy",
            "time-varying treatment",
            "时变治疗",
            "时变混杂",
            "time-varying confounding",
            "cloning",
            "clone-censor-weight",
            "克隆",
        ),
    ),
    Rule(
        "emulate-randomization",
        "emulation",
        "defines confounding control, exchangeability, standardization, weighting, or matching",
        (
            "emulate-randomization",
            "混杂",
            "可交换性",
            "exchangeability",
            "confound",
            "confounding",
            "标准化",
            "standardization",
            "ipw",
            "权重",
            "匹配",
            "matching",
            "倾向评分",
            "识别假设",
            "identifying assumption",
            "positivity",
            "consistency",
        ),
    ),
    Rule(
        "competing-events",
        "emulation",
        "defines death, discharge, RRT, loss to follow-up, or intercurrent-event handling",
        (
            "competing-events",
            "竞争事件",
            "死亡",
            "出院",
            "rrt",
            "透析",
            "失访",
            "competing event",
            "censor",
            "截断",
            "post-death",
            "intercurrent event",
            "intercurrent events",
            "救援",
            "rescue",
            "switch",
            "switching",
            "停药",
        ),
    ),
    Rule(
        "tte-estimate",
        "analysis",
        "creates or runs the prespecified effect estimate after the protocol is frozen",
        (
            "tte-estimate",
            "估计代码",
            "分析代码",
            "运行分析",
            "run the analysis",
            "pooled logistic",
            "person-time",
            "g-formula",
            "tmle",
            "per-protocol",
            "intention-to-treat",
            "itt",
            "风险差",
            "risk difference",
            "risk ratio",
            "hazard ratio",
            "效应估计",
        ),
    ),
    Rule(
        "check-emulation",
        "checking",
        "checks overlap, balance, extreme weights, negative controls, or emulation diagnostics",
        (
            "check-emulation",
            "共同支持",
            "overlap",
            "平衡",
            "balance",
            "极端权重",
            "权重诊断",
            "负对照",
            "negative control",
            "诊断",
            "effective sample size",
            "ess",
        ),
    ),
    Rule(
        "tte-report",
        "reporting",
        "documents the protocol, methods, flow, results, or TTE reporting artifact",
        (
            "tte-report",
            "报告",
            "论文",
            "protocol table",
            "methods",
            "results",
            "流程图",
            "report",
            "manuscript",
            "target statement",
            "target guideline",
        ),
    ),
)

TTE_STRONG_SIGNAL = (
    "tte",
    "tte_cc",
    "target trial",
    "target-trial",
    "目标试验",
    "目标模拟",
    "观察性目标试验",
)
TTE_WORKFLOW_SIGNAL = (
    "sequential trial",
    "序贯试验",
    "multiple eligibility",
    "多个入组",
    "cloning",
    "clone-censor-weight",
    "克隆",
)
TTE_DESIGN_SIGNAL = (
    "time-zero",
    "time zero",
    "时间零点",
    "不死时间",
    "immortal time",
    "持续策略",
    "持续利尿",
    "利尿策略",
    "动态策略",
    "时变治疗",
    "time-varying treatment",
    "竞争事件",
    "competing event",
)
WEAK_CAUSAL_SIGNAL = ("causal inference", "因果推断")
DISCOVERY_SIGNAL = (
    "选题",
    "科学问题",
    "研究空白",
    "文献反思",
    "研究设计比较",
    "研究意义",
    "文献",
    "检索",
    "research gap",
    "research question",
    "literature",
    "novelty",
    "topic",
    "clinical significance",
)
STATS_SIGNAL = (
    "统计方法",
    "方法选择",
    "模型选择",
    "估计量",
    "statistical method",
    "which model",
    "survival analysis",
    "生存分析",
    "竞争风险分析",
)
ANALYSIS_CONTEXT_SIGNAL = (
    "tte-estimate",
    "per-protocol",
    "intention-to-treat",
    "itt",
    "协议已冻结",
    "方案已冻结",
    "数据映射已完成",
    "estimand frozen",
    "estimand 已冻结",
)
CLINICAL_CONTEXT = (
    "心衰",
    "心肌梗死",
    "心血管",
    "糖尿病",
    "肥胖",
    "icu",
    "mimic",
    "eicu",
    "临床",
    "住院",
    "患者",
    "治疗",
    "药物",
    "利尿",
    "结局",
    "死亡",
    "cardiovascular",
    "heart failure",
    "diabetes",
    "obesity",
    "hospital",
    "treatment",
    "outcome",
)
NON_TTE_ONLY = (
    "traffic simulation",
    "交通仿真",
    "translation",
    "翻译",
    "普通文档",
    "ordinary document",
)
NON_TTE_NEGATION = (
    "不涉及临床研究",
    "不涉及 tte",
    "not a clinical research",
    "not clinical research",
    "without tte",
)

DISCOVERY_SKILLS = (
    "clinical-research-session",
    "multi-database-literature-collector",
    "auto-inspire-literature-workflow-orchestrator",
    "medical-research-gap-finder",
    "auto-inspire-scientific-problem-selection",
    "auto-inspire-paper-topic-discovery",
    "auto-inspire-academic-literature-search",
)


def _contains(text: str, patterns: Iterable[str]) -> list[str]:
    lowered = text.casefold()
    exact_tokens = {"tte", "t0", "ipw", "rrt", "itt", "ess"}
    found: list[str] = []
    for pattern in patterns:
        token = pattern.casefold()
        if token in exact_tokens:
            if re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", lowered):
                found.append(pattern)
        elif token in lowered:
            found.append(pattern)
    return found


def _empty_result(normalized: str, confidence: str = "low") -> dict[str, object]:
    return {
        "intent": "none",
        "stage": "none",
        "selected": [],
        "supporting_skills": [],
        "reasons": {},
        "evidence_tasks": [],
        "evidence_sources": [],
        "evidence_gaps": [],
        "design_card": {},
        "prerequisites": [],
        "next_handoff": None,
        "stop_condition": "State a clinical research question or an explicit TTE workflow stage.",
        "run_status": "suggested",
        "confidence": confidence,
        "unmatched": normalized,
        "pipeline": {
            "state_artifact": "research-state.json",
            "handoff_artifacts": [],
            "pilot_required_before_estimate": True,
            "execution_mode": "suggested",
        },
    }


def _frozen(text: str) -> bool:
    return bool(
        _contains(
            text,
            (
                "protocol frozen",
                "protocol is frozen",
                "协议已冻结",
                "方案已冻结",
                "数据映射已完成",
                "design is complete",
                "estimand frozen",
                "estimand 已冻结",
            ),
        )
    )


def _design_card(frozen: bool, discovery: bool) -> dict[str, str]:
    return {
        "clinical_decision": "required",
        "population": "required",
        "treatment_strategy_A": "required",
        "treatment_strategy_B": "required",
        "outcome": "required",
        "follow_up": "required",
        "summary_measure": "required",
        "intercurrent_events": "required",
        "estimand_status": "frozen" if frozen else "draft",
        "identifying_assumptions": "required",
        "data_support": "required",
        "literature_evidence": "required" if discovery else "recommended",
    }


def route(text: str) -> dict[str, object]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return _empty_result(normalized)

    strong_hits = _contains(normalized, TTE_STRONG_SIGNAL)
    workflow_hits = _contains(normalized, TTE_WORKFLOW_SIGNAL)
    design_hits = _contains(normalized, TTE_DESIGN_SIGNAL)
    weak_causal_hits = _contains(normalized, WEAK_CAUSAL_SIGNAL)
    discovery_hits = _contains(normalized, DISCOVERY_SIGNAL)
    stats_hits = _contains(normalized, STATS_SIGNAL)
    clinical_hits = _contains(normalized, CLINICAL_CONTEXT)
    explicit_stage_hits = _contains(
        normalized,
        CANONICAL_ORDER
        + ("ipw", "positivity", "共同支持", "负对照", "权重诊断")
        + ANALYSIS_CONTEXT_SIGNAL,
    )
    non_tte_hits = _contains(normalized, NON_TTE_ONLY)
    non_tte_negation_hits = _contains(normalized, NON_TTE_NEGATION)

    clinical_causal = bool(weak_causal_hits and clinical_hits)
    research_signal = bool(
        strong_hits
        or workflow_hits
        or explicit_stage_hits
        or (discovery_hits and clinical_hits)
        or clinical_causal
        or (design_hits and clinical_hits)
    )
    if non_tte_negation_hits:
        return _empty_result(normalized, "high")
    if non_tte_hits and not strong_hits and not workflow_hits:
        return _empty_result(normalized, "high")
    if not research_signal:
        return _empty_result(normalized)

    literature_request = bool(discovery_hits)
    if literature_request:
        intent = "question_discovery"
    elif explicit_stage_hits or strong_hits or workflow_hits or (design_hits and clinical_hits):
        if _contains(normalized, ("tte-estimate", "per-protocol", "intention-to-treat", "itt", "运行分析", "估计代码")):
            intent = "analysis"
        elif _contains(normalized, ("check-emulation", "共同支持", "overlap", "权重诊断", "负对照", "balance")):
            intent = "checking"
        elif _contains(normalized, ("tte-report", "target statement", "methods", "results", "报告", "论文")):
            intent = "reporting"
        elif stats_hits:
            intent = "question_discovery"
        elif _contains(normalized, ("混杂", "confounding", "competing-events", "竞争事件", "死亡", "出院", "rrt", "时变混杂", "time-varying")):
            intent = "emulation"
        else:
            intent = "protocol_design"
    elif stats_hits:
        intent = "question_discovery"
    else:
        intent = "question_discovery"

    hits: dict[str, list[str]] = {}
    selected: set[str] = set()
    for rule in RULES:
        matched = _contains(normalized, rule.patterns)
        if matched:
            selected.add(rule.name)
            hits[rule.name] = matched

    frozen = _frozen(normalized)
    if frozen and "target-trial" in selected and not _contains(normalized, ("target trial", "target-trial", "目标试验", "目标模拟")):
        selected.remove("target-trial")
        hits.pop("target-trial", None)
    terminal_stage_requested = bool(selected.intersection(("tte-estimate", "check-emulation", "tte-report")))
    # Discovery asks for evidence first. Add the protocol specialist only when
    # the request also asks to turn an explicit TTE decision into a protocol.
    if (strong_hits or workflow_hits) and not terminal_stage_requested and intent != "question_discovery":
        selected.add("target-trial")
        hits.setdefault("target-trial", strong_hits or workflow_hits)

    if "sustained-strategies" in selected and "time-zero" not in selected and not frozen:
        selected.add("time-zero")
        hits.setdefault("time-zero", ["sustained-strategy gate"])
    if "tte-estimate" in selected and not frozen:
        selected.update(("target-trial", "time-zero"))
        hits.setdefault("target-trial", ["estimate gate"])
        hits.setdefault("time-zero", ["estimate gate"])

    ordered = [name for name in CANONICAL_ORDER if name in selected]

    # A literature-led discovery request may mention a treatment duration or
    # competing event while still asking whether the question is worth
    # studying. Do not let those words prematurely dispatch a TTE specialist.
    # The discovery handoff must first produce evidence and a clinical
    # decision; a later request can then route the protocol stages.
    if literature_request:
        ordered = []
        hits = {}

    supporting: set[str] = set()
    if intent == "question_discovery":
        supporting.update(DISCOVERY_SKILLS)
    if stats_hits:
        supporting.add("auto-inspire-stat-method-selector")
        if _contains(normalized, ("生存", "survival", "竞争风险", "competing", "死亡", "出院")):
            supporting.add("auto-inspire-survival-epi")
    if _contains(normalized, ("混杂", "confounding", "因果", "causal", "识别假设", "exchangeability")):
        supporting.add("auto-inspire-causal-inference")
    if _contains(normalized, ("偏倚", "immortal", "信息泄漏", "selection bias", "time zero", "T0")):
        supporting.add("clinical-research-pitfalls")
    if intent in ("protocol_design", "emulation", "analysis"):
        supporting.add("clinical-research-analysis-framework")
    if _contains(normalized, ("收敛", "refine", "refinement", "候选题目", "candidate topic")):
        supporting.add("research-refine")
    supporting_ordered = [name for name in RESEARCH_SUPPORT_ORDER if name in supporting]

    evidence_tasks: list[str] = []
    evidence_gaps: list[str] = []
    if intent == "question_discovery":
        evidence_tasks = [
            "Find one direct clinical TTE example and extract population, strategy, outcome, horizon, and estimand.",
            "Find one methods example for the proposed time-zero, dynamic strategy, or competing-event problem.",
            "Find one boundary or counterexample and record why its design or data cannot be copied.",
        ]
        evidence_gaps.append("No literature was fetched by this keyword router; record database, query, date, and verified sources before claiming novelty.")
    if strong_hits or workflow_hits:
        evidence_gaps.append("Confirm that the treatment action, decision time, outcome, and required longitudinal measurements are observable in the chosen database.")
    if weak_causal_hits and not strong_hits and not workflow_hits:
        evidence_gaps.append("A general causal question was detected; confirm a well-defined clinical intervention and whether TTE is the intended framework before routing to target-trial.")

    prerequisites: list[str] = []
    if intent == "question_discovery":
        prerequisites.append("Complete the evidence tasks and design card before freezing the target-trial protocol.")
    if "target-trial" in ordered and intent != "question_discovery" and not frozen:
        prerequisites.append("Define clinical decision, population, A/B strategies, outcome, horizon, T0, estimand, and data support.")
    if "tte-estimate" in ordered and not frozen:
        prerequisites.append("Freeze all eight target-trial elements and the variable-level data map before estimation.")
    if "check-emulation" in ordered and "tte-estimate" not in ordered:
        prerequisites.append("Provide the estimand and analysis object whose overlap, balance, or weights will be checked.")
    if "tte-report" in ordered and not ("tte-estimate" in ordered or frozen):
        prerequisites.append("Identify whether the deliverable is protocol-only or includes executed estimates and diagnostics.")

    if intent == "question_discovery":
        stage = "discovery"
        next_handoff = "target-trial"
    elif "tte-report" in ordered:
        stage = "reporting"
        next_handoff = None
    elif "check-emulation" in ordered:
        stage = "checking"
        next_handoff = "tte-report"
    elif "tte-estimate" in ordered:
        stage = "analysis"
        next_handoff = "check-emulation"
    elif "emulate-randomization" in ordered or "competing-events" in ordered:
        stage = "emulation"
        next_handoff = "tte-estimate"
    else:
        stage = "design"
        if ordered:
            last = ordered[-1]
            next_index = CANONICAL_ORDER.index(last) + 1
            next_handoff = CANONICAL_ORDER[next_index] if next_index < len(CANONICAL_ORDER) else None
        else:
            next_handoff = "target-trial"

    reasons = {}
    for name in ordered:
        rule = next(rule for rule in RULES if rule.name == name)
        reasons[name] = {"why": rule.reason, "matched": hits.get(name, [])}

    return {
        "intent": intent,
        "stage": stage,
        "selected": ordered,
        "supporting_skills": supporting_ordered,
        "reasons": reasons,
        "evidence_tasks": evidence_tasks,
        "evidence_sources": [],
        "evidence_gaps": evidence_gaps,
        "design_card": _design_card(frozen, intent == "question_discovery"),
        "prerequisites": prerequisites,
        "next_handoff": next_handoff,
        "stop_condition": "Resolve the listed prerequisites and confirm the selected artifact before advancing.",
        "run_status": "suggested",
        "confidence": "high" if strong_hits or workflow_hits or len(ordered) > 1 else "medium",
        "unmatched": normalized,
        "pipeline": {
            "state_artifact": "research-state.json",
            "handoff_artifacts": [
                "route-card.json",
                "evidence-map.json",
                "evidence-ledger.json",
                "design-card.json",
                "dispatch-manifest.json",
                "run-bundle.md",
                "pilot-report.md",
                "feedback.md",
            ],
            "pilot_required_before_estimate": True,
            "execution_mode": "suggested",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, help="TTE or clinical research task description")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit JSON")
    args = parser.parse_args()
    result = route(args.text)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"intent: {result['intent']}")
        print(f"stage: {result['stage']}")
        print(f"selected: {', '.join(result['selected']) or '[]'}")
        print(f"supporting_skills: {', '.join(result['supporting_skills']) or '[]'}")
        print(f"next_handoff: {result['next_handoff'] or 'none'}")
        for item in result["prerequisites"]:
            print(f"prerequisite: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
