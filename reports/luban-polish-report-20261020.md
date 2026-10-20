# daxuan-tte-router 打磨报告

审阅日期：2026-10-20  
审阅范围：本地 Skill 包、路由脚本、触发评估、单元测试、结构检查、TTE 方法学来源  
本轮状态：方案 B 已实施；完成验料、访行、过尺、意图路由改写和验证门。

## 1. 验料结果（Skill 前提挑战）

挑战1 - 真实问题：**成立**。八个并列 TTE Skill 分散在本机，研究者需要先判断研究处于选题、协议、T0、动态策略、混杂、竞争事件、估计、检查还是报告阶段。当前路由器确实减少了入口选择成本。

挑战2 - 独特角度：唯一性来自**工作流和项目临床语义**：它保留 TTE_CC 的八个专业边界，又加入 MIMIC/eICU 与 INSPIRE/MOVER 的数据角色、心衰两个 T0 不同的问题，以及可重复的 route card。当前独特性尚未覆盖“文献证据如何改变科学问题和统计方案”。

挑战3 - 安装理由：**成立但需要补强**。安装后可以得到最小 TTE Skill 路径、阶段闸门和 run status；但用户提出“选题、研究空白、文献反思、estimand 与统计方法”时，当前 Skill 还会过早进入 TTE 设计或只返回关键词路由。

挑战4 - 公共传播性：钩子是“一个入口管理八个 TTE 专业 Skill”。0.2.0 只有 route card 和路由 JSON；0.3.0 已加入研究设计卡、证据任务和两个不含隐私的 JSON showcase。

验料结论：**好料，继续打磨；定位应从“八个 TTE Skill 路由器”升级为“证据约束的 TTE 研究设计路由器”。**

## 2. 访行记录（同类 Skill 与方法同行）

| 同类来源 | 链接 | 类型 | 一句话定位 | 可学手艺 | 不能照搬的点 |
|---|---|---|---|---|---|
| TTE_CC | [GitHub](https://github.com/jacobjameson/TTE_CC) | 直接 | 将 TTE 拆成协议、T0、持续策略、混杂、竞争事件、估计、检查、报告 | 保持 specialist 边界和 person-time → 权重/估计 → 诊断 → 报告的链条 | 教学数据和 helper 不是心血管证据 |
| Hernán & Robins | [AJE 2016](https://academic.oup.com/aje/article/183/8/758/1739860) | 方法同行 | 先写能回答临床决策的假想随机试验，再决定观察数据如何模拟 | 把临床问题、协议、识别假设和分析计划分开 | TTE 不会自动消除未测混杂、测量误差和 positivity 问题 |
| BMJ Target Trial | [BMJ 2022](https://www.bmj.com/content/378/bmj-2022-071108) | 方法同行 | 用随机试验原则约束观察性研究的 time zero、策略和因果对比 | 先确定 ITT/per-protocol，再决定估计方法 | 不能把未来治疗或存活者回填到基线 |
| Starting Right | [BMJ 2025/2026](https://www.bmj.com/content/392/bmj-2025-084909) | 方法同行 | 处理 sequential trials、cloning 和重复入组的 time-zero 设计 | 将多次入组、多个可行策略和 cluster bootstrap 变成显式路由条件 | 不应把所有研究都扩成 cloning 设计 |
| TARGET Statement | [BMJ 2025](https://www.bmj.com/content/390/bmj-2025-087179) | 报告同行 | 逐项报告 target trial、emulation、estimand、数据映射和敏感性分析 | 将报告作为协议与结果的一一对账，而不是最后的文字润色 | 不能只写“进行了 TTE” |
| ICH E9(R1) | [EMA guidance](https://www.ema.europa.eu/en/scientific-guidelines/ich-e9-statistical-principles-clinical-trials) | 统计设计同行 | 用 estimand 约束 clinical question、estimator、estimate 和 sensitivity | 将 population、treatment、endpoint、summary measure、intercurrent events 固定为前置字段 | 不能让现成模型反过来决定问题 |
| Dynamic treatment strategies | [PMC primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC5710813/) | 统计设计同行 | 解释时变混杂受既往治疗影响时为何需要 g-methods | 将时间顺序、治疗/混杂/结局测量和 positivity 设为动态策略闸门 | 单次暴露数据不能硬套动态策略 |
| EHR-Trial-Emulation | [GitHub](https://github.com/real-causal/EHR-Trial-Emulation) | 直接/教学 | 用 notebook 演示 T0、策略、随访/删失、因果对比和 overlap 诊断 | 把路由变成诊断决策卡和可见产物 | 玩具数据和示例阈值不能直接硬编码到心衰/MIMIC |
| qiaomu-meta-skill | [GitHub](https://github.com/joeseesun/qiaomu-meta-skill) | 手艺 | 将 Skill 做成可发现、可验证、可维护的包 | 保留 root-only、触发评估、Skill IR 和证据边界 | 不把打磨规则堆进 TTE 路由正文 |
| Anthropic skill-creator | [skills.sh](https://skills.sh/anthropics/skills/skill-creator) | 手艺 | 用清晰的 Skill 骨架和验证方式降低安装摩擦 | 首屏定位、示例和可复现验证 | 不改变本项目的 TTE 专业边界 |

补充的间接与手艺同行包括 [Tessl performing-causal-analysis](https://tessl.io/registry/skills/github/foryourhealth111-pixel/Vibe-Skills/performing-causal-analysis)、
[Tessl confounder-and-bias-control-planner](https://tessl.io/registry/skills/github/aipoch/medical-research-skills/confounder-and-bias-control-planner)、
[Tessl hypothesis-generation](https://tessl.io/registry/skills/github/K-Dense-AI/scientific-agent-skills/hypothesis-generation)、
[ClawHub Scholar Research](https://clawhub.ai/jcheng67/skills/scholar-research) 和
[ClawHub Skill Test](https://clawhub.ai/fwwdn/skills/skills-test)。它们共同提示：研究设计、混杂审计、文献检索和 Skill 评估应有明确交接，不应把泛化的 causal 关键词直接映射为全部 TTE 专业 Skill。

## 3. 生态位判断

纵向结论：0.3.0 已从八个并列入口上升为一个带 discovery lane 的本地路由器；文献检索仍由支持 Skill 执行，主路由只记录已验证来源和证据缺口。

横向结论：方法同行的共同立足点是先定义临床决策、estimand 和数据映射，再选择统计估计；优秀 Skill 的共同手艺是首屏说明价值、给出可见产物、把验证留在包内。

交叉洞察：真正应抢的生态位不是“自动替用户选择一个模型”，而是“把文献证据、临床决策、estimand、数据可支持性和 TTE Skill 串成一张可审计的研究设计路线图”。

一句话新定位：**daxuan-tte-router 将临床选题和文献反思转译为可验证的 TTE 协议、识别假设与统计设计，再路由到最小的专业 Skill 组合。**

## 4. 过尺结果（活体检查 + 质量评分）

### 活体与实测证据

本小节的基线记录对应 0.2.0；0.3.0 的新增实测见本节后面的“0.3.0 实施后实测”。

- `check-skill-repo.sh`：PASS 8 项，WARN 5 项，FAIL 0 项。WARN 为缺少 examples、LICENSE、市场清单、demo GIF/视频和 skills.sh 徽章。
- 单元测试：6 项通过，覆盖心衰设计、持续策略、冻结协议估计、IPW/共同支持审查、普通文本排除和英文词边界。
- 触发评估：10/10 通过，误触发 0，漏触发 0。
- Skill 包验证：`ok: true`，根 `SKILL.md`、接口、manifest 和 Skill IR 一致。
- 路由干跑发现的真实边界：选题/研究空白、sequential trial + cloning、统计方法选择没有进入专门意图；单独出现“因果推断”会被当作 TTE 设计；“协议已冻结 + per-protocol effect”若未写 `tte-estimate` 可能不进估计路由。
- 活体证据缺口：没有 CI、公开仓库、干净外部安装、真实心衰 cohort 回放和展示 GIF；因此不能把当前路由准确性外推到真实临床请求分布。

### 九维评分（0.2.0 冻结基线）

| 维度 | 权重 | 得分 | 主要证据 | 最大短板 | 优先级 |
|---|---:|---:|---|---|---|
| Frontmatter 与触发条件 | 7 | 6 | description 可触发，触发评估 10/10 | 未覆盖选题/文献反思/estimand 触发词 | P1 |
| 工作流清晰度 | 12 | 8 | 八阶段顺序与阶段闸门清楚 | 没有 question discovery → protocol 的前置链 | P0 |
| 失败模式编码 | 12 | 6 | 有 T0、未来信息、估计前置条件 | 没有弱信号、冲突意图、cloning/sequential 的规则 | P0 |
| 检查点设计 | 6 | 5 | route card、stop condition、run status | 未强制记录 ICE、假设和 data support | P1 |
| 可执行具体性 | 17 | 13 | 可运行 route_tte.py，路由顺序明确 | 文献检索和统计方法选择未形成交付物 | P0 |
| 资源整合度 | 4 | 3 | references、scripts、tests、reports 齐全 | 没有证据矩阵/estimand card 模板 | P1 |
| 整体架构 | 12 | 8 | 根 Skill + 八个 specialist + 适配器 | 研究设计与 TTE 执行层尚未分层 | P0 |
| 实测表现 | 23 | 17 | 6 个单测、10 个触发例、结构验证通过 | 无真实 cohort 回放和外部 clean install | P1 |
| 反例与黑名单 | 7 | 4 | 普通文本和词边界有负测例 | 缺“仅描述性研究”“普通因果问题”“未来信息/动态策略不支持”等测试矩阵 | P1 |
| **总分** | **100** | **70** |  |  |  |

### 0.3.0 实施后实测

在保持八个 TTE specialist 不变的前提下，0.3.0 增加了 discovery lane、supporting skills、evidence tasks、
estimand/design card、心衰 data-support 模板和 11 条路由单元测试。当前实测评分为 **86/100**：
结构校验 `ok: true`，触发评估 14/14 通过，路由单元测试 11/11 通过；仍缺真实心衰 cohort 回放、外部
clean install、CI 和 demo GIF，因此实测分不等同于临床有效性或公共生态质量。

## 5. 差距清单（0.2.0 基线；0.3.0 实施结果见 8.1）

### P0：不补就无法准确支持当前目标

- 增加 `intent` 层，至少区分 `question_discovery`、`protocol_design`、`emulation`、`analysis`、`checking`、`reporting`。
- 在路由卡中强制记录 `clinical_decision`、estimand 五属性、`intercurrent_events`、`identifying_assumptions`、`data_support` 和 `literature_evidence`。
- 将“文献反思 → 候选科学问题 → estimand → TTE 路由”写成有闸门的顺序；没有人群、临床动作、结局、时间范围和数据可支持性时不得进入估计。
- 将“因果推断”降为弱信号，要求同时出现观察性/目标试验语境和临床治疗决策，避免一般因果问题误入 TTE。
- 增加 sequential trial、cloning、动态策略、rescue/switch/死亡等 intercurrent event 的明确路由规则。

### P1：补上后明显提升研究质量和传播力

- 增加 `evidence_tasks`：每个新问题至少找一个直接临床 TTE 范例、一个方法学范例和一个反例/边界。
- 增加 `estimand-card` 和 `design-rationale` 模板，让统计方法由 estimand 和数据结构驱动。
- 为 MIMIC/eICU、INSPIRE/MOVER 和心衰两个适配器补充变量级 data-support 表。
- 用一组 12–20 条意图测试替代只有关键词触发的测试，记录期望路由、阻断项和人工覆盖规则。

### P2：锦上添花

- 加入可复现的 JSON/Markdown showcase，展示“输入临床问题 → 研究设计卡 → Skill 路由卡”。
- 增加 MIT LICENSE、市场元数据和一个不含隐私的 demo GIF/静态截图。
- 增加回炉日志，记录上游 TTE_CC、TARGET 和 E9(R1) 规则变更。

### 与同行相比最缺的 3 件事

1. 研究问题发现和文献证据没有进入路由主链。
2. estimand、intercurrent events、识别假设和数据支持没有成为硬字段。
3. 没有真实临床请求回放和可见的研究设计产物。

### 最有机会打穿的 3 件事

1. 心衰临床决策与两个不同 T0 的适配器。
2. 将 TTE 方法学来源转化为可执行的阶段闸门。
3. 用 route card 把科学问题、统计方案、数据缺口和下一步交接放在同一张卡上。

## 6. 三个打磨方向

### 方案 A：细修——提高现有八 Skill 的路由准确性

- 新定位：关键词初筛器升级为意图分类器。
- 改动范围：只改 `route_tte.py`、测试矩阵、`SKILL.md` 路由规则和 route card 字段。
- 优点：风险最低，保持当前八个 Skill 体系和安装方式。
- 风险：只能减少误路由，不能真正完成文献反思和科学问题设计。
- 适合条件：先需要稳定执行现有 TTE_CC 代码。

### 方案 B：精雕——增加证据约束的研究设计入口（推荐）

- 新定位：从“Skill 路由器”升级为“临床问题 → 文献反思 → estimand → TTE 路由器”。
- 改动范围：新增 question-discovery/literature-reflection 意图、文献证据任务、estimand card、统计方法门和研究设计 rationale；保留八个 TTE specialist，不把文献 Skill 混成 TTE specialist。
- 优点：最贴合当前用户目标，能直接支持心衰选题和高水平论文设计。
- 风险：需要维护文献来源、处理检索证据边界，并增加一轮真实问题回放。
- 适合条件：希望把公共数据库分析变成可解释、可发表的研究方案。

### 方案 C：开套件——拆成研究设计、TTE 路由、统计执行三个入口

- 新定位：`daxuan-research-design` → `daxuan-tte-router` → `daxuan-causal-analysis`。
- 改动范围：新增多个可独立安装的 Skill 和共享证据协议。
- 优点：边界最清晰，适合未来团队协作和公共发布。
- 风险：安装和维护成本增加，容易形成重复路由；需要用户明确授权改变现有架构。
- 适合条件：准备把方法体系作为长期公共工具包发布。

推荐选择：**方案 B**。它在保留现有八个 TTE Skill 的前提下，补上当前最影响科学价值的缺口。本轮已按此方向实施。

## 7. 候选改写方案

本轮只刨：**增加“意图层 + 证据约束设计门”，不改变八个 TTE specialist 的实现。**

### 建议文件变更

| 文件 | 操作 | 原因 |
|---|---|---|
| `SKILL.md` | 增加 intent 路由和证据任务 | 先判断用户是在选题、设计、估计还是报告 |
| `scripts/route_tte.py` | 增加 intent、弱信号和 cloning/sequential 规则 | 减少误路由和漏路由 |
| `references/route-card.md` | 增加 estimand/ICE/假设/data support 字段 | 让科学设计能交接和审计 |
| `references/design-rationale.md` | 新增模板 | 固化文献如何改变问题和方法 |
| `references/estimand-card.md` | 新增模板 | 防止模型名称先于临床问题出现 |
| `tests/test_route_tte.py` | 扩展为意图测试矩阵 | 验证选题、文献、动态策略、非 TTE 因果问题等边界 |
| `README.md` | 增加一条从问题到研究设计卡的 showcase | 提供可见产物和安装理由 |

### 可直接替换的核心片段

```text
先判定 intent，再选择 specialist：

question_discovery：用户提出选题、研究空白、文献反思、临床意义或研究设计比较。
先调用研究问题选择与文献检索入口，交付“临床决策 → 证据缺口 → 候选干预 → 候选 estimand”。

protocol_design：临床决策已明确，但 population、action A/B、outcome、horizon、T0、ICE 或
estimand 尚未冻结。调用 target-trial，并按需要加入 time-zero、sustained-strategies、
competing-events。

emulation：协议已冻结，仍需处理混杂、时变策略、竞争事件、sequential trial 或 cloning。
调用 emulate-randomization、sustained-strategies、competing-events 和相应的 TTE_CC 工具。

analysis/checking/reporting：只有在协议、estimand 和变量级 data map 足够明确后，才进入
估计、检查或报告。

统计方法只能在 estimand 和数据支持性明确后选择。每个方法必须写出它回答的 estimand、
识别假设、数据要求和不适用条件。
```

```text
研究设计卡必须包含：
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

## 8. README 与 Showcase 升级建议

首屏一句话改为：

> 把“我想研究什么”变成一张有文献依据、estimand、数据缺口和 TTE Skill 交接的研究设计路线图。

首个示例使用心衰肾功能恶化后的利尿策略，展示三段固定输出：

1. 文献反思：为什么维持/减量是临床决策，已有研究如何定义 WRF、出院和死亡；
2. 研究设计卡：两个策略、T0、24 小时窗口、intercurrent events、识别假设；
3. 路由卡：`target-trial → time-zero → sustained-strategies → emulate-randomization → competing-events`。

本轮已加入 `examples/heart-failure-question-discovery.json` 和 `examples/frozen-protocol-estimate.json`，
作为可重复的非临床结果展示。

## 8.1 实施结果

- 根 Skill 升级到 0.3.0，加入 `question_discovery`、`protocol_design`、`emulation`、`analysis`、`checking`、`reporting` 意图层。
- `route_tte.py` 新增 supporting skills、evidence tasks、evidence gaps、design card、estimand/ICE 闸门和普通因果问题的降级规则。
- 新增 `references/estimand-card.md`、`references/design-rationale.md`、`references/heart-failure-data-support.md` 和 `references/supporting-skills.md`。
- 新增 11 条单元测试、14 条触发案例和两个可重复 JSON 示例。
- 0.3.0 不复制或改变 TTE_CC 八个 specialist 的实现，也没有运行临床估计。

## 9. 执行计划

### 24 小时内必须完成

- [x] 用户选择方案 B。
- [x] 固定意图测试和预期路由。
- [x] 将 TARGET 与 ICH E9(R1) 的字段转成 route card 闸门。

### 3 天内完成

- [x] 增加 question-discovery/literature-reflection 路由。
- [x] 增加 estimand card、design rationale 和心衰 data-support 模板。
- [ ] 用真实的心衰问题回放改动前后路由差异。

### 7 天内完成

- [x] 形成一个不含隐私的 JSON/Markdown showcase。
- [ ] 补 LICENSE、市场元数据和回炉清单。
- [x] 冻结 0.3.0 版本候选并重新运行验证门。

### 本轮不做

- 不改变八个 TTE specialist 的实现。
- 不自动替用户确定 WRF 阈值、剂量比例、治疗窗口或救援规则。
- 不把文献检索结果写成“全球首次”或保证目标期刊接受。

## 10. 出师证书

```text
┌────────────────────────────────────────┐
│  出师证书 · 鲁班工坊                   │
│                                        │
│  作品：daxuan-tte-router               │
│  过尺：0.2.0 基线 70/100 → 0.3.0 实测 86/100 │
│  定位：证据约束的 TTE 研究设计路由器     │
│  绝活：临床决策—estimand—数据—Skill交接 │
│  下一步：真实心衰回放、CI 与发布元数据     │
│                                        │
│  验收师傅：鲁班                         │
└────────────────────────────────────────┘
```

## 11. 回炉清单

- 持续观察 [TTE_CC](https://github.com/jacobjameson/TTE_CC) 的 specialist 边界和 helper 变化。
- 持续观察 [TARGET Statement](https://www.bmj.com/content/390/bmj-2025-087179) 的解释与实施资料。
- 持续观察 [ICH E9(R1)](https://www.ema.europa.eu/en/scientific-guidelines/ich-e9-statistical-principles-clinical-trials) 对 estimand 与 sensitivity 的应用。
- 每次上游方法或项目数据库语义变化后，更新路由规则、证据来源和意图测试。
- 下一轮入口：先验证“选题/文献反思/统计设计”是否能正确停在 discovery 或 design gate，再扩展更多数据库适配器。

## 12. 下一轮需要用户确认的问题

1. 首个真实回放是否优先使用“心衰肾功能恶化后的利尿维持 vs 减量”问题？
2. 文献检索是否默认使用 PubMed 与官方指南，并把检索式、日期、纳入文献和证据边界写入 `design-rationale`？
3. 下一轮是否补齐 LICENSE、市场元数据与 CI，同时保持 0.3.0 的路由行为不变？

## 13. 附录：参考来源

- [Hernán & Robins, AJE 2016](https://academic.oup.com/aje/article/183/8/758/1739860)
- [BMJ Target Trial 2022](https://www.bmj.com/content/378/bmj-2022-071108)
- [Starting Right, BMJ 2025/2026](https://www.bmj.com/content/392/bmj-2025-084909)
- [TARGET Statement, BMJ 2025](https://www.bmj.com/content/390/bmj-2025-087179)
- [ICH E9(R1), EMA](https://www.ema.europa.eu/en/scientific-guidelines/ich-e9-statistical-principles-clinical-trials)
- [Dynamic treatment strategies primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC5710813/)
- [TTE_CC](https://github.com/jacobjameson/TTE_CC)
- [auto-inspire-skill](https://github.com/joeseesun/auto-inspire-skill)
