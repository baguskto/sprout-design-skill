# sprout-design

Sprout's house design skill for Claude Code. One discoverable entrypoint that orchestrates impeccable's 23-verb workflow, taste-skill's tunable dials and pattern arsenal, and dual-engine image generation (GPT Image 2 for text-heavy assets, Gemini Nano Banana for photo-realistic). Installs as a single skill — teammates see one entry in `/skills`, not five.

## Install

```bash
curl -sL https://raw.githubusercontent.com/baguskto/sprout-design-skill/main/install.sh | bash
```

The installer clones into `~/.claude/skills/sprout-design`, makes scripts executable, and prompts for OpenAI and Gemini API keys (skip and configure later if needed).

## Commands Quick Reference

| Command | What it does |
|---|---|
| `/sprout-design teach` | Discovery wizard. Writes `PRODUCT.md` + `DESIGN.md` to project root. |
| `/sprout-design craft <target>` | Build a feature end-to-end. Auto-routes asset generation. |
| `/sprout-design shape <target>` | Plan structure before coding. |
| `/sprout-design audit` | Surface anti-slop violations. |
| `/sprout-design critique` | Deeper aesthetic review against house tokens. |
| `/sprout-design polish` | Tighten existing UI. |
| `/sprout-design bolder` / `quieter` | Push aesthetic direction up or down. |
| `/sprout-design animate` | Add motion within current dial values. |
| `/sprout-design image <prompt>` | Generate visual assets. Engine auto-picked. |
| `/sprout-design arsenal [category]` | Show curated pattern recipes. |
| `/sprout-design tune <v> <m> <d>` | Update session dials (1–10 each). |
| `/sprout-design extract` | Pull design tokens from existing UI. |

Full verb list and routing details in `SKILL.md`.

## House Defaults

- Dials: `variance=7 motion=5 density=5`
- Display font: Cabinet Grotesk (700/600)
- Body font: Geist Sans
- Mono font: Geist Mono
- Palette: OKLCH-restrained, zinc-tinted neutrals, max one accent per project
- Spacing: Tailwind scale (0.25rem base)
- Default card radius: 8px. Default button radius: 999px.
- Icons: `@phosphor-icons/react` (preferred) or `@radix-ui/react-icons`, strokeWidth 1.5

## Per-Project Customization

Override defaults by editing `DESIGN.md` in the project root. The frontmatter accepts:

```yaml
---
dials:
  variance: 9
  motion: 4
  density: 5
fonts:
  display: "Tobias"
  body: "Inter Display"
palette:
  accent: "oklch(0.65 0.2 25)"
spacing:
  base: "0.25rem"
---
```

Precedence: `DESIGN.md` frontmatter > CLI flags (`--variance=N`) > session `tune` > skill defaults.

## Update

```bash
~/.claude/skills/sprout-design/scripts/update.sh
```

Runs `git pull --ff-only` on the skill repo and re-applies executable bits.

## Troubleshooting

- **`verb not recognized`** — Check spelling against the routing table in `SKILL.md`.
- **OpenAI key missing** — Run `python3 ~/.claude/skills/sprout-design/lib/gpt-image/scripts/setup.py`.
- **Gemini key missing** — Run `python3 ~/.claude/skills/sprout-design/lib/banana/scripts/setup_mcp.py`.
- **Skill not appearing in `/skills`** — Confirm path is exactly `~/.claude/skills/sprout-design/SKILL.md`. Restart Claude Code.
- **Image router crashes** — Check `~/.sprout-design/cost.jsonl` for the last entry; rerun with `--engine` explicit to bypass auto-routing.

## Credit

Built on impeccable by Paul Bakaus (Apache 2.0) and inspired by Anthropic's frontend-design and taste-skill. See [NOTICE.md](NOTICE.md) for full attribution.
