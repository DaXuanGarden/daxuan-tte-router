# 可恢复运行示例

```bash
python3 scripts/pipeline.py init \
  --text "先查心衰肾功能恶化后的利尿策略文献，再决定是否进入 TTE 协议" \
  --workdir ./tte-runs/heart-failure-renal-signal

# 先写入并交接 intake 产物。
cat > ./tte-runs/heart-failure-renal-signal/intake.md <<'EOF'
临床决策：在预先定义的肾功能恶化信号后维持或降低利尿强度。
EOF
python3 scripts/pipeline.py complete-phase \
  --workdir ./tte-runs/heart-failure-renal-signal \
  --phase intake \
  --artifact intake.md \
  --notes "临床决策已记录"

# 完成真实检索后，先把 evidence-map.json 的 status 改为 completed 并填入来源，
# 再用 complete-phase 记录 literature 阶段的交接。
python3 scripts/pipeline.py complete-phase \
  --workdir ./tte-runs/heart-failure-renal-signal \
  --phase literature \
  --artifact evidence-map.json \
  --notes "检索式、数据库、日期和核验来源已记录"

python3 scripts/pipeline.py record-pilot \
  --workdir ./tte-runs/heart-failure-renal-signal \
  --decision proceed \
  --notes "队列、暴露、结局、时间零点和重叠性均已检查"

python3 scripts/pipeline.py feedback \
  --workdir ./tte-runs/heart-failure-renal-signal \
  --classification assumption_violation \
  --notes "权重诊断提示共同支持不足" \
  --next-action "返回 data_support 阶段并重审暴露定义"
```

初始化和 `record-pilot` 都只记录研究状态；只有明确运行相应分析 Skill 后，才可以把估计或诊断写成已完成。
