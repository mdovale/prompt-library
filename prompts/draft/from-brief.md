---
id: draft.from-brief
title: Draft from a brief
status: active
use_when: You have a brief and need a first draft in a named format
inputs: [brief, format]
output: A draft in the requested format, with assumptions listed first
tags: [draft, writing]
includes:
  - fragments/constraint-stay-in-scope.md
---

## Use

Replace `{{brief}}` and `{{format}}`. Name the format, such as "a short design note" or "a PR description".

## Prompt

Write a first draft from the brief. Match the format. Keep every claim inside the brief.

{{include:fragments/constraint-stay-in-scope.md}}

Start with an Assumptions section only for gaps that change the draft. Then write the draft.

Format: {{format}}

Brief:

{{brief}}

## Notes

Works when the format is named. A short brief produces a longer assumptions list.
