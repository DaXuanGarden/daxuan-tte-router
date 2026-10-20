# TTE 研究设计路由卡与阶段闸门

路由卡用于记录一次临床研究请求当前应该进入哪个阶段。它是交接记录，不是分析结果；空的
`evidence_sources` 不能被描述为已完成文献检索。

```text
intent: question_discovery | protocol_design | emulation | analysis | checking | reporting
stage: discovery | design | emulation | analysis | checking | reporting
selected: <按执行顺序排列的 TTE specialist 集合>
supporting_skills: <选题、文献、因果或统计支持 Skill>
why: <每个 selected Skill 对应的临床或方法学理由>
evidence_tasks: <直接范例、方法学范例、反例/边界>
evidence_sources: <实际检索并核验的来源；未检索时为空>
evidence_gaps: <创新性、数据语义或识别假设缺口>
design_card: <clinical decision、estimand、ICE、假设和 data support>
prerequisites: <尚未满足的协议、T0、数据映射或分析对象条件>
deliverable: <证据矩阵、研究设计卡、协议、数据字典、估计、诊断或报告产物>
stop condition: <进入下一阶段前必须满足的条件>
run status: suggested | consulted | drafted | executed | checked
```

## 意图到交付物

| 意图 | 先确认 | 主要交付物 | 下一步 |
|---|---|---|---|
| `question_discovery` | 临床决策 A/B、研究对象、结局、数据范围和文献证据边界 | 证据反思卡、候选问题、候选 estimand、研究设计 rationale | `target-trial` |
| `protocol_design` | 人群、A/B 策略、T0、随访、结局、ICE、summary measure 和识别假设 | 目标试验八要素协议、变量级 data map | `time-zero` 或策略定义 |
| `emulation` | 混杂、动态策略、sequential/cloning、竞争事件和数据时间顺序 | emulation 对象、权重/删失/竞争事件规则 | `tte-estimate` |
| `analysis` | 协议和 estimand 已冻结，person-period/data map 可执行 | 估计对象、效应估计、精度和运行日志 | `check-emulation` |
| `checking` | 已有 estimand、处理分配和估计对象 | 共同支持、权重、平衡、负对照和敏感性诊断 | `tte-report` |
| `reporting` | 能区分已执行结果、计划内容和未验证假设 | TARGET 对账表、Methods、流程、Results 或协议报告 | 外部审阅 |

## Estimand card 最小字段

```text
clinical_decision:
population:
treatment_strategy_A:
treatment_strategy_B:
outcome:
follow_up:
summary_measure:
intercurrent_events:
estimand_status: draft | frozen | blocked
identifying_assumptions:
  exchangeability:
  positivity:
  consistency:
  well_defined_intervention:
data_support:
literature_evidence:
  direct_clinical_example:
  methods_example:
  boundary_or_counterexample:
next_handoff:
```

统计方法写在 estimand card 之后。每个候选方法都要说明它回答的 estimand、依赖的识别假设、数据要求
和不适用条件。模型名称不能反向决定临床问题。

## 阶段闸门

- **发现 → 协议**：至少记录一个直接临床 TTE 范例、一个方法学范例和一个反例/边界；记录检索库、检索式、日期和核验来源。没有检索时标记为待核验，不写成“全球首次”。
- **协议 → 仿真**：population、A/B 策略、assignment/T0、follow-up、outcome、causal contrast、analysis plan 和变量级 data map 均有状态。
- **动态策略 → 估计**：每个时间点的 treatment、confounder、outcome、rescue、switching、censoring 和测量时间可观测；时变混杂由既往治疗影响时，普通回归不能作为默认方案。
- **竞争事件 → 估计**：先明确死亡、出院、RRT 或失访在 estimand 中的角色，再决定 cause-specific hazard、CIF/Aalen–Johansen 或其他模型；不机械把出院当作普通删失。
- **估计 → 检查**：已有 estimand、处理分配和分析对象；检查结果必须能改变下一步判断。
- **检查 → 报告**：报告中逐项区分 target trial、observational mapping、估计量、精度、敏感性分析和未验证假设。

如果处理在新的肌酐、血压、氧合或容量信号出现后发生，信号出现的时刻就是需要重新审查的决策点。不能用后续实际用药、存活到出院、或完成随访测量回填基线策略。
