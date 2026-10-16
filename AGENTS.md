# Prompt library

This repository is a catalog of prompts. Look up a prompt before writing a new one.

## Lookup

1. Read `catalog.yaml`.
2. Choose one entry by `id`, or one `active` entry by `use_when`.
3. Read that file and its `includes` fragments. Leave the rest of the library unread.
4. The model call is the `## Prompt` section. Replace each `{{include:path}}` with that fragment's body (the text after its frontmatter). Fill other `{{placeholders}}` from the task. Omit `## Use` and `## Notes`.

If no entry fits, say so.

## Changes

Prompt files, fragments, and `catalog.yaml` follow `.cursor/rules/prompt-format.mdc`. After editing them, run `python3 scripts/check_library.py`.
