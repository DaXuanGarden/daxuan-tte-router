# Prior-Art Research

- Researched at: 2026-10-20
- Purpose: create a local TTE routing skill for the installed TTE_CC specialist package.
- Catalogs attempted: skills.sh and SkillsMP through the bundled qiaomu-meta-skill runner.
- Rating evidence: unavailable; catalog metrics were not treated as ratings.

## Sources inspected

| Candidate/source | Relevance | Concrete lesson | Decision |
|---|---|---|---|
| [TTE_CC](https://github.com/jacobjameson/TTE_CC) | Direct source toolkit; eight specialist skills and transparent R helpers | Separate protocol, time zero, sustained strategies, estimation, checks and reporting; require long person-time data | Keep and adapt as the routed specialist set |
| [TTE_CC README](https://github.com/jacobjameson/TTE_CC/blob/main/README.md) | Package-level workflow and data boundary | Two-step “ask then answer” model; synthetic teaching data must not be confused with clinical evidence | Keep, with project-specific data-semantic rules |
| [qiaomu-meta-skill](https://github.com/joeseesun/qiaomu-meta-skill) | Skill packaging and routing authority | One discoverable root, trigger cases, Skill IR, evidence-bound claims and proportional gates | Keep as the package authoring standard |
| BMJ TARGET Statement | Reporting analogue rather than a routing skill | Protocol, estimand, mapping, precision and sensitivity findings should be explicit | Adapt into the router output contract |

## Catalog result and missing evidence

The unified runner returned SkillsMP candidates for both intent queries and skills.sh results for the router
query. The skills.sh target-trial query timed out during this run; this is recorded as missing evidence. The
returned catalog records were not treated as proof of quality, and no unreviewed candidate code was executed.
No external candidate contributed a mechanism that was more relevant than the installed TTE_CC package.

## Keep / adapt / reject / invent

- **Keep:** TTE_CC's stage sequence and eight specialist boundaries.
- **Adapt:** route descriptions and output language to Chinese clinical research, MIMIC/eICU/INSPIRE/MOVER
  semantics, and the current heart-failure protocol.
- **Reject:** a large copied meta-prompt, automatic execution of every stage, generic model-first routing,
  and claims that a teaching helper is ready for any clinical cohort.
- **Invent:** a heart-failure adapter, explicit database-role separation, run-status contract, and a single
  local route entry for the eight installed skills.

## Evidence status

- Design advantage: the root package names the smallest route and hands off to the existing specialist skill.
- Design advantage: the heart-failure adapter keeps T0, treatment action, outcome and data semantics together.
- Hypothesis: a single route entry will reduce repeated manual skill selection; provider-backed and user
  comparison evidence is missing.
