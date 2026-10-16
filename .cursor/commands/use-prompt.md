---
name: use-prompt
description: Look up one library prompt and return the text to send
---

# Use a prompt

The user passes a prompt id or describes the task.

1. Read `catalog.yaml`.
2. If they named an id, use that entry. Otherwise pick the single `active` entry whose `use_when` matches the task. If several match, list those ids and `use_when` lines, then stop. If none match, say so and stop.
3. Read the prompt file and each fragment in `includes`.
4. Build the model call from `## Prompt` only. Replace each `{{include:path}}` with that fragment's body after its frontmatter. Leave other `{{placeholders}}` unfilled when the user did not supply them, and list those names.
5. Show the finished prompt in one fenced block. Under it, list any placeholders still open.
6. Keep `## Notes` and `## Use` out of that block.
