---
id: plan.steps
title: Plan the steps
status: active
use_when: You have a goal and need an ordered plan whose first step is small enough to start
inputs: [goal, constraints]
output: An ordered plan with a first step and risks
tags: [plan]
includes:
  - fragments/constraint-stay-in-scope.md
---

## Use

Replace `{{goal}}` and `{{constraints}}`. Use "None" when there are no constraints.

## Prompt

Break the goal into an ordered plan. The first step must be small enough to start with the information given.

{{include:fragments/constraint-stay-in-scope.md}}

## Plan

1. Step. Say what is true when it is done.

## First step

The concrete action to take now.

## Risks

- Risk, and the step that addresses it.

Goal:

{{goal}}

Constraints:

{{constraints}}

## Notes

Fits implementation and writing tasks. Dates appear only when the constraints include them.
