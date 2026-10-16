---
id: review.diff
title: Diff review
status: active
use_when: You have a diff and need correctness, risk, and test gaps called out before merge
inputs: [diff]
output: Markdown findings with severity, location, and a concrete fix
tags: [review, code]
includes:
  - fragments/constraint-stay-in-scope.md
  - fragments/output-markdown-findings.md
---

## Use

Replace `{{diff}}` with the diff, or with the files and the intended behavior.

## Prompt

Review this diff for correctness, behavioral risk, and missing tests.

{{include:fragments/constraint-stay-in-scope.md}}

{{include:fragments/output-markdown-findings.md}}

Treat a missing test for a behavior change as a finding. Ignore style nits unless they hide a defect.

Diff:

{{diff}}

## Notes

Fits a focused diff. Ask for the intended behavior when the diff does not show it.
