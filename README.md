# Daxuan TTE Router

> 把“我想研究什么”变成一张有文献依据、estimand、数据缺口和 TTE Skill 交接的研究设计路线图。

这是本项目 TTE_CC 工具包的总入口。它先判断请求处于选题/文献反思、协议设计、仿真、估计、检查还是报告阶段，再选择最小的 TTE specialist 和必要的研究支持 Skill。

## 你什么时候需要它？

- 你有一个心衰、心肌梗死、糖尿病或肥胖研究想法，但还没有明确的临床决策和 estimand。
- 你需要把文献中的 T0、持续治疗、sequential trial、cloning 或竞争事件设计反思到自己的 MIMIC/eICU 数据。
- 你的协议已经冻结，需要选择 `tte-estimate`、检查共同支持和权重，再生成 TARGET 风格报告。

## 它会交付什么？

- `question_discovery`：证据任务、候选科学问题、研究设计 rationale 和候选 estimand。
- `protocol_design`：目标试验八要素、T0、治疗规则、intercurrent events 和变量级 data map 闸门。
- `emulation/analysis/checking/reporting`：最小 TTE Skill 路径、前置条件、数据缺口和实际运行状态。
- 路由 JSON、estimand card、心衰 data-support 表和可审计的下一步交接。

## 已接入的八个 TTE Skill

| 阶段 | Skill |
|---|---|
| 设计 | `target-trial`、`time-zero` |
| 持续策略与混杂 | `sustained-strategies`、`emulate-randomization` |
| 竞争事件 | `competing-events` |
| 估计 | `tte-estimate` |
| 审查 | `check-emulation` |
| 报告 | `tte-report` |

研究问题发现时按需联动 `auto-inspire-scientific-problem-selection`、`auto-inspire-paper-topic-discovery`、
`auto-inspire-academic-literature-search`、`auto-inspire-causal-inference`、
`auto-inspire-stat-method-selector` 和 `auto-inspire-survival-epi`。这些是支持 Skill，不替代八个 TTE specialist。

原始工具包位于 `/home/daxuan/.tte_cc`，专业入口位于 `/home/daxuan/.codex/skills/`。本路由器不复制它们的正文。

上游工具包：TTE_CC by Jacob Jameson（[GitHub](https://github.com/jacobjameson/TTE_CC)）。

## 快速开始

安装/发现入口：

```bash
npx skills add DaXuanGarden/daxuan-tte-router --skill daxuan-tte-router
npx skills add /home/daxuan/20260907_Clinical_Database/skills/daxuan-tte-router --skill daxuan-tte-router
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
python3 /home/daxuan/20260907_Clinical_Database/skills/daxuan-tte-router/scripts/route_tte.py \
  --text "我想找心衰肾功能恶化后的利尿策略研究空白和文献反思" --json
```

脚本只根据文字给出候选意图和路由，不读取数据库，也不自动检索文献。真实检索后，把核验来源写入
`evidence_sources` 和 [design-rationale.md](references/design-rationale.md)。使用
[route-card.md](references/route-card.md) 记录 `intent`、estimand、intercurrent events、识别假设和 data support。

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
- `tests/test_route_tte.py`：路由边界测试。

## 校验

```bash
python3 /home/daxuan/.codex/skills/qiaomu-meta-skill/scripts/validate_skill.py .
python3 -m unittest discover -s tests -v
python3 /home/daxuan/.codex/skills/qiaomu-meta-skill/scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python3 /home/daxuan/.codex/skills/qiaomu-meta-skill/scripts/export_skill_ir.py . --output reports/skill-ir.json
```

## 维护

当 TTE_CC specialist、研究支持 Skill、数据库语义或心衰协议发生变化时，按
[maintenance.md](references/maintenance.md) 更新规则、模板和意图测试，并重新生成报告文件。

## Troubleshooting

如果路由器没有触发，直接写出 `TTE`、`目标试验模拟`、`研究空白` 或目标阶段（例如 `time-zero`、`tte-estimate`）。如果只有一般“因果推断”而没有明确临床干预，路由器会先停在研究问题发现，不会自动选择 TTE 估计器。

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/
