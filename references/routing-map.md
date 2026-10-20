# TTE_CC 与研究设计路由判定表

| 用户任务中的核心动作 | 当前意图 | 首选路由 | 追加支持/路由 |
|---|---|---|---|
| 选题、研究空白、文献反思、比较研究设计 | `question_discovery` | `auto-inspire-scientific-problem-selection`、`auto-inspire-paper-topic-discovery` | `auto-inspire-academic-literature-search`；完成候选 estimand 后进入 `target-trial` |
| 统计方法选择、estimand 与结局设计 | `question_discovery` 或 `protocol_design` | `auto-inspire-stat-method-selector`、`auto-inspire-survival-epi` | 先完成 estimand card，再进入 `competing-events`/`tte-estimate` |
| 研究问题、协议、两种策略 | `protocol_design` | `target-trial` | `time-zero` |
| T0、多个入组时点、未来治疗、sequential trial、cloning | `protocol_design` | `time-zero` | `target-trial`、`sustained-strategies` |
| 继续/停止、剂量、治疗窗口、动态规则 | `protocol_design` 或 `emulation` | `sustained-strategies` | `time-zero`、`emulate-randomization` |
| 混杂、可交换性、IPW/标准化/匹配 | `emulation` | `emulate-randomization` | `sustained-strategies`（若时变） |
| 死亡、出院、RRT、失访、救援、switching | `emulation` | `competing-events` | `tte-estimate`（estimand 已冻结后） |
| 已冻结协议后的数据结构和估计 | `analysis` | `tte-estimate` | `competing-events`（若需要） |
| 权重、共同支持、平衡、负对照 | `checking` | `check-emulation` | `tte-estimate`（如需重跑） |
| 目标试验表、Methods、流程、Results | `reporting` | `tte-report` | 读取所有已完成阶段产物 |

## 路由后的最小交付

- 发现阶段：直接临床范例、方法学范例、反例/边界、候选科学问题、候选 estimand 和证据边界。
- 设计阶段：临床决策、8 要素协议、T0、策略、ICE、识别假设、data-support 和 data map。
- 估计阶段：已通过数据格式检查的 person-period 数据、估计量、bootstrap 和运行状态。
- 审查阶段：检查实际运行内容、结果、未能检查的项目和下一步。
- 报告阶段：目标试验表、观察数据映射、精度、敏感性分析、Methods/Results 和假设边界。

## 路由记录

需要可重复的初筛时使用 `scripts/route_tte.py --text '<请求>' --json`。脚本只做关键词和意图建议；
最终选择以临床决策、estimand、T0、数据语义和专业 Skill 的阶段闸门为准。每次交接保留
`references/route-card.md` 中的 `intent`、`selected`、`supporting_skills`、`evidence_gaps`、
`design_card` 和 `run status`。

## 心衰适配

现阶段主问题是“已接受静脉袢利尿治疗、仍有淤血并出现新的肾功能恶化后，维持与减量策略的短期比较”。
`+2 L` 只能作为候选容量触发，不能独立确诊心衰。治疗动作必须来自实际执行记录；未来是否继续用药不能定义 T0 分组。
