---
id: debug.failure
title: Diagnose a failure
status: active
use_when: You have an error, log, or failing output and need the most likely cause and the next check
inputs: [symptom, context]
output: Likely cause, what would disprove it, and the next check
tags: [debug]
includes:
  - fragments/constraint-stay-in-scope.md
---

## Use

Replace `{{symptom}}` with the error or failing output. Replace `{{context}}` with what changed, or "Unknown".

## Prompt

Diagnose the failure. Prefer the cause that fits the symptom with the fewest new assumptions.

{{include:fragments/constraint-stay-in-scope.md}}

## Likely cause

One paragraph.

## What would disprove it

One check or observation.

## Next check

The single next step. Include the command or the place to look when the context allows it.

Symptom:

{{symptom}}

Context:

{{context}}

## Notes

Works when the symptom includes the actual error text. "It doesn't work" with no output leaves the cause underdetermined.
