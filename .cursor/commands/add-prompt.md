---
name: add-prompt
description: Add one prompt file and its catalog entry
---

# Add a prompt

1. Choose a job folder under `prompts/`: `review`, `extract`, `draft`, `revise`, `plan`, `debug`, `decide`, or a new lowercase job name.
2. Read `.cursor/rules/prompt-format.mdc` and one existing file in `prompts/` before writing.
3. Create `prompts/<job>/<slug>.md` with id `<job>.<slug>`. Put the sendable text only under `## Prompt`.
4. Add the `catalog.yaml` entry in the same change. Copy `id`, `path`, `title`, `status`, `use_when`, `inputs`, and `tags`.
5. Run `python3 scripts/check_library.py`. Fix every failure and run it again.
6. Reply with the new id and its `use_when` line.
