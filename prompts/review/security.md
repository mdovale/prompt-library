---
id: review.security
title: Security review
status: active
use_when: You have a diff and need security findings before merge
inputs: [diff]
output: Markdown findings with severity, location, and a concrete fix
tags: [review, security]
includes:
  - fragments/constraint-stay-in-scope.md
  - fragments/output-markdown-findings.md
---

## Use

Replace `{{diff}}` with the diff.

## Prompt

Review this diff for security issues. Look for injection, authz gaps, secret exposure, unsafe deserialization, path traversal, and trust-boundary mistakes.

{{include:fragments/constraint-stay-in-scope.md}}

{{include:fragments/output-markdown-findings.md}}

Report issues this diff introduces or leaves in place. Keep the threat model inside what the diff shows.

Diff:

{{diff}}

## Notes

Fits application code in a diff. For infrastructure or cryptography design, include the surrounding config in the diff.
