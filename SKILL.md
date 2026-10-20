---
name: daxuan-tte-router
description: |
  Route target trial emulation (TTE) work through the installed TTE_CC toolkit. Use when a user wants to
  formulate, sharpen, audit/审核, analyze, check, or report an observational target trial, or select a
  cardiovascular research question from literature before TTE design, especially for
  cardiovascular, heart failure, ICU, MIMIC/eICU, INSPIRE, or MOVER studies. Select the smallest useful
  set of the eight TTE_CC skills, preserve the target-trial protocol before estimation, and use the
  project's clinical and data-semantic rules, including confounding/混杂 and positivity/共同支持. This skill routes work; it does not replace the specialist
  skills or turn teaching examples into executed clinical analyses.
metadata:
  version: "0.3.0"
  owner: "20260907_Clinical_Database"
  upstream: "TTE_CC by Jacob Jameson"
---

# Daxuan TTE Router

Use this package as the single entry point for the local TTE workflow. It routes a request to the existing
TTE_CC specialist skills and keeps the clinical question, estimand, data mapping, and analysis stage aligned.
The router is a policy layer: it decides what should be read next, while the selected specialist skill
defines how that stage is carried out.

The workflow has two connected lanes:

```text
question discovery → evidence reflection → estimand/data-support gate → TTE protocol → emulation
→ estimate → check → report
```

The discovery lane improves the scientific question; the TTE lane freezes and emulates the causal protocol.
Do not let a literature search, model name, or teaching example silently become a clinical conclusion.

## First classify the intent

- **`question_discovery`**: the user asks for a topic, research gap, clinical significance, literature
  reflection, design comparison, or statistical-method choice. Route to the supporting research skills first,
  and return evidence tasks plus a design card. Do not freeze an estimand from keywords alone.
- **`protocol_design`**: the clinical decision is identifiable but population, A/B strategies, outcome,
  horizon, T0, intercurrent events, or estimand remain open. Route to `target-trial` and the TTE design
  specialists that the decision requires.
- **`emulation`**: the protocol is sufficiently specified and the work concerns confounding, dynamic or
  sustained strategies, sequential trials, cloning, censoring, or competing events.
- **`analysis`**, **`checking`**, and **`reporting`**: use the corresponding TTE specialist only after the
  preceding gate and data support are explicit.

When `question_discovery` is selected, use only the supporting skills listed in
`references/supporting-skills.md` and resolve their actual local entries before reading them. They cover
problem choice, topic/gap mapping, verified literature retrieval, causal framing, statistical method choice,
and survival/competing-risks teaching.

Use only the supporting skills required by the request. They advise the design lane; they do not replace
the eight TTE_CC specialists or freeze the protocol.

## Route by the user's job

1. **Choose a topic, identify a gap, compare designs, or reflect on literature** → use the discovery lane,
   then read `target-trial` only after a clinical decision and candidate estimand are stated.
2. **Sharpen a causal question or write the protocol** → read `target-trial` first.
3. **Define or audit T0, repeated eligibility, immortal time, sequential trials, or cloning** → add `time-zero`.
4. **Compare treatment duration, continuation, stopping, dose, timing, or repeated decisions** → add
   `sustained-strategies`; use `target-trial` and `time-zero` when their decisions are not already fixed.
5. **Identify confounders, choose standardization/IP weighting/matching, or judge exchangeability** → add
   `emulate-randomization`.
6. **Handle death, discharge, RRT, loss to follow-up, rescue, switching, or an undefined post-death measurement** → add
   `competing-events` before selecting an estimator.
7. **Generate or run an estimate after the protocol and data mapping are frozen** → read `tte-estimate`.
8. **Assess overlap, weights, balance, negative controls, or a related randomized benchmark** → read
   `check-emulation`.
9. **Draft the protocol, methods, flow, or results report after analysis** → read `tte-report`.

For an end-to-end request, use this order:

```text
question discovery → target-trial → time-zero → (sustained-strategies and/or emulate-randomization and/or competing-events)
→ tte-estimate → check-emulation → tte-report
```

Select only the stages needed for the request. If the user asks for a design or audit, do not route to
estimation merely because an estimator is available. If the user asks for an estimate without a frozen
protocol, route the missing design stages first and state the gate.

Read the selected specialist `SKILL.md` from `/home/daxuan/.codex/skills/<name>/SKILL.md`. The shared
TTE_CC toolkit and references are at `/home/daxuan/.tte_cc`; use `$TTE_CC_HOME` when the project sets it.
If a specialist or toolkit is unavailable, state the missing evidence and continue only with the stage that
can be completed faithfully.

## Deterministic route card

When the request is ambiguous, or when a reproducible routing record is useful, run:

```bash
python3 /home/daxuan/20260907_Clinical_Database/skills/daxuan-tte-router/scripts/route_tte.py \
  --text "<the user's TTE request>" --json
```

The script is a keyword-based suggestion, not a clinical decision. Resolve its suggestions against the
question, treatment decision, data semantics, and the specialist instructions. Return this route card in
the response:

```text
intent: question_discovery | protocol_design | emulation | analysis | checking | reporting
stage: discovery | design | emulation | analysis | checking | reporting
selected: <smallest specialist set, in execution order>
supporting_skills: <only the literature, causal, statistical, or survival skills needed before/alongside TTE>
why: <one clinical or methodological reason per selected skill>
evidence_tasks: <direct example, methods example, boundary/counterexample when discovery is active>
evidence_sources: <verified sources actually read; empty until retrieval runs>
evidence_gaps: <unverified novelty, missing data semantics, or unsupported assumptions>
design_card: <clinical decision, estimand fields, intercurrent events, assumptions, data support>
prerequisites: <protocol, T0, data mapping, or other unmet gate>
deliverable: <protocol, data map, estimate, diagnostic, or report artifact>
stop condition: <what must be true before the next stage>
run status: suggested | consulted | drafted | executed | checked
```

The route card prevents a draft protocol from being described as an executed analysis and makes the next
handoff explicit. The script reports `selected: []` for ordinary writing, translation, or descriptive work
without a causal TTE request. It reports supporting research skills separately from the eight TTE specialists.

## Stage gates

- Before `tte-estimate`, freeze population, treatment strategies, assignment/T0, follow-up, outcome,
  estimand, summary measure, intercurrent-event strategy, analysis time scale, and a variable-level data map. Mark unresolved clinical thresholds and
  missing measurements as gaps; do not infer them from the outcome.
- Before `target-trial` is frozen after discovery, record one direct clinical example, one methods example,
  and one boundary/counterexample. Record the search database, query, date, and verified citation; an empty
  search result is not proof of novelty.
- For every estimand, record population, treatment, endpoint, summary measure, and the strategy for each
  intercurrent event. Record exchangeability, positivity, consistency, and well-defined intervention as
  assumptions with their data support status.
- If a proposed intervention is dynamic or sustained, confirm longitudinal treatment, confounder, outcome,
  rescue, switching, and censoring measurements before selecting g-methods or cloning.
- Before `check-emulation`, an estimate or an explicitly defined emulation object must exist. A checklist
  without an estimand, treatment assignment, and analysis object cannot establish validity.
- Before `tte-report`, identify which protocol, estimates, diagnostics, and figures actually exist. A report
  can document a protocol-only study, but it must not imply results that were not run.
- If a request changes treatment after a new laboratory or physiologic signal, treat it as a new decision
  point. Do not classify exposure using future treatment, survival, discharge, or a completed follow-up
  measurement.

## Routing rules for this project

- Start from the clinical decision: population, action A versus B, outcome, horizon, and why the choice
  matters. Do not start by choosing a model or a fashionable exposure.
- Specify all eight target-trial elements before estimation. Every protocol item must map to a measured
  variable, time, or an explicitly documented data gap.
- Make eligibility, strategy assignment, and follow-up begin at the same T0. Do not classify treatment by
  future receipt, survival, eventual discharge, or a completed follow-up measurement.
- Use causal language for the target trial and estimand; report observed estimates without causal wording
  until the identifying assumptions and emulation checks have been addressed.
- Treat MIMIC/eICU as acute-care data and INSPIRE/MOVER as perioperative data. Do not call a different
  population an external validation merely because a variable has the same name.
- Confirm the data semantics of actual treatment administration, laboratory availability, measurement time,
  discharge, and mortality before promising a strategy or endpoint. Absence of a measurement is not a
  normal value.
- Prefer one primary clinical question, one primary estimand, and a small number of prespecified modifiers.
  Do not add methods merely to make a paper appear sophisticated.
- TTE_CC teaching data and helper examples are methodological templates. They are not cardiovascular
  evidence and do not substitute for a cohort-specific treatment and outcome mapping.

## Heart-failure adapters

Keep these two questions separate because they define different treatment decisions and T0s:

For either question, begin with `question_discovery` when the clinical gap or comparison has not been
established. Record the direct clinical example, methods example, boundary/counterexample, estimand card and
the variable-level checks in:

`/home/daxuan/20260907_Clinical_Database/skills/daxuan-tte-router/references/heart-failure-data-support.md`

### Initiation timing

Among eligible adults with acute heart failure, what is the effect of initiating intravenous loop diuretics
within a prespecified window versus later initiation on in-hospital outcomes? This question routes through
`target-trial`, `time-zero`, `emulate-randomization`, and `competing-events`; add `tte-estimate` only after
the initiation window and eligibility are observable in the data.

The current local draft is:

`/home/daxuan/20260907_Clinical_Database/target_trial_protocol.md`

### Response to worsening renal function while treating congestion

Among adults with acute heart failure who are still congested, already receiving intravenous loop diuretics,
and newly meet a prespecified worsening-renal-function signal, what is the effect of adhering to a 24-hour
strategy to maintain versus reduce diuretic intensity on in-hospital mortality and renal outcomes? This
question routes through `target-trial`, `time-zero`, `sustained-strategies`, `emulate-randomization`, and
`competing-events`; add `tte-estimate` only after phenotype, dose/action mapping, strategy support, and
endpoint coverage are documented.

The current local draft is:

`/home/daxuan/20260907_Clinical_Database/MIMIC_elCU数据库/literature/心血管TTE选题与设计_20261020/心衰肾功能恶化_TTE草案/target_trial_protocol.md`

Neither adapter freezes a dose percentage, decision grid, renal threshold, or rescue rule. Those are
clinical and data decisions to settle before effect estimation. A +2 L net-fluid trigger alone does not
establish acute heart failure or pulmonary congestion.

## Output contract

Return:

1. the route card with the intent, TTE specialists, supporting skills, evidence tasks, and why each is needed;
2. the current stage and the next handoff;
3. the design card or protocol/data artifact produced or updated;
4. concrete data gaps, unsupported assumptions, or validity threats that change the next action;
5. whether any literature retrieval, estimation, diagnostic check, or report section was actually run.

Do not claim that a specialist was executed when only its instructions were consulted. Do not report a
clinical effect before an analysis has actually been run on the mapped cohort.

## Exclusions

This router does not create a new causal estimator, silently repair cohort code, choose a clinical threshold
from the outcome, guarantee novelty or journal acceptance, or publish a skill/package. Use the user's
explicit request for code changes, publication, or external communication as a separate authorization.

Copyright (c) 向阳乔木  
X: https://x.com/vista8  
GitHub: https://github.com/joeseesun/
