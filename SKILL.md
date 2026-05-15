---
name: sprout-design
description: "Sprout's house design skill. Use for ANY frontend design work — building, auditing, critiquing, polishing, animating, generating visual assets, working with design tokens. Triggers on: design, redesign, audit, critique, polish, craft, shape, build, animate, colorize, harden, optimize, image generation, logo, banner, infographic, hero, landing, dashboard, component, form, onboarding. Combines impeccable's 23-verb workflow with taste-skill's tunable dials and unified anti-slop enforcement. Auto-routes image generation to GPT Image 2 (text-heavy) or Gemini Nano Banana (photo-realistic)."
version: "1.0.0"
user-invocable: true
argument-hint: "[craft|shape|audit|critique|polish|bolder|quieter|distill|harden|animate|colorize|typeset|layout|delight|overdrive|clarify|adapt|optimize|onboard|teach|document|extract|live|image|arsenal|tune] [target]"
license: "Internal use — Sprout. Built on impeccable (Apache 2.0). See NOTICE.md."
---

# sprout-design

Sprout's house design skill. One discoverable entrypoint that orchestrates four vendored engines: impeccable (workflow verbs), taste-skill (dials + arsenal patterns), gpt-image (text-heavy asset gen), banana (photo-realistic asset gen).

## Purpose & House Identity

This is Sprout's house design skill. Every frontend deliverable that ships under the Sprout brand routes through this skill so that aesthetic direction, anti-slop enforcement, and asset generation stay coherent across SixSeven, AuraCheck, TOCO, and future products. The skill is opinionated by design: it inherits the bold-aesthetic-direction principle (pick a real flavor, never converge on generic AI defaults), enforces the unified anti-slop list, and applies house tokens (Cabinet Grotesk + Geist, OKLCH-restrained palette) unless a project's `DESIGN.md` overrides them.

Default dials are `variance=7 motion=5 density=5` — slightly bolder than baseline, balanced motion, normal density. These are tuned for B2B SaaS dashboards. Override per project by editing `DESIGN.md` frontmatter, per session via `/sprout-design tune <v> <m> <d>`, or per command via `--variance=N --motion=N --density=N`.

## Routing Table

| Verb | Action |
|---|---|
| `teach` | Run discovery wizard. Write `PRODUCT.md` + `DESIGN.md` to project root with house dials pinned in frontmatter. Workflow: `lib/impeccable/scripts/load-context.mjs` then `lib/impeccable/reference/teach.md`. |
| `craft <target>` | Apply house overlay, load `lib/impeccable/reference/craft.md`, execute. At mock-approval step, call `scripts/image-router.py` for visual asset generation. |
| `shape <target>` | Load `lib/impeccable/reference/shape.md`. Apply house defaults during discovery. |
| `audit [target]` | Load `lib/impeccable/reference/audit.md`. Additionally check `reference/anti-slop-unified.md` rules. |
| `critique [target]` | Load `lib/impeccable/reference/critique.md`. Add house-tokens compliance check from `reference/house-tokens.md`. |
| `polish` | Delegate to `lib/impeccable/reference/polish.md`. Pass current dials as context. |
| `bolder` | Delegate to `lib/impeccable/reference/bolder.md`. Pass current dials as context. |
| `quieter` | Delegate to `lib/impeccable/reference/quieter.md`. Pass current dials as context. |
| `distill` | Delegate to `lib/impeccable/reference/distill.md`. Pass current dials as context. |
| `harden` | Delegate to `lib/impeccable/reference/harden.md`. Pass current dials as context. |
| `animate` | Delegate to `lib/impeccable/reference/animate.md`. Pass current dials as context. |
| `colorize` | Delegate to `lib/impeccable/reference/colorize.md`. Pass current dials as context. |
| `typeset` | Delegate to `lib/impeccable/reference/typeset.md`. Pass current dials as context. |
| `layout` | Delegate to `lib/impeccable/reference/layout.md`. Pass current dials as context. |
| `delight` | Delegate to `lib/impeccable/reference/delight.md`. May invoke image-router for hero/decorative assets. |
| `overdrive` | Delegate to `lib/impeccable/reference/overdrive.md`. May invoke image-router for hero/decorative assets. |
| `clarify` | Delegate to `lib/impeccable/reference/clarify.md`. Pass current dials as context. |
| `adapt` | Delegate to `lib/impeccable/reference/adapt.md`. Pass current dials as context. |
| `optimize` | Delegate to `lib/impeccable/reference/optimize.md`. Pass current dials as context. |
| `onboard` | Delegate to `lib/impeccable/reference/onboard.md`. Pass current dials as context. |
| `document` | Generate `DESIGN.md` via `lib/impeccable/reference/document.md` flow. |
| `extract` | Extract design tokens via `lib/impeccable/reference/extract.md`. |
| `live` | Interactive variant mode via `lib/impeccable/scripts/live.mjs`. |
| `image <prompt>` | Run `scripts/image-router.py` with prompt. Auto-engine unless `--engine banana\|gpt`. |
| `arsenal [category]` | Show patterns from `reference/arsenal.md`. Categories: `hero`, `navigation`, `layout`, `card`, `scroll`, `gallery`, `typography`, `micro`. |
| `tune <variance> <motion> <density>` | Update session dials. Example: `/sprout-design tune 9 7 4`. |

Full path mapping lives in `reference/routing.md`.

## Mandatory Pre-Flight

Before executing any verb that builds or edits code, load this stack in order:

1. `reference/house-philosophy.md` — bold aesthetic direction principle.
2. `reference/anti-slop-unified.md` — banned defaults (REJECT / ALLOW WHEN / REPLACE WITH).
3. `reference/house-tokens.md` — fonts, color, spacing, motion, icons.
4. `reference/dials.md` — interpret current dial values.
5. `node lib/impeccable/scripts/load-context.mjs` — load project `PRODUCT.md` / `DESIGN.md` if present.

Resolve dial values with this precedence: `DESIGN.md` frontmatter > CLI flags > session tune > defaults (7/5/5).

## Dial Override Syntax

`--variance=N --motion=N --density=N` where each `N` is 1–10.

Example: `/sprout-design craft hero --density=9 --motion=3` overrides to packed-cockpit density with restrained motion for one command. Use `tune` to update the session-wide defaults instead.

## Image-Gen Invocation Pattern

When a verb (typically `craft`, `delight`, `overdrive`) needs visual assets, invoke:

```
python3 scripts/image-router.py --prompt "<extracted brief>" \
  [--engine banana|gpt] \
  [--size 1024x1024|1024x1536|1536x1024] \
  [--aspect-ratio 1:1|16:9|9:16] \
  [--quality low|medium|high|auto] \
  [--project <slug>]
```

Without `--engine`, the router scores the prompt for text-heavy vs photo-realistic keywords and picks GPT Image 2 or Gemini Nano Banana accordingly. Default fallback is GPT (more general).

## Output Conventions

- Generated images: `~/Documents/sprout-design-assets/<project-slug>/`
- Cost log (jsonl): `~/.sprout-design/cost.jsonl`
- Project context files: written to project root (`PRODUCT.md`, `DESIGN.md`)

## Error Handling

- `lib/impeccable/reference/<verb>.md` not found → respond `"verb not recognized, did you mean <closest>?"` and list available verbs.
- OpenAI key missing → direct user to `python3 lib/gpt-image/scripts/setup.py`.
- Gemini key missing → direct user to `python3 lib/banana/scripts/setup_mcp.py`.
- Network/API failure during image-gen → print the router's structured error JSON and stop; do not auto-retry.

## Surface Discipline

The underlying workflow engine is impeccable by Paul Bakaus (Apache 2.0; see `NOTICE.md`). Do not expose `lib/` paths in routine output to end users — present a clean `/sprout-design <verb>` command surface. Internal references to `lib/...` are fine in this `SKILL.md` and the `reference/` files because they are read by the model, not shipped to the end user as UX.
