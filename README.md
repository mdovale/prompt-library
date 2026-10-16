# Prompt library

Prompts to look up during LLM tasks and agent workflows. One id, one file. `catalog.yaml` is the index.

## Find a prompt

- Browse `catalog.yaml` for `id` and `use_when`.
- In Cursor, run `/list-prompts` or `/use-prompt`.

`/use-prompt` reads the catalog, opens one prompt, expands fragments, and returns the text to send.

## Add a prompt

Run `/add-prompt`, or add `prompts/<job>/<slug>.md` and a matching `catalog.yaml` entry. The id is `<job>.<slug>` (for example `prompts/review/security.md` is `review.security`).

Then run:

```bash
python3 scripts/check_library.py
```

`/check-library` runs that same check.

## Layout

```text
catalog.yaml          # index an agent reads first
prompts/<job>/        # one prompt per file
fragments/            # clauses prompts include
scripts/check_library.py
.cursor/rules/        # lookup and format rules
.cursor/commands/     # /use-prompt, /add-prompt, /list-prompts, /check-library
```

Starter jobs: `review`, `extract`, `draft`, `revise`, `plan`, `debug`, `decide`. Add a job by adding a folder.
