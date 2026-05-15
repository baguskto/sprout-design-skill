# OpenAI GPT Image Models

> Verify the latest at https://platform.openai.com/docs/models and
> https://platform.openai.com/docs/api-reference/images

## Available Models

### gpt-image-2 (DEFAULT)
| Property | Value |
|----------|-------|
| **Model ID** | `gpt-image-2` |
| **Status** | Current generation -- **Active, recommended default** |
| **Strengths** | Best-in-class text rendering, layout reasoning ("thinking latent space"), brand-aware composition |
| **Sizes** | `1024x1024`, `1024x1536`, `1536x1024`, `auto` |
| **Quality tiers** | `low`, `medium`, `high`, `auto` |
| **Endpoints** | `/v1/images/generations`, `/v1/images/edits` |
| **Output format** | PNG (returned as base64 in `data[0].b64_json`) |
| **Best For** | All standard production generation and editing, especially text-heavy or layout-driven assets |

### gpt-image-1 (LEGACY / FALLBACK)
| Property | Value |
|----------|-------|
| **Model ID** | `gpt-image-1` |
| **Status** | Previous generation, still available |
| **Strengths** | Cheaper per image |
| **Weaknesses** | Weaker text rendering, less reliable layout reasoning |
| **Best For** | Budget-constrained workflows where typography accuracy is not required |

## Domain-to-Model Routing

| Domain Mode | Recommended Model | Reason |
|---|---|---|
| Cinema, Landscape, Abstract | `gpt-image-2` | Layout reasoning improves complex compositions |
| Product, Portrait | `gpt-image-2` | Fidelity at `high` quality |
| UI, Infographic | `gpt-image-2` | Excellent typography and structured layout |
| Logo | `gpt-image-2` | Best text rendering -- exact wordmark spelling |
| Editorial | `gpt-image-2` | Default |
| Budget / bulk drafts | `gpt-image-1` | Cheaper, less text-critical |

## Quality Defaults by Domain

| Domain | Default `quality` | Rationale |
|--------|------------------|-----------|
| Portrait, Product, Logo | `high` | Fine detail and text fidelity |
| Cinema, Landscape | `high` | Atmospheric depth |
| UI, Infographic | `high` | Reliable typography |
| Quick draft / preview | `low` | Rapid iteration, lowest cost |
| Standard production | `medium` | Balanced quality and cost |

## Sizes

GPT Image 2 supports a fixed set of sizes -- there is **no `aspect_ratio` parameter**.

| `size` | Pixels | Best for |
|--------|--------|----------|
| `1024x1024` | Square 1:1 | Social posts, avatars, thumbnails, icons |
| `1024x1536` | Portrait 2:3 | Book covers, posters, mobile vertical, Pinterest |
| `1536x1024` | Landscape 3:2 | Blog headers, presentations, website hero |
| `auto` | Model picks | When unsure, let the model select based on prompt |

**Mapping common ratios to supported sizes:**

| Desired ratio | Closest `size` | Crop strategy |
|---------------|---------------|---------------|
| 1:1 (square) | `1024x1024` | No crop |
| 4:3, 3:2, 16:9, 5:4 (landscape) | `1536x1024` | Crop horizontally in post |
| 3:4, 2:3, 4:5, 9:16 (portrait) | `1024x1536` | Crop vertically in post |
| 21:9, 4:1, 8:1 (ultra-wide) | `1536x1024` | Heavy horizontal crop in post |
| 1:4, 1:8 (ultra-tall) | `1024x1536` | Heavy vertical crop in post |

For non-native ratios, use `references/post-processing.md` to crop after generation.

## Quality Tiers

| `quality` | Use case |
|-----------|----------|
| `low` | Drafts, rapid iteration, low cost |
| `medium` | Standard production |
| `high` | Final deliverables, hero images, anything with text |
| `auto` | Model picks based on prompt complexity |

## API Configuration

### Generate endpoint
```
POST https://api.openai.com/v1/images/generations
Authorization: Bearer $OPENAI_API_KEY
Content-Type: application/json
```

### Required body
```json
{
  "model": "gpt-image-2",
  "prompt": "your prompt here",
  "size": "1024x1024",
  "quality": "high",
  "n": 1
}
```

### Edit endpoint
```
POST https://api.openai.com/v1/images/edits
Authorization: Bearer $OPENAI_API_KEY
Content-Type: multipart/form-data
```

Form fields: `model`, `prompt`, `image` (file upload), optional `mask`, `size`,
`quality`, `n`.

### Response shape
```json
{
  "created": 1234567890,
  "data": [
    { "b64_json": "<base64-encoded PNG bytes>" }
  ]
}
```

Decode `data[0].b64_json` from base64 and write to a `.png` file.

## Rate Limits

Rate limits vary by usage tier. Check yours at
https://platform.openai.com/account/limits. Tiers scale with cumulative spend.

| Tier | Notes |
|------|-------|
| Free / Tier 1 | Lower RPM, suited to development |
| Tier 2+ | Production-grade throughput |
| Enterprise | Custom |

On HTTP 429: wait, retry with exponential backoff (2s, 4s, 8s).

## Pricing

Approximate. Subject to change -- verify at https://openai.com/api/pricing.

| Model | Size | Quality | Approx cost / image |
|-------|------|---------|---------------------|
| gpt-image-2 | 1024x1024 | low | ~$0.011 |
| gpt-image-2 | 1024x1024 | medium | ~$0.042 |
| gpt-image-2 | 1024x1024 | high | ~$0.167 |
| gpt-image-2 | 1024x1536 / 1536x1024 | low | ~$0.016 |
| gpt-image-2 | 1024x1536 / 1536x1024 | medium | ~$0.063 |
| gpt-image-2 | 1024x1536 / 1536x1024 | high | ~$0.250 |
| gpt-image-1 | any | n/a | cheaper, varies |

## Image Output Specs

| Property | Value |
|----------|-------|
| **Format** | PNG (base64 in `b64_json`) |
| **Max Resolution** | 1536x1024 or 1024x1536 native |
| **Color Space** | sRGB |
| **Text Rendering** | Excellent -- near-perfect for short copy, reliable for paragraphs |
| **Transparency** | Not native -- generate on solid background then post-process |

## Safety / Content Policy

OpenAI returns HTTP 400 with structured `error.code` values when content is blocked:

| Error code | Meaning | Retryable? |
|------------|---------|:----------:|
| `content_policy_violation` | Prompt violates content policy | Rephrase prompt |
| `moderation_blocked` | Generated image blocked by output moderation | Shift visual concept |
| `invalid_request_error` | Malformed parameter | Fix the parameter |

Filters cannot be disabled. The only path forward on a block is rephrasing -- see
`references/prompt-engineering.md` Safety Filter Rephrase Strategies.

## Key Limitations

- No video generation (image only)
- No native transparent backgrounds -- use post-processing workaround
- No `seed` parameter for reproducibility on gpt-image-2 (verify current docs)
- No persistent session / chat memory -- multi-turn is client-side replay
- Three discrete sizes only (plus `auto`); non-native ratios require cropping
- Text rendering is strong but very small text (<16px equivalent) may still need iteration
