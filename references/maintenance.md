# 维护规则

当 `/home/daxuan/.tte_cc` 的 specialist 入口、名称或顺序变化时，更新 `SKILL.md`、`references/route-card.md`
和 `scripts/route_tte.py` 的规则，并重新生成 `reports/skill-ir.json` 与 `reports/trigger-eval.json`。

当研究支持 Skill 的路径、名称或文献检索边界变化时，只更新 discovery lane 的支持表和测试，不把支持
Skill 复制进 TTE specialist 路由。真实检索后，把数据库、检索式、日期、来源和证据边界写入
`references/design-rationale.md` 对应的研究产物。

当本项目的数据库语义或心衰协议草案变化时，只更新对应的项目适配器和路由闸门；不要为了适配单个
研究增加新的 specialist 名称。每次修改路由规则，都要回放 question discovery、普通因果问题、动态策略/
cloning、冻结协议估计、竞争事件统计方法和普通文档六类边界。路由脚本只做可重复的初筛，临床问题、
协议和数据语义优先级更高。
