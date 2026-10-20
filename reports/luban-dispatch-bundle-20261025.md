# Luban B：TTE run bundle 与有序交接

审阅日期：2026-10-25  
范围：specialist 选择后的可见交接、运行包和执行边界。

## 交付

- 新增 `pipeline.py dispatch` 命令。
- 为每个已选 TTE specialist 和支持 Skill 生成有序 handoff 文件。
- 新增 `dispatch-manifest.json`，记录意图、阶段、解析状态、顺序、缺失 required Skill 和下一步动作。
- 新增 `run-bundle.md`，把 route card、design card、evidence ledger、pilot gate 和 handoff 关系集中展示。
- 明确 `handoff-only` 边界：dispatch 只生成可审计交接，不执行数据库查询、估计或临床报告。

## 验证

- 24/24 路由与 pipeline 单元测试通过。
- 14/14 触发评估通过。
- required specialist 缺失时 dispatch 显示 `blocked`，可用时显示 `ready`。
- run bundle 不包含机器绝对路径，也不复制 specialist 正文。
