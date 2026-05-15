# OpenAI Images API Reference

> Official docs: https://platform.openai.com/docs/api-reference/images
> Models: https://platform.openai.com/docs/models

This skill calls the OpenAI REST API directly from Python stdlib. There is no
MCP server in the loop.

## Endpoints

### Generate -- text to image
```
POST https://api.openai.com/v1/images/generations
Authorization: Bearer $OPENAI_API_KEY
Content-Type: application/json
```

Request body:
```json
{
  "model": "gpt-image-2",
  "prompt": "A weathered ceramicist holding a tea bowl...",
  "size": "1024x1024",
  "quality": "high",
  "n": 1
}
```

Response:
```json
{
  "created": 1715731200,
  "data": [
    { "b64_json": "<base64-encoded PNG>" }
  ]
}
```

Decode `data[0].b64_json` from base64 and write to a PNG file.

### Edit -- modify an existing image
```
POST https://api.openai.com/v1/images/edits
Authorization: Bearer $OPENAI_API_KEY
Content-Type: multipart/form-data
```

Form fields:
| Field | Type | Required | Notes |
|-------|------|---------|-------|
| `model` | string | Yes | `gpt-image-2` |
| `prompt` | string | Yes | Edit instructions |
| `image` | file | Yes | The source image (PNG/JPEG/WebP) |
| `mask` | file | No | Optional alpha mask for inpainting |
| `size` | string | No | `1024x1024`, `1024x1536`, `1536x1024`, `auto` |
| `quality` | string | No | `low`, `medium`, `high`, `auto` |
| `n` | integer | No | 1-10 |

Response shape is identical to `/v1/images/generations`.

## Parameters Reference

| Parameter | Type | Valid values | Default | Notes |
|-----------|------|--------------|---------|-------|
| `model` | string | `gpt-image-2`, `gpt-image-1` | n/a | Default to `gpt-image-2` |
| `prompt` | string | up to ~4,000 chars | n/a | Required |
| `size` | string | `1024x1024`, `1024x1536`, `1536x1024`, `auto` | `1024x1024` | No `aspect_ratio` param exists |
| `quality` | string | `low`, `medium`, `high`, `auto` | `auto` | `high` for hero / text-heavy |
| `n` | integer | 1-10 | 1 | This skill uses `n=1` per call |
| `response_format` | string | `b64_json` only on gpt-image-2 | `b64_json` | Returned as base64 PNG |

Verify the exact parameter list at the official docs link above before
depending on edge cases.

## Authentication

Set `OPENAI_API_KEY` in the environment, or pass `--api-key` to the scripts.

```bash
export OPENAI_API_KEY="sk-proj-..."
```

The setup script writes the key to `~/.gpt-image/config.json` so the Python
scripts can load it without requiring a shell export.

## Parameters That Do NOT Exist

These are common copy-paste errors from other model docs:

- `aspect_ratio` -- use `size` instead
- `imageSize` (Gemini-style) -- OpenAI uses `size` and `quality` separately
- `negative_prompt` -- use semantic reframing (see prompt-engineering.md)
- `seed` -- not currently exposed for gpt-image-2; verify in latest docs
- `style` (DALL-E 3 style param) -- not present on gpt-image-2

## Output Directory

All generated images are saved to: `~/Documents/gpt_image_generated/`

Filenames are timestamped:
- New images: `gptimage_YYYYMMDD_HHMMSS_microseconds.png`
- Edited images: `gptimage_edit_YYYYMMDD_HHMMSS_microseconds.png`

## Error Response Taxonomy

OpenAI returns JSON errors with this shape:
```json
{
  "error": {
    "code": "content_policy_violation",
    "message": "Your request was rejected as a result of our safety system.",
    "type": "invalid_request_error"
  }
}
```

| HTTP status | `error.code` | Meaning | Correct response |
|-------------|--------------|---------|------------------|
| 400 | `content_policy_violation` | Prompt blocked by content policy | Apply safety rephrase, retry with user approval |
| 400 | `moderation_blocked` | Generated image blocked by output moderation | Shift visual concept further from trigger |
| 400 | `invalid_request_error` | Bad parameter (wrong size, quality, etc.) | Fix the parameter |
| 401 | `invalid_api_key` | API key missing or wrong | Generate new key at https://platform.openai.com/api-keys |
| 429 | `rate_limit_exceeded` | Too many requests | Exponential backoff (2s, 4s, 8s); check tier at https://platform.openai.com/account/limits |
| 500/502/503 | various | Transient server error | Retry with backoff; check https://status.openai.com |

## Multipart Construction (for edits)

`scripts/edit.py` constructs `multipart/form-data` manually using `urllib`
(no `requests` or `httpx`). The boundary format is:
```
--<boundary>
Content-Disposition: form-data; name="prompt"

<value>
--<boundary>
Content-Disposition: form-data; name="image"; filename="src.png"
Content-Type: image/png

<binary bytes>
--<boundary>--
```

If you need to add a `mask` field, follow the same `name="mask"; filename=...`
pattern with the mask file bytes.

## Rate Limit Guidance

Rate limits scale with your usage tier. View yours at
https://platform.openai.com/account/limits.

On HTTP 429, the scripts back off automatically: 2s, 4s, 8s, up to 3 retries.
After that, they exit with a JSON error message. For sustained heavy use,
consider:
- Lower-quality drafts (`--quality low`)
- Spreading work across time
- Upgrading usage tier (cumulative spend unlocks higher tiers)
