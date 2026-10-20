# Daxuan TTE Router

> 把“我想研究什么”变成一张有文献依据、estimand、数据缺口和 TTE Skill 交接的研究设计路线图。

面向用户的名称统一写作 **TTE**；`target-trial`、`tte-estimate` 等是上游 Skill 的精确标识符，保持原样以确保安装和路由兼容。详见 [naming-conventions.md](references/naming-conventions.md)。

这是本项目 TTE_CC 工具包的总入口。它先判断请求处于选题/文献反思、协议设计、仿真、估计、检查还是报告阶段，再选择最小的 TTE specialist 和必要的研究支持 Skill。`scripts/pipeline.py` 在此基础上提供可恢复的研究运行目录、阶段交接和 pilot 门禁。

## 你什么时候需要它？

- 你有一个心衰、心肌梗死、糖尿病或肥胖研究想法，但还没有明确的临床决策和 estimand。
- 你需要把文献中的 T0、持续治疗、sequential trial、cloning 或竞争事件设计反思到自己的 MIMIC/eICU 数据。
- 你的协议已经冻结，需要选择 `tte-estimate`、检查共同支持和权重，再生成 TARGET 风格报告。

## 它会交付什么？

- `question_discovery`：证据任务、候选科学问题、研究设计 rationale 和候选 estimand。
- `protocol_design`：目标试验八要素、T0、治疗规则、intercurrent events 和变量级 data map 闸门。
- `emulation/analysis/checking/reporting`：最小 TTE Skill 路径、前置条件、数据缺口和实际运行状态。
- 路由 JSON、estimand card、心衰 data-support 表、研究状态和可审计的下一步交接。

## 已接入的八个 TTE Skill

| 阶段 | Skill |
|---|---|
| 设计 | `target-trial`、`time-zero` |
| 持续策略与混杂 | `sustained-strategies`、`emulate-randomization` |
| 竞争事件 | `competing-events` |
| 估计 | `tte-estimate` |
| 审查 | `check-emulation` |
| 报告 | `tte-report` |

研究问题发现时按需联动 `clinical-research-session`、`multi-database-literature-collector`、
`auto-inspire-literature-workflow-orchestrator`、`medical-research-gap-finder`、
`auto-inspire-scientific-problem-selection`、`auto-inspire-paper-topic-discovery`、
`auto-inspire-academic-literature-search`、`auto-inspire-causal-inference`、
`auto-inspire-stat-method-selector` 和 `auto-inspire-survival-epi`。这些是支持 Skill，不替代八个 TTE specialist；完整注册见 [references/skill-registry.json](references/skill-registry.json)。

原始工具包通过 `TTE_CC_HOME` 定位，专业入口通过 `CODEX_SKILLS_ROOT`、`DAXUAN_SKILLS_ROOT` 或常规用户 Skill 目录定位。本路由器不复制它们的正文。

上游工具包：TTE_CC by Jacob Jameson（[GitHub](https://github.com/jacobjameson/TTE_CC)）。

## 快速开始

安装/发现入口：

```bash
npx skills add DaXuanGarden/daxuan-tte-router --skill daxuan-tte-router
npx skills add ./skills/daxuan-tte-router --skill daxuan-tte-router
```

你可以直接这样说：

```text
使用 daxuan-tte-router，先查阅心衰肾功能恶化后的利尿策略文献，比较研究空白，生成候选 estimand，再决定是否进入目标试验协议。
```

```text
按 daxuan-tte-router，审核心衰肌酐升高后的利尿维持与减量策略，先做 T0、intercurrent events 和结局定义，不运行估计。
```

```text
协议已经冻结。使用 tte-estimate，然后用 check-emulation 审核权重、共同支持和负对照，最后生成 tte-report。
```

## Examples

可复现 JSON 示例见 [examples/](examples/)。

## 可重复路由与研究设计卡

```bash
python3 scripts/route_tte.py \
  --text "我想找心衰肾功能恶化后的利尿策略研究空白和文献反思" --json
```

脚本只根据文字给出候选意图和路由，不读取数据库，也不自动检索文献。真实检索后，把核验来源写入
`evidence_sources` 和 [design-rationale.md](references/design-rationale.md)。使用
[route-card.md](references/route-card.md) 记录 `intent`、estimand、intercurrent events、识别假设和 data support。

### 可恢复研究运行

初始化只创建状态和交接模板，不查询数据库、不抓取文献、不运行估计：

```bash
python3 scripts/pipeline.py init \
  --text "先查心衰肾功能恶化后的利尿策略文献，再决定是否进入 TTE 协议" \
  --workdir ./tte-runs/heart-failure-renal-signal
python3 scripts/pipeline.py status --workdir ./tte-runs/heart-failure-renal-signal
python3 scripts/pipeline.py dispatch --workdir ./tte-runs/heart-failure-renal-signal
```

运行目录包含 `research-state.json`、`route-card.json`、`evidence-map.json`、`evidence-ledger.json`、`design-card.json`、
`dispatch-manifest.json`、`run-bundle.md`、`pilot-report.md`、`feedback.md` 和 `handoffs/`。`dispatch`
只生成有序交接，不执行数据库查询或临床估计。完成每个阶段后用 `complete-phase` 写入真实产物；
完整估计前必须用 `record-pilot --decision proceed` 记录队列、暴露、结局、时间零点、随访和重叠性检查。
如果 pilot 需要改设计，使用 `downgrade`；如果数据不支持，使用 `stop`。分析或 pilot 后使用
`feedback` 记录 `data_failure`、`design_failure`、`assumption_violation`、`null_result`、
`positive_result` 或 `pilot_failure`，并写明下一步动作。

### 证据账本

每条影响研究问题或 estimand 的主张都应写入 `evidence-ledger.json`。记录至少包括主张、原文片段、来源 URL、来源日期、独立性说明和验证状态：

```bash
python3 scripts/pipeline.py record-evidence \
  --workdir ./tte-runs/heart-failure-renal-signal \
  --claim "研究中的治疗决策发生在预先定义的时间零点" \
  --passage "<从原始来源实际读取的支持片段>" \
  --source-url "https://example.org/source" \
  --source-date "2026-10-25" \
  --independence-note "方法学来源；尚未与临床队列研究交叉验证" \
  --status single-source
```

文献阶段没有证据账本记录时，`complete-phase` 会停止，不能把空检索写成研究空白。

### 状态完整性

`record-pilot` 只能在前置阶段完成并进入 `pilot` 后执行；`proceed` 不会跳过协议和数据支持闸门。共享的
`research-state.json` 只保留 Skill 解析状态，不写入本机绝对路径。账本只有在全部记录为 `verified` 时才标记为已核验。

## 心衰首个 Showcase

当前优先回放的问题是：急性心衰患者仍有容量负荷、已接受静脉袢利尿剂并出现预先定义的肾功能恶化信号后，未来 24 小时维持还是降低利尿强度？

路由应先生成文献反思和 [heart-failure-data-support.md](references/heart-failure-data-support.md)，再进入：

```text
question discovery → target-trial → time-zero → sustained-strategies
→ emulate-randomization → competing-events → tte-estimate → check-emulation → tte-report
```

`+2 L` 只能作为候选容量触发，不能独立确诊急性心衰或淤血；剂量比例、肾功能阈值、治疗窗口和补救规则必须在估计前由临床依据与数据可观测性共同确定。

## 使用边界

路由器负责选择和衔接 Skill；文献检索、目标试验协议、数据语义和实际估计仍由对应 Skill 与本项目资料决定。教学数据不是心血管证据。没有真实运行的检索、估计、检查或报告，不会被描述为已完成。

统计方法必须在 estimand 和数据支持性明确后选择。路由器不会从结果倒推阈值、把普通因果问题自动当作 TTE、或把文献中出现的设计直接复制到 MIMIC/eICU。

## 文件结构

- `SKILL.md`：意图层、TTE 路由规则和阶段闸门。
- `references/route-card.md`：交接格式和 estimand/ICE 闸门。
- `references/estimand-card.md`：estimand 模板。
- `references/design-rationale.md`：文献反思和候选问题模板。
- `references/heart-failure-data-support.md`：心衰变量级数据支持表。
- `scripts/route_tte.py`：无依赖的可重复初筛器。
- `scripts/skill_registry.py`：按能力注册表解析已安装 Skill，不写死本机路径。
- `scripts/pipeline.py`：创建、恢复和更新研究运行状态。
- `dispatch-manifest.json` / `run-bundle.md`：记录有序 specialist handoff 和当前执行边界。
- `evidence-ledger.json`：逐条保存主张到来源的可审计证据链。
- `tests/test_route_tte.py`：路由边界测试。

## 校验

```bash
python3 -m unittest discover -s tests -v
python3 scripts/skill_registry.py --json --skill target-trial
python3 scripts/route_tte.py --text "协议已冻结，运行 tte-estimate 并检查共同支持" --json
```

如果本地安装了 `qiaomu-meta-skill`，可以另外运行其 `validate_skill.py`、`trigger_eval.py` 和
`export_skill_ir.py`；这些是发布环境检查，不是本包的运行时依赖。

## 维护

当 TTE_CC specialist、研究支持 Skill、数据库语义或心衰协议发生变化时，按
[maintenance.md](references/maintenance.md) 更新规则、模板和意图测试，并重新生成报告文件。

## Troubleshooting

如果路由器没有触发，直接写出 `TTE`、`目标试验模拟`、`研究空白` 或目标阶段（例如 `time-zero`、`tte-estimate`）。如果只有一般“因果推断”而没有明确临床干预，路由器会先停在研究问题发现，不会自动选择 TTE 估计器。

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/
