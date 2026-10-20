# 路由示例

这些 JSON 是路由器的可重复示例输出，不是临床分析结果，也不代表文献检索已经完成。

- `heart-failure-question-discovery.json`：先进入文献/选题支持层，再交接 `target-trial`。
- `frozen-protocol-estimate.json`：协议冻结后进入 `tte-estimate`，并保留检查闸门。
- `resumable-run.md`：创建运行目录、记录 pilot 门禁和反馈的最小闭环。

重新生成：

```bash
python3 scripts/route_tte.py --text "<request>" --json > examples/<name>.json
```
