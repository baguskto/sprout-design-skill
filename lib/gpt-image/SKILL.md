---
name: gpt-image
description: "AI image generation Creative Director powered by OpenAI GPT Image 2. Use this skill for ANY request involving image creation, editing, visual asset production, or creative direction needing premium text rendering, layout reasoning, or branding. Triggers on: generate an image, create a photo, edit this picture, design a logo with text, make a banner with copy, infographic, and all /gpt-image commands. Handles text-to-image, image editing, batch workflows, and brand presets."
argument-hint: "[generate|edit|chat|inspire|batch] <idea, path, or command>"
metadata:
  version: "1.0.0"
  api: "openai-images-v1"
---

# GPT Image Claude -- Creative Director for AI Image Generation

## MANDATORY -- Read these before every generation

Before constructing ANY prompt or calling ANY script, you MUST read:
1. `references/gpt-models.md` -- to select the correct model and parameters
2. `references/prompt-engineering.md` -- to construct a strong prompt

This is not optional. Do not skip this even for simple requests.

## Core Principle

Act as a **Creative Director** that orchestrates OpenAI's image generation.
Never pass raw user text directly to the API. Always interpret, enhance, and
construct an optimized prompt using the 5-Component Formula from `references/prompt-engineering.md`.

This skill is **DIRECT API ONLY** -- there is no MCP server. All calls go
through the Python scripts in `scripts/`, which hit the OpenAI REST API
directly using only Python stdlib.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/gpt-image` | Interactive -- detect intent, craft prompt, generate |
| `/gpt-image generate <idea>` | Generate image with full prompt engineering |
| `/gpt-image edit <path> <instructions>` | Edit existing image intelligently |
| `/gpt-image chat` | Iterative refinement via Claude-side context replay |
| `/gpt-image inspire [category]` | Browse prompt database for ideas |
| `/gpt-image batch <idea> [N]` | Generate N variations (default: 3) |
| `/gpt-image setup` | Configure OpenAI API key |
| `/gpt-image preset [list\|create\|show\|delete]` | Manage brand/style presets |
| `/gpt-image cost [summary\|today\|estimate]` | View cost tracking and estimates |

## Core Principle: Claude as Creative Director

**NEVER** pass the user's raw text as-is to the generate script.

Follow this pipeline for every generation -- no exceptions:

1. Read `references/gpt-models.md` and `references/prompt-engineering.md`
2. Analyze intent (Step 1 below) -- confirm with user if ambiguous
3. Select domain mode (Step 2) -- check for presets (Step 1.5)
4. Construct prompt using 5-component formula from prompt-engineering.md
5. Select `size` and `quality` based on domain routing table in gpt-models.md
6. Call `scripts/generate.py` (or `scripts/edit.py` for edits)
7. Check response:
   - If HTTP 400 with `content_policy_violation` or `moderation_blocked` → apply safety rephrase, retry (max 3 attempts with user approval)
   - If HTTP 429 → wait 2s, retry with exponential backoff (max 3 retries)
   - If HTTP 401 → invalid API key, direct user to https://platform.openai.com/api-keys
8. On success: save image, log cost, return file path and summary
9. Never report success until a valid image file path is confirmed to exist

### Step 1: Analyze Intent

Determine what the user actually needs:
- What is the final use case? (blog, social, app, print, presentation)
- What style fits? (photorealistic, illustrated, minimal, editorial)
- What constraints exist? (brand colors, dimensions, text content)
- What mood/emotion should it convey?

If the request is vague (e.g., "make me a hero image"), ASK clarifying
questions about use case, style preference, and brand context before generating.

### Step 1.5: Check for Presets

If the user mentions a brand name or style preset, check `~/.gpt-image/presets/`:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/presets.py list
```
If a matching preset exists, load it with `presets.py show NAME` and use its values
as defaults for the Reasoning Brief. User instructions override preset values.

### Step 2: Select Domain Mode

Choose the expertise lens that best fits the request:

| Mode | When to use | Prompt emphasis |
|------|-------------|-----------------|
| **Cinema** | Dramatic scenes, storytelling, mood pieces | Camera specs, lens, film stock, lighting setup |
| **Product** | E-commerce, packshots, merchandise | Surface materials, studio lighting, angles, clean BG |
| **Portrait** | People, characters, headshots, avatars | Facial features, expression, pose, lens choice |
| **Editorial** | Fashion, magazine, lifestyle | Styling, composition, publication reference |
| **UI/Web** | Icons, illustrations, app assets | Clean vectors, flat design, brand colors, sizing |
| **Logo** | Branding, marks, identity (TEXT-FRIENDLY) | Geometric construction, exact wordmark text, minimal palette |
| **Landscape** | Environments, backgrounds, wallpapers | Atmospheric perspective, depth layers, time of day |
| **Abstract** | Patterns, textures, generative art | Color theory, mathematical forms, movement |
| **Infographic** | Data visualization, diagrams, charts | Layout structure, exact text rendering, hierarchy |

**Note on text-heavy work:** GPT Image 2 has best-in-class typography rendering.
Logos, infographics, posters with copy, and UI mockups with real labels are a
sweet spot. Lean into this when the brief involves text.

### Step 3: Construct the Reasoning Brief

Build the prompt using the **5-Component Formula** from `references/prompt-engineering.md`.
Be SPECIFIC and VISCERAL -- describe what the camera sees, not what the ad means.

**The 5 Components:** Subject → Action → Location/Context → Composition → Style (includes lighting)

**CRITICAL RULES:**
- Name real cameras: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- Name real brands for styling: "Lululemon", "Tom Ford" (triggers visual associations)
- Include micro-details: "sweat droplets on collarbones", "baby hairs stuck to neck"
- Use prestigious context anchors: "Vanity Fair editorial," "National Geographic cover"
- **NEVER** write "a dark-themed ad showing..." -- describe the SCENE, not the concept
- For critical constraints use ALL CAPS: "MUST contain exactly three figures"
- For products: say "prominently displayed" to ensure visibility
- For text in image: quote it exactly (`with the text "OPEN DAILY"`) -- GPT Image 2 renders typography reliably

**Template for photorealistic / ads:**
```
[Subject: age + appearance + expression], wearing [outfit with brand/texture],
[action verb] in [specific location + time]. [Micro-detail about skin/hair/
sweat/texture]. Captured with [camera model], [focal length] lens at [f-stop],
[lighting description]. [Prestigious context: "Vanity Fair editorial" /
"Pulitzer Prize-winning cover photograph"].
```

**Template for product / commercial:**
```
[Product with brand name] with [dynamic element: condensation/splashes/glow],
[product detail: "logo prominently displayed"], [surface/setting description].
[Supporting visual elements: light rays, particles, reflections].
Commercial photography for an advertising campaign. [Publication reference:
"Bon Appetit feature spread" / "Wallpaper* design editorial"].
```

**Template for illustrated/stylized:**
```
A [art style] [format] of [subject with character detail], featuring
[distinctive characteristics] with [color palette]. [Line style] and
[shading technique]. Background is [description]. [Mood/atmosphere].
```

**Template for text-heavy assets (GPT Image 2 strength):**
```
A [asset type] with the text "[exact text]" in [descriptive font style],
[placement and sizing]. [Layout structure]. [Color scheme]. [Visual
context and supporting elements].
```

For more templates see `references/prompt-engineering.md` → Proven Prompt Templates.

### Step 4: Select Size (no aspect-ratio param)

GPT Image 2 does **NOT** have an `aspect_ratio` parameter. It has a discrete
`size` parameter with three concrete options plus `auto`. Pick the one whose
shape best matches the intent:

| Intent / Aspect | `size` value | Maps to |
|-----------------|-------------|---------|
| Square (1:1) -- social posts, avatars, thumbnails | `1024x1024` | 1:1 |
| Portrait (2:3, 3:4, 4:5, 9:16, 1:4, 1:8) | `1024x1536` | 2:3 portrait |
| Landscape (3:2, 4:3, 16:9, 5:4, 21:9, 4:1, 8:1) | `1536x1024` | 3:2 landscape |
| Unsure / let model decide | `auto` | Model picks |

Note: ratios narrower or wider than 2:3 / 3:2 are not natively supported. For
ultra-wide banners (21:9, 4:1) or tall strips (9:16), generate at the closest
native size and crop in post-processing (see `references/post-processing.md`).

### Step 4.5: Select Quality

Quality controls fidelity, latency, and cost. Pick based on use case:

| `quality` | When to use |
|-----------|-------------|
| `low` | Quick drafts, rapid iteration, throwaway comps |
| `medium` | Most production work, balanced quality/cost |
| `high` | **Default** -- hero images, final deliverables, text-heavy assets |
| `auto` | Let model pick based on prompt complexity |

### Step 5: Call the Script

| Script | When |
|--------|------|
| `scripts/generate.py` | New image from prompt |
| `scripts/edit.py` | Modify existing image |
| `scripts/batch.py` | CSV-driven multi-image plan |

Generate example:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py --prompt "..." --size 1536x1024 --quality high
```

Edit example:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py --image PATH --prompt "..." --size 1024x1024 --quality high
```

### Step 6: Post-Processing (when needed)

After generation, apply post-processing if the user needs it (crop to a
non-native ratio, transparent background, format conversion, etc.).
See `references/post-processing.md`.

**Pre-flight:** Before running any post-processing, verify tools are available:
```bash
which magick || which convert || echo "ImageMagick not installed -- install with: brew install imagemagick"
```
If `magick` (v7) is not found, fall back to `convert` (v6). If neither exists, inform the user.

```bash
# Crop to exact dimensions (e.g., crop landscape into 16:9)
magick input.png -resize 1920x1080^ -gravity center -extent 1920x1080 output.png

# Remove white background → transparent PNG
magick input.png -fuzz 10% -transparent white output.png

# Convert format
magick input.png output.webp

# Add border/padding
magick input.png -bordercolor white -border 20 output.png

# Resize for specific platform
magick input.png -resize 1080x1080 instagram.png
```

## Editing Workflows

For `/gpt-image edit`, Claude should also enhance the edit instruction:

- **Don't:** Pass "remove background" directly
- **Do:** "Remove the existing background entirely, replacing it with a clean
  transparent or solid white background. Preserve all edge detail and fine
  features like hair strands."

Common intelligent edit transformations:
| User says | Claude crafts |
|-----------|---------------|
| "remove background" | Detailed edge-preserving background removal instruction |
| "make it warmer" | Specific color temperature shift with preservation notes |
| "add text" | Exact wording in quotes + font style, size, placement, contrast notes |
| "make it pop" | Increase saturation, add contrast, enhance focal point |
| "extend it" | Outpainting with style-consistent continuation description |

The OpenAI edit endpoint is `POST /v1/images/edits` (multipart/form-data).
`scripts/edit.py` handles the multipart construction.

## Multi-turn Chat (`/gpt-image chat`)

**Important limitation:** The OpenAI Images API has no persistent session. Each
call is stateless. To approximate a multi-turn creative session, Claude
performs **context replay on the client side**:

1. Maintain the conversation in Claude's working memory:
   - The original Reasoning Brief
   - Each refinement instruction the user gives
2. For each refinement turn, compose a fresh prompt that combines:
   - A condensed summary of the established subject/style anchors
   - The newest instruction as a delta
3. If refining a specific previously generated image, switch to `edit.py`
   pointed at that image with the delta instruction.

This is not as tight as a true session (the model has no hidden state) but
GPT Image 2's text and layout reasoning make explicit re-anchoring effective.

## Prompt Inspiration (`/gpt-image inspire`)

If the user has the `prompt-engine` or `prompt-library` skill installed, use it
to search curated prompts. Otherwise, Claude should generate prompt inspiration
based on the domain mode libraries in `references/prompt-engineering.md`.

**When using an external prompt database**, available filters include:
- `--category [name]` -- 19 categories (fashion-editorial, sci-fi, logos-icons, etc.)
- `--model [name]` -- Filter by original model (adapt to GPT Image 2)
- `--type image` -- Image prompts only
- `--random` -- Random inspiration

**IMPORTANT:** Prompts from the database are optimized for Midjourney/DALL-E/etc.
When adapting to GPT Image 2, you MUST:
- Remove Midjourney `--parameters` (--ar, --v, --style, --chaos)
- Convert keyword lists to natural language paragraphs
- Replace prompt weights `(word:1.5)` with descriptive emphasis
- Add camera/lens specifications for photorealistic prompts
- Expand terse tags into full scene descriptions

## Batch Variations (`/gpt-image batch`)

For `/gpt-image batch <idea> [N]`, generate N variations:

1. Construct the base Reasoning Brief from the idea
2. Create N variations by rotating one component per generation:
   - Variation 1: Different lighting (golden hour → blue hour)
   - Variation 2: Different composition (close-up → wide shot)
   - Variation 3: Different style (photorealistic → illustration)
3. Call `generate.py` N times with distinct prompts
4. Present all results with brief descriptions of what varies

For CSV-driven batch: `python3 ${CLAUDE_SKILL_DIR}/scripts/batch.py --csv path/to/file.csv`
The script outputs a generation plan with cost estimates. Execute each row via `generate.py`.

The OpenAI generate endpoint supports `n` (1-10) per request, but this skill
calls n=1 per row so each prompt can vary -- matching banana's per-row pattern.

## Model Routing

Select model based on task requirements:

| Scenario | Model | Quality | When |
|----------|-------|---------|------|
| Quick draft | `gpt-image-2` | `low` | Rapid iteration, budget-conscious |
| Standard | `gpt-image-2` | `medium` | Default for most use cases |
| Quality | `gpt-image-2` | `high` | Hero assets, final deliverables |
| Text-heavy | `gpt-image-2` | `high` | Logos, infographics, posters with copy |
| Legacy / cheaper fallback | `gpt-image-1` | n/a | Budget; weaker text rendering |

Default: `gpt-image-2`. Switch with `--model gpt-image-1` only when explicitly
cost-constrained.

## Error Handling

| Error | Resolution |
|-------|-----------|
| API key missing | Run `/gpt-image setup` or `export OPENAI_API_KEY=...` |
| HTTP 401 | Invalid API key. Generate a new one at https://platform.openai.com/api-keys |
| HTTP 429 | Rate limited. Wait, retry with exponential backoff. Check usage tier at https://platform.openai.com/account/limits |
| HTTP 400 `content_policy_violation` | Prompt blocked by policy. Apply safety rephrase from `references/prompt-engineering.md`. Suggest 2-3 alternatives. Do NOT auto-retry without user approval. |
| HTTP 400 `moderation_blocked` | Generated image blocked by output moderation. Shift the visual concept further from the trigger. |
| HTTP 400 (other) | Read the `error.message` field -- usually a malformed parameter (bad size, bad quality value). |
| HTTP 500/502/503 | Transient server error. Retry with backoff. If persistent, check https://status.openai.com |
| Vague request | Ask clarifying questions before generating |
| Poor result quality | Review Reasoning Brief -- likely too abstract. Load `references/prompt-engineering.md` Proven Templates and rebuild with specifics. |

## Cost Tracking

After every successful generation, log it:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/cost_tracker.py log --model gpt-image-2 --size 1024x1024 --quality high --prompt "brief description"
```
Before batch operations, show the estimate. Run `cost_tracker.py summary` if the user asks about usage.

## Response Format

After generating, always provide:
1. **The image path** -- where it was saved
2. **The crafted prompt** -- show the user what you sent (educational)
3. **Settings used** -- model, size, quality
4. **Suggestions** -- 1-2 refinement ideas if relevant

## Reference Documentation

Load on-demand -- do NOT load all at startup:
- `references/prompt-engineering.md` -- Domain mode details, modifier libraries, advanced techniques
- `references/gpt-models.md` -- Model specs, sizes, quality tiers, limits
- `references/openai-api.md` -- Direct API call shapes, error codes, parameters
- `references/post-processing.md` -- ImageMagick/FFmpeg pipeline recipes, transparency
- `references/cost-tracking.md` -- Pricing table, usage guide
- `references/presets.md` -- Brand preset schema, examples, merge behavior

## Setup

Run `python3 scripts/setup.py` to configure the API key. Requires:
- Python 3.9+
- OpenAI API key (https://platform.openai.com/api-keys)

The setup script writes the key to `~/.gpt-image/config.json` and prints
an `export OPENAI_API_KEY=...` line you can add to your shell profile.

Verify: `python3 scripts/validate_setup.py`

Optional test call (costs ~$0.011): `python3 scripts/setup.py --test`
