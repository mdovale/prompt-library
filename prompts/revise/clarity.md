---
id: revise.clarity
title: Revise for clarity
status: active
use_when: You have a draft and need it clearer and shorter without changing the claim
inputs: [draft]
output: The revised text, then a short list of what changed
tags: [revise, writing]
includes:
  - fragments/constraint-stay-in-scope.md
---

## Use

Replace `{{draft}}` with the text to revise.

## Prompt

Revise the draft so it is clearer and shorter. Preserve the claims, the audience, and any required terms.

{{include:fragments/constraint-stay-in-scope.md}}

Return the revised text, then a section called "What changed" with at most five bullets. Keep the explanation out of the revised text.

Draft:

{{draft}}

## Notes

Preserves the claim. For a new audience or a different stance, draft again instead of revising.
