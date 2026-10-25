# TTE naming conventions

Use **TTE** in prose, headings, descriptions, reports, examples, and user-facing output.

Keep these exact identifiers unchanged because they are installation or routing keys:

- package name: `daxuan-tte-router`
- upstream package: `TTE_CC`
- specialist identifiers: `target-trial`, `time-zero`, `sustained-strategies`, `emulate-randomization`,
  `competing-events`, `tte-estimate`, `check-emulation`, `tte-report`
- script and test filenames that already use lowercase `tte`

When a sentence contains both forms, use the display form outside code formatting and the exact identifier
inside backticks. For example: “运行 `tte-estimate` 完成 TTE 效应估计”。
