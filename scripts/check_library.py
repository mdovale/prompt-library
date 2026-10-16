#!/usr/bin/env python3
"""Validate prompts, fragments, and catalog.yaml stay in sync."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"draft", "active", "retired"}
PROMPT_KEYS = {
    "id",
    "title",
    "status",
    "use_when",
    "inputs",
    "output",
    "tags",
    "includes",
}
PROMPT_REQUIRED = PROMPT_KEYS - {"includes"}
FRAGMENT_KEYS = {"id", "title"}
CATALOG_KEYS = {"id", "path", "title", "status", "use_when", "inputs", "tags"}
SECTIONS = ("## Use", "## Prompt", "## Notes")
SLUG = re.compile(r"^[a-z][a-z0-9-]*$")
INCLUDE = re.compile(r"\{\{include:([^}]+)\}\}")
PLACEHOLDER = re.compile(r"\{\{([^{}]+)\}\}")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def split_frontmatter(text: str, rel: str, errors: list[str]) -> tuple[str, str] | None:
    if not text.startswith("---\n"):
        fail(errors, f"{rel}: file must start with ---")
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(errors, f"{rel}: missing closing ---")
        return None
    return text[4:end], text[end + 5 :]


def parse_inline_list(value: str, rel: str, key: str, errors: list[str]) -> list[str]:
    if not (value.startswith("[") and value.endswith("]")):
        fail(errors, f"{rel}: {key} must be an inline list like [a, b]")
        return []
    inner = value[1:-1].strip()
    if not inner:
        fail(errors, f"{rel}: {key} list is empty")
        return []
    items = [part.strip() for part in inner.split(",")]
    if any(not item for item in items):
        fail(errors, f"{rel}: {key} has an empty list item")
    return items


def parse_value(value: str, rel: str, key: str, errors: list[str]) -> str | list[str]:
    if value.startswith("["):
        return parse_inline_list(value, rel, key, errors)
    if value.startswith(("'", '"', ">", "|")):
        fail(errors, f"{rel}: {key} must be a plain single-line value")
        return value
    return value


def parse_flat_mapping(raw: str, rel: str, errors: list[str]) -> dict:
    data: dict = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line[0] in " \t":
            fail(errors, f"{rel}: unexpected indent near {line.strip()!r}")
            index += 1
            continue
        if ":" not in line:
            fail(errors, f"{rel}: expected key: value, got {line!r}")
            index += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            items: list[str] = []
            index += 1
            while index < len(lines) and lines[index].startswith("  - "):
                items.append(lines[index][4:].strip())
                index += 1
            if not items:
                fail(errors, f"{rel}: {key} list is empty or missing")
            data[key] = items
            continue
        data[key] = parse_value(rest, rel, key, errors)
        index += 1
    return data


def parse_catalog(raw: str, errors: list[str]) -> list[dict]:
    rel = "catalog.yaml"
    lines = [line for line in raw.splitlines() if line.strip()]
    if not lines or lines[0] != "prompts:":
        fail(errors, "catalog.yaml: first line must be prompts:")
        return []
    entries: list[dict] = []
    current: dict | None = None
    for line in lines[1:]:
        if line.startswith("  - "):
            if current is not None:
                entries.append(current)
            current = {}
            body = line[4:]
        elif line.startswith("    ") and current is not None:
            body = line[4:]
        else:
            fail(errors, f"catalog.yaml: unexpected line {line!r}")
            continue
        if ":" not in body:
            fail(errors, f"catalog.yaml: expected key: value, got {body!r}")
            continue
        key, _, rest = body.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            fail(errors, f"catalog.yaml: {key} must be a single-line value")
            continue
        current[key] = parse_value(rest, rel, key, errors)
    if current is not None:
        entries.append(current)
    return entries


def section_map(body: str, rel: str, errors: list[str]) -> dict[str, str]:
    positions = []
    for heading in SECTIONS:
        match = re.search(rf"(?m)^{re.escape(heading)}\s*$", body)
        if match is None:
            fail(errors, f"{rel}: missing {heading}")
            return {}
        positions.append((match.start(), match.end(), heading))
    positions.sort()
    if [item[2] for item in positions] != list(SECTIONS):
        fail(errors, f"{rel}: sections must appear in order Use, Prompt, Notes")
        return {}
    found: dict[str, str] = {}
    for index, (_, end, heading) in enumerate(positions):
        stop = positions[index + 1][0] if index + 1 < len(positions) else len(body)
        text = body[end:stop].strip()
        if not text:
            fail(errors, f"{rel}: {heading} is empty")
        found[heading] = text
    return found


def check_prompt(path: Path, errors: list[str]) -> dict | None:
    rel = path.relative_to(ROOT).as_posix()
    parsed = split_frontmatter(path.read_text(), rel, errors)
    if parsed is None:
        return None
    raw, body = parsed
    meta = parse_flat_mapping(raw, rel, errors)
    unknown = set(meta) - PROMPT_KEYS
    missing = PROMPT_REQUIRED - set(meta)
    for key in sorted(unknown):
        fail(errors, f"{rel}: unexpected frontmatter key {key}")
    for key in sorted(missing):
        fail(errors, f"{rel}: missing frontmatter key {key}")
    if missing or unknown:
        return None

    job, _, slug = rel.removeprefix("prompts/").removesuffix(".md").partition("/")
    if not SLUG.match(job) or not slug or not SLUG.match(slug) or "/" in slug:
        fail(errors, f"{rel}: path must be prompts/<job>/<slug>.md")
    expected_id = f"{job}.{slug}"
    if meta.get("id") != expected_id:
        fail(errors, f"{rel}: id must be {expected_id}")
    if meta.get("status") not in STATUSES:
        fail(errors, f"{rel}: status must be draft, active, or retired")
    for key in ("inputs", "tags"):
        if not isinstance(meta.get(key), list):
            fail(errors, f"{rel}: {key} must be an inline list")
    includes = meta.get("includes", [])
    if "includes" in meta and not isinstance(includes, list):
        fail(errors, f"{rel}: includes must be a list of fragment paths")
        includes = []

    sections = section_map(body, rel, errors)
    prompt = sections.get("## Prompt", "")
    markers = INCLUDE.findall(prompt)
    if sorted(markers) != sorted(includes):
        fail(errors, f"{rel}: includes and {{{{include:...}}}} markers differ")
    for include in includes:
        if not include.startswith("fragments/") or not include.endswith(".md"):
            fail(errors, f"{rel}: include must be fragments/<file>.md")
        elif not (ROOT / include).is_file():
            fail(errors, f"{rel}: missing include {include}")
    names = []
    for placeholder in PLACEHOLDER.findall(prompt):
        if placeholder.startswith("include:"):
            continue
        names.append(placeholder)
    inputs = meta.get("inputs") if isinstance(meta.get("inputs"), list) else []
    if Counter(names) != Counter(inputs):
        fail(errors, f"{rel}: {{{{placeholders}}}} must match inputs")
    return {
        "id": meta.get("id"),
        "path": rel,
        "title": meta.get("title"),
        "status": meta.get("status"),
        "use_when": meta.get("use_when"),
        "inputs": inputs,
        "tags": meta.get("tags") if isinstance(meta.get("tags"), list) else [],
    }


def check_fragment(path: Path, errors: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    parsed = split_frontmatter(path.read_text(), rel, errors)
    if parsed is None:
        return
    raw, body = parsed
    meta = parse_flat_mapping(raw, rel, errors)
    unknown = set(meta) - FRAGMENT_KEYS
    missing = FRAGMENT_KEYS - set(meta)
    for key in sorted(unknown):
        fail(errors, f"{rel}: unexpected frontmatter key {key}")
    for key in sorted(missing):
        fail(errors, f"{rel}: missing frontmatter key {key}")
    stem = path.stem
    if meta.get("id") != stem:
        fail(errors, f"{rel}: id must be {stem}")
    if not body.strip():
        fail(errors, f"{rel}: fragment body is empty")
    for heading in SECTIONS:
        if re.search(rf"(?m)^{re.escape(heading)}\s*$", body):
            fail(errors, f"{rel}: fragments omit {heading}")


def main() -> int:
    errors: list[str] = []
    prompt_root = ROOT / "prompts"
    fragment_root = ROOT / "fragments"
    for path in sorted(prompt_root.glob("*.md")):
        fail(errors, f"{path.relative_to(ROOT).as_posix()}: move this file under prompts/<job>/")
    for path in sorted(prompt_root.rglob("*.md")):
        if len(path.relative_to(prompt_root).parts) > 2:
            fail(errors, f"{path.relative_to(ROOT).as_posix()}: path must be prompts/<job>/<slug>.md")
    for path in sorted(fragment_root.rglob("*.md")):
        if path.parent != fragment_root:
            fail(errors, f"{path.relative_to(ROOT).as_posix()}: fragments live in fragments/")

    prompt_paths = sorted(prompt_root.glob("*/*.md"))
    fragment_paths = sorted(fragment_root.glob("*.md"))
    if not prompt_paths:
        fail(errors, "prompts/: no prompt files")

    expected: dict[str, dict] = {}
    for path in prompt_paths:
        entry = check_prompt(path, errors)
        if entry and entry["id"] in expected:
            fail(errors, f"{entry['path']}: duplicate id {entry['id']}")
        elif entry and entry["id"]:
            expected[entry["id"]] = entry
    for path in fragment_paths:
        check_fragment(path, errors)

    catalog_path = ROOT / "catalog.yaml"
    if not catalog_path.is_file():
        fail(errors, "catalog.yaml: file is missing")
        entries = []
    else:
        entries = parse_catalog(catalog_path.read_text(), errors)

    seen: set[str] = set()
    for entry in entries:
        unknown = set(entry) - CATALOG_KEYS
        missing = CATALOG_KEYS - set(entry)
        label = entry.get("id") or entry.get("path") or "entry"
        for key in sorted(unknown):
            fail(errors, f"catalog.yaml: {label} has unexpected key {key}")
        for key in sorted(missing):
            fail(errors, f"catalog.yaml: {label} is missing {key}")
        if missing:
            continue
        prompt_id = entry["id"]
        if prompt_id in seen:
            fail(errors, f"catalog.yaml: duplicate id {prompt_id}")
        seen.add(prompt_id)
        source = expected.get(prompt_id)
        if source is None:
            fail(errors, f"catalog.yaml: {prompt_id} has no prompt file")
            continue
        for key in CATALOG_KEYS:
            if entry[key] != source[key]:
                fail(errors, f"catalog.yaml: {prompt_id} {key} does not match {source['path']}")

    for prompt_id, source in expected.items():
        if prompt_id not in seen:
            fail(errors, f"catalog.yaml: missing {prompt_id} ({source['path']})")

    if errors:
        print(f"{len(errors)} problem(s):", file=sys.stderr)
        for message in errors:
            print(f"- {message}", file=sys.stderr)
        return 1
    print(f"ok: {len(expected)} prompts, {len(fragment_paths)} fragments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
