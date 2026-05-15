# Routing

Verb → impeccable reference file path. Used by `SKILL.md` to keep its routing table terse.

## Verb Map

| Verb | Reference file |
|---|---|
| `adapt` | `lib/impeccable/reference/adapt.md` |
| `animate` | `lib/impeccable/reference/animate.md` |
| `audit` | `lib/impeccable/reference/audit.md` |
| `bolder` | `lib/impeccable/reference/bolder.md` |
| `clarify` | `lib/impeccable/reference/clarify.md` |
| `colorize` | `lib/impeccable/reference/colorize.md` |
| `craft` | `lib/impeccable/reference/craft.md` |
| `critique` | `lib/impeccable/reference/critique.md` |
| `delight` | `lib/impeccable/reference/delight.md` |
| `distill` | `lib/impeccable/reference/distill.md` |
| `document` | `lib/impeccable/reference/document.md` |
| `extract` | `lib/impeccable/reference/extract.md` |
| `harden` | `lib/impeccable/reference/harden.md` |
| `layout` | `lib/impeccable/reference/layout.md` |
| `onboard` | `lib/impeccable/reference/onboard.md` |
| `optimize` | `lib/impeccable/reference/optimize.md` |
| `overdrive` | `lib/impeccable/reference/overdrive.md` |
| `polish` | `lib/impeccable/reference/polish.md` |
| `quieter` | `lib/impeccable/reference/quieter.md` |
| `shape` | `lib/impeccable/reference/shape.md` |
| `teach` | `lib/impeccable/reference/teach.md` |
| `typeset` | `lib/impeccable/reference/typeset.md` |
| `live` | `lib/impeccable/scripts/live.mjs` (interactive script, not a reference doc) |

Also relevant for context loading:
- `lib/impeccable/scripts/load-context.mjs` — loads `PRODUCT.md` / `DESIGN.md` for any verb.

## Chaining Rules

Some verbs implicitly call others. The conductor SHOULD short-circuit these chains when context is already loaded.

- `craft` runs `shape` first internally to plan structure before code. If a `shape` artifact for the same target is already present in the conversation, skip the inner call.
- `audit` is a precondition for `polish`, `bolder`, `quieter`, and `harden`. Run audit findings into the next verb as context.
- `teach` is a precondition for `craft` on fresh projects. If `PRODUCT.md` and `DESIGN.md` are missing, run `teach` first.
- `extract` typically follows `document` when capturing tokens from existing UI for codification.

## Image Router Invocation

The router script lives at `scripts/image-router.py`.

- **Implicit invocation:** When `craft.md` reaches a "visual direction" or mock-approval step, the conductor runs:
  ```
  python3 scripts/image-router.py --prompt "<brief extracted from craft step>" --project "<slug>"
  ```
- **Explicit invocation:** When the user runs `/sprout-design image <prompt>`, the conductor calls the router directly with the user prompt and any flags they pass through.
- **Engine override:** `--engine banana` for photo-realistic, `--engine gpt` for text-heavy. Without the flag, the router keyword-scores the prompt.
- **Aspect ratio for banana:** `--aspect-ratio 16:9` (etc.) maps to Gemini's native aspect format.
- **Size for gpt:** `--size 1024x1024`, `1024x1536`, or `1536x1024`.

## Delegation Helper

`scripts/delegate.sh <verb>` resolves and prints the absolute path of a verb's reference file. Useful when the conductor wants to confirm the file exists before reading it.

Example:
```
scripts/delegate.sh audit
# /Users/<user>/.claude/skills/sprout-design/lib/impeccable/reference/audit.md
```

Exits non-zero with an error message on stderr if the verb is unknown.
