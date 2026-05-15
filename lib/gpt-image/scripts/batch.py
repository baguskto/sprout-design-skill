#!/usr/bin/env python3
"""GPT Image Claude -- CSV Batch Workflow

Parse a CSV file of image generation requests and output a structured plan.
Claude then executes each row via generate.py.

Usage:
    batch.py --csv path/to/file.csv

CSV columns:
    prompt (required), size, quality, model, preset (all optional)

Example CSV:
    prompt,size,quality
    "coffee shop hero image",1536x1024,high
    "team photo placeholder",1024x1024,medium
    "product shot on marble",1024x1024,high
"""

import argparse
import csv
import json
import sys
from pathlib import Path

# Inline pricing for estimates (USD per image, approximate)
PRICING = {
    "gpt-image-2": {
        "1024x1024": {"low": 0.011, "medium": 0.042, "high": 0.167, "auto": 0.042},
        "1024x1536": {"low": 0.016, "medium": 0.063, "high": 0.250, "auto": 0.063},
        "1536x1024": {"low": 0.016, "medium": 0.063, "high": 0.250, "auto": 0.063},
        "auto":      {"low": 0.011, "medium": 0.042, "high": 0.167, "auto": 0.042},
    },
}
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_QUALITY = "high"


def estimate_cost(model, size, quality):
    """Estimate cost for a single image."""
    model_pricing = PRICING.get(model, PRICING[DEFAULT_MODEL])
    size_pricing = model_pricing.get(size, model_pricing.get(DEFAULT_SIZE, {}))
    return size_pricing.get(quality, size_pricing.get(DEFAULT_QUALITY, 0.167))


def main():
    parser = argparse.ArgumentParser(description="Parse CSV batch and output generation plan")
    parser.add_argument("--csv", required=True, help="Path to CSV file")
    args = parser.parse_args()

    csv_path = Path(args.csv).resolve()
    if not csv_path.exists():
        print(json.dumps({"error": True, "message": f"CSV not found: {csv_path}"}))
        sys.exit(1)

    rows = []
    errors = []

    try:
        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "prompt" not in reader.fieldnames:
                print(json.dumps({"error": True, "message": "CSV must have a 'prompt' column header"}))
                sys.exit(1)
            for i, row in enumerate(reader, start=2):
                prompt = row.get("prompt", "").strip()
                if not prompt:
                    errors.append(f"Row {i}: missing prompt")
                    continue

                rows.append({
                    "row": i,
                    "prompt": prompt,
                    "size": row.get("size", "").strip() or DEFAULT_SIZE,
                    "quality": row.get("quality", "").strip() or DEFAULT_QUALITY,
                    "model": row.get("model", "").strip() or DEFAULT_MODEL,
                    "preset": row.get("preset", "").strip() or None,
                })
    except (csv.Error, UnicodeDecodeError) as e:
        print(json.dumps({"error": True, "message": f"Failed to parse CSV: {e}"}))
        sys.exit(1)

    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
        if not rows:
            sys.exit(1)
        print()

    total_cost = sum(estimate_cost(r["model"], r["size"], r["quality"]) for r in rows)

    print(json.dumps({"rows": rows, "total_count": len(rows),
                       "estimated_cost": round(total_cost, 3),
                       "errors": errors}, indent=2))


if __name__ == "__main__":
    main()
