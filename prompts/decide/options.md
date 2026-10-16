---
id: decide.options
title: Choose an option
status: active
use_when: You have two or more options and need a recommendation against stated criteria
inputs: [decision, options, criteria]
output: A comparison and a single recommendation
tags: [decide]
includes:
  - fragments/constraint-stay-in-scope.md
  - fragments/output-recommendation.md
---

## Use

Replace `{{decision}}`, `{{options}}`, and `{{criteria}}`.

## Prompt

Compare the options for this decision. Judge only against the criteria.

{{include:fragments/constraint-stay-in-scope.md}}

{{include:fragments/output-recommendation.md}}

Decision:

{{decision}}

Options:

{{options}}

Criteria:

{{criteria}}

## Notes

Works when the options and criteria are already listed. It will not go gather missing facts.
