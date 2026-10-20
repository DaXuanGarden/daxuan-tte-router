# Creation Handoff

## Result

- Skill: `daxuan-tte-router` 0.3.0
- Job: turn a clinical research question into an evidence-aware estimand, data-support gate, and minimal target-trial-emulation specialist route while preserving the project clinical and data-semantic rules.
- Local path: `/home/daxuan/20260907_Clinical_Database/skills/daxuan-tte-router`
- Installed discovery link: `/home/daxuan/.codex/skills/daxuan-tte-router`
- Publication: not requested; local package only.

## Reference skills studied

- `TTE_CC/target-trial`, `time-zero`, `sustained-strategies`, `emulate-randomization`, `competing-events`, `tte-estimate`, `check-emulation`, and `tte-report`: supplied the eight-stage boundaries and specialist handoffs.
- `qiaomu-meta-skill`: supplied root isolation, trigger evaluation, Skill IR, evidence-bound claims, and package gates.
- BMJ TARGET Statement: supplied the reporting emphasis on protocol, estimand, data mapping and precision.
- ICH E9(R1), BMJ target-trial and dynamic-strategy guidance: supplied estimand, intercurrent-event, time-zero, sequential/cloning, time-varying confounding and competing-event gates.

## Absorbed and rejected

- **Keep:** protocol-first workflow, time-zero alignment, sustained-strategy routing, competing-event estimands, person-level bootstrap, and post-analysis checks.
- **Adapt:** Chinese-first routing, local paths, four-database distinctions, and the heart-failure clinical adapter.
- **Reject:** copying specialist bodies into a large root prompt, automatic execution of all stages, and clinical claims based on synthetic examples.
- **Invent:** a discovery lane, evidence tasks, estimand/design cards, and a single local route entry plus a project-specific handoff for the heart-failure renal-function question.

## Advantages and evidence

- **design advantage:** explicit smallest-useful-route table in `SKILL.md` and `references/routing-map.md`.
- **design advantage:** project-specific heart-failure adapter connects the router to the current protocol without changing TTE_CC specialists.
- **design advantage:** deterministic `scripts/route_tte.py` produces a route card suggestion and exposes stage prerequisites without pretending to execute an analysis.
- **design advantage:** version 0.3.0 separates supporting research skills from the eight TTE specialists and records evidence gaps before protocol freeze.
- **hypothesis:** the route should reduce repeated manual selection; provider-backed and human-comparison evidence remains missing.

## Verification and limits

The package is intended for local reuse. Validation, trigger evaluation, route unit tests and Skill IR are generated alongside
this handoff. The skills.sh target-trial catalog query timed out in prior-art discovery, so catalog coverage
is incomplete. No publication, remote repository, clean external install, or clinical treatment estimate is
claimed by this package.
