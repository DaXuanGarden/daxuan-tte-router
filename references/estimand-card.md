# Estimand card 模板

这张卡把临床问题固定为可审计的 estimand。先填问题和 intercurrent events，再选择 estimator。

```yaml
clinical_decision: "谁在什么时点需要在 A 与 B 之间做什么决定？"
population:
  inclusion:
  exclusion:
  baseline_time:
treatment:
  strategy_A:
  strategy_B:
  assignment_rule:
endpoint:
  outcome:
  ascertainment:
  follow_up_start:
  follow_up_end:
summary_measure:
  scale: risk_difference | risk_ratio | survival_difference | hazard_ratio | other
  time_horizon:
intercurrent_events:
  death: competing_event | composite | censoring | hypothetical | other
  discharge: competing_event | censoring | other
  rescue_or_switching: treatment_policy | while_on_treatment | censoring | other
  loss_to_follow_up: censoring | hypothetical | other
estimand_status: draft | frozen | blocked
identifying_assumptions:
  exchangeability: data_support_and_gap
  positivity: data_support_and_gap
  consistency: data_support_and_gap
  well_defined_intervention: data_support_and_gap
analysis_plan:
  estimator:
  time_scale:
  confounding_control:
  missing_data:
  precision:
  sensitivity_analyses:
data_support:
  treatment_administration:
  outcome_capture:
  covariate_timing:
  longitudinal_measurement:
  competing_event_capture:
literature_evidence:
  direct_clinical_example:
  methods_example:
  boundary_or_counterexample:
next_handoff:
```

`estimand_status: frozen` 只有在 A/B 策略、结局、时间范围和 intercurrent-event 策略都已经明确，并且变量级
data map 没有阻断缺口时使用。统计方法必须解释为何回答这张卡中的 summary measure。
