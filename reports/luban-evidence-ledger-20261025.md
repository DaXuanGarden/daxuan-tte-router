# Luban B：证据账本与 TTE 术语规范

审阅日期：2026-10-25  
范围：`daxuan-tte-router` 的证据交接、TTE 术语、运行产物和发布验证。

## 交付

- 新增 `evidence-ledger.json`，为每条影响临床问题或 estimand 的主张记录原文片段、来源 URL、来源日期、独立性说明和验证状态。
- 新增 `record-evidence` 命令；文献阶段没有来源到主张的记录时，`complete-phase --phase literature` 会保持在当前阶段。
- 将 `evidence-ledger.json` 纳入 route card 的 pipeline handoff artifacts、README、Skill 正文和示例运行。
- 统一面向用户的术语为 **TTE**；保留 `target-trial`、`tte-estimate` 等上游精确标识符，并新增命名约定说明。
- 将包版本更新为 0.5.0，刷新 Skill IR 和创建交接记录。

## 验证

- 19/19 路由与 pipeline 单元测试通过。
- 14/14 触发评估通过。
- qiaomu Skill 结构验证通过，无警告。
- 运行示例返回 `evidence-ledger.json`，命令帮助包含 `record-evidence`。
- 公共包文件保持项目相对路径；证据账本仍只记录来源和主张，不声称已完成文献检索或临床估计。

## 边界

本轮只补强证据交接和术语一致性，不改变八个 TTE specialist 的路由规则，也不接入数据库查询。下一轮再根据真实研究问题回放决定是否增加自动 Skill dispatch 或数据库 pilot adapter。
