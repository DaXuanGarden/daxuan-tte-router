# 研究支持 Skill 入口

这些 Skill 支持研究问题发现和方法选择，但不替代八个 TTE_CC specialist，也不自动冻结协议。
路由器只保存名称和能力；`scripts/skill_registry.py` 会在运行时按安装根目录寻找
`<skill-name>/SKILL.md`，因此不会把某台机器的绝对路径写入公共包。

| Need | Supporting skill | Pipeline phase |
|---|---|---|
| clinical intake | `clinical-research-session` | `intake` |
| literature collection | `multi-database-literature-collector` | `literature` |
| verified literature retrieval | `auto-inspire-academic-literature-search` | `literature` |
| literature workflow | `auto-inspire-literature-workflow-orchestrator` | `literature` |
| gap audit | `medical-research-gap-finder` | `gap_audit` |
| problem choice and risk | `auto-inspire-scientific-problem-selection` | `question_refinement` |
| topic and gap mapping | `auto-inspire-paper-topic-discovery` | `question_refinement` |
| thesis refinement | `research-refine` / `research-refine-pipeline` | `question_refinement` |
| causal framing | `auto-inspire-causal-inference` | `data_support` |
| statistical method choice | `auto-inspire-stat-method-selector` | `data_support` |
| survival and competing risks teaching | `auto-inspire-survival-epi` | `data_support` |
| clinical analysis workflow | `clinical-research-analysis-framework` | `data_support` |
| EHR bias pitfalls | `clinical-research-pitfalls` | `data_support` |
| pilot planning | `experiment-plan` | `pilot` |
| code execution | `experiment-bridge` / `run-experiment` | `execution` |
| result audit | `experiment-audit` / `auto-review-loop` | `diagnostics` / `feedback` |

The registry is maintained in `references/skill-registry.json`. Missing optional skills are reported and
the run can continue; a missing required TTE specialist blocks the corresponding handoff instead of being
silently treated as executed.
