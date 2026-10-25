# Luban A：状态机与证据账本可信性

审阅日期：2026-10-25  
范围：阶段跳转、pilot 门禁、证据账本聚合状态和运行状态可分享性。

## 交付

- `record-pilot` 现在只接受 `current_phase == pilot`，不能从 intake 或协议草案直接进入 execution。
- evidence ledger 只有在每条记录均为 `verified` 时才标记为 `verified`；混合状态保持 `in_progress`。
- 运行状态保留 Skill 的发现状态，但清除本机 `path` 和 `searched_roots`，并标记为 `local-runtime-only`。
- 增加阶段门、混合账本和路径脱敏测试；版本更新为 0.6.0。

## 验证

- 22/22 路由与 pipeline 单元测试通过。
- A 方向不改变八个 TTE specialist 的路由规则。
- 共享状态不再包含本机 Skill 解析路径；实际解析仍由本地 resolver 命令提供。
