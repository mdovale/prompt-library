---
id: revise.deepen
title: Deepen a task
status: active
use_when: You have a task or prompt and need it rewritten to ask for professional depth rather than more scope
inputs: [task]
output: Four diagnostic points, then the rewritten prompt
tags: [revise, prompts]
---

## Use

Replace `{{task}}` with the task or prompt to deepen.

## Prompt

Rewrite this task so it asks for a deeper version of the same work, not a larger one. Keep the original goal. Raise the standard of the work.

Before the rewrite, answer these four points:

1. What a top professional in this field would do here that the task does not ask for.
2. The rawest material they would start from, instead of a source that has already been digested.
3. The specific methods and tools they would use.
4. What, besides you or the person who set the task, would show the result is right.

Then rewrite the task so it asks for exactly that.

Task:

{{task}}

## Notes

Raises the standard of the same task. For a shorter edit that keeps the claim, use `revise.clarity`.
