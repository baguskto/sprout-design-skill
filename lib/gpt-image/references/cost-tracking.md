# Cost Tracking Reference

> Load this on-demand when the user asks about costs or before batch operations.
> Pricing is approximate and subject to change -- verify at https://openai.com/api/pricing

## Pricing Table (USD per image)

| Model | Size | Quality | Cost/Image |
|-------|------|---------|-----------|
| gpt-image-2 | 1024x1024 | low | $0.011 |
| gpt-image-2 | 1024x1024 | medium | $0.042 |
| gpt-image-2 | 1024x1024 | high | $0.167 |
| gpt-image-2 | 1024x1536 | low | $0.016 |
| gpt-image-2 | 1024x1536 | medium | $0.063 |
| gpt-image-2 | 1024x1536 | high | $0.250 |
| gpt-image-2 | 1536x1024 | low | $0.016 |
| gpt-image-2 | 1536x1024 | medium | $0.063 |
| gpt-image-2 | 1536x1024 | high | $0.250 |
| gpt-image-1 | any | n/a | cheaper, verify with provider |

Non-square sizes cost roughly 1.5x the equivalent square. `auto` is billed at
whatever the model selects -- the tracker logs the actual returned size.

## Rate Limits

Rate limits scale with usage tier. Check yours at
https://platform.openai.com/account/limits.

## Cost Tracker Commands

```bash
# Log a generation
cost_tracker.py log --model gpt-image-2 --size 1024x1024 --quality high --prompt "logo for Northbeam"

# View summary (total + last 7 days)
cost_tracker.py summary

# Today's usage
cost_tracker.py today

# Estimate before batch
cost_tracker.py estimate --model gpt-image-2 --size 1024x1024 --quality high --count 10

# Reset ledger
cost_tracker.py reset --confirm
```

## Storage

Ledger stored at `~/.gpt-image/costs.json`. Created automatically on first use.
