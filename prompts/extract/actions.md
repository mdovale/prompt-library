---
id: extract.actions
title: Extract actions
status: active
use_when: You have notes or a transcript and need owners, actions, and open questions
inputs: [source]
output: Markdown lists of decisions, actions, and open questions
tags: [extract, meetings]
includes:
  - fragments/constraint-stay-in-scope.md
---

## Use

Replace `{{source}}` with the notes or transcript.

## Prompt

Extract decisions, actions, and open questions from the source. Use only what the source states.

{{include:fragments/constraint-stay-in-scope.md}}

## Decisions

- Decision, and who confirmed it when the source says.

## Actions

- Owner — action — due date when stated. Write "unassigned" or "no date" when the source omits them.

## Open questions

- Question, and who it is waiting on when the source says.

If a section has nothing, write "None."

Source:

{{source}}

## Notes

Fits meeting notes and chat threads. Owners appear only when the source names them.
