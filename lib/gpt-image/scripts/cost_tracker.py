#!/usr/bin/env python3
"""GPT Image Claude -- Cost Tracker

Track image generation costs, view summaries, and estimate batch costs.

Usage:
    cost_tracker.py log --model MODEL --size SIZE --quality QUALITY --prompt "summary"
    cost_tracker.py summary
    cost_tracker.py today
    cost_tracker.py estimate --model MODEL --size SIZE --quality QUALITY --count N
    cost_tracker.py reset --confirm
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path.home() / ".gpt-image" / "costs.json"

# Cost per image in USD (approximate, subject to change)
PRICING = {
    "gpt-image-2": {
        "1024x1024": {"low": 0.011, "medium": 0.042, "high": 0.167, "auto": 0.042},
        "1024x1536": {"low": 0.016, "medium": 0.063, "high": 0.250, "auto": 0.063},
        "1536x1024": {"low": 0.016, "medium": 0.063, "high": 0.250, "auto": 0.063},
        "auto":      {"low": 0.011, "medium": 0.042, "high": 0.167, "auto": 0.042},
    },
}

VALID_SIZES = {"1024x1024", "1024x1536", "1536x1024", "auto"}
VALID_QUALITIES = {"low", "medium", "high", "auto"}


def _load_ledger():
    """Load the cost ledger from disk."""
    if not LEDGER_PATH.exists():
        return {"total_cost": 0.0, "total_images": 0, "entries": [], "daily": {}}
    with open(LEDGER_PATH, "r") as f:
        return json.load(f)


def _save_ledger(ledger):
    """Save the cost ledger to disk."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)


def _lookup_cost(model, size, quality):
    """Look up cost for a model+size+quality combination."""
    model_pricing = PRICING.get(model)
    if not model_pricing:
        for key in PRICING:
            if key in model or model in key:
                model_pricing = PRICING[key]
                break
    if not model_pricing:
        print(f"Warning: Unknown model '{model}', using gpt-image-2 pricing", file=sys.stderr)
        model_pricing = PRICING["gpt-image-2"]

    if size not in VALID_SIZES:
        print(f"Warning: Unknown size '{size}', using 1024x1024 pricing", file=sys.stderr)
        size = "1024x1024"
    if quality not in VALID_QUALITIES:
        print(f"Warning: Unknown quality '{quality}', using high pricing", file=sys.stderr)
        quality = "high"

    return model_pricing[size][quality]


def cmd_log(args):
    """Log a generation to the ledger."""
    ledger = _load_ledger()
    cost = _lookup_cost(args.model, args.size, args.quality)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    entry = {
        "ts": now,
        "model": args.model,
        "size": args.size,
        "quality": args.quality,
        "cost": cost,
        "prompt": args.prompt[:100],
    }

    ledger["entries"].append(entry)
    ledger["total_cost"] = round(ledger["total_cost"] + cost, 4)
    ledger["total_images"] += 1

    if today not in ledger["daily"]:
        ledger["daily"][today] = {"count": 0, "cost": 0.0}
    ledger["daily"][today]["count"] += 1
    ledger["daily"][today]["cost"] = round(ledger["daily"][today]["cost"] + cost, 4)

    _save_ledger(ledger)
    print(json.dumps({"logged": True, "cost": cost, "total_cost": ledger["total_cost"],
                       "total_images": ledger["total_images"]}))


def cmd_summary(args):
    """Show cost summary."""
    ledger = _load_ledger()
    print(f"Total images: {ledger['total_images']}")
    print(f"Total cost:   ${ledger['total_cost']:.3f}")
    print()

    daily = ledger.get("daily", {})
    if daily:
        sorted_days = sorted(daily.keys(), reverse=True)[:7]
        print("Last 7 days:")
        for day in sorted_days:
            d = daily[day]
            print(f"  {day}: {d['count']} images, ${d['cost']:.3f}")
    else:
        print("No usage recorded yet.")


def cmd_today(args):
    """Show today's usage."""
    ledger = _load_ledger()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    daily = ledger.get("daily", {}).get(today, {"count": 0, "cost": 0.0})
    print(f"Today ({today}): {daily['count']} images, ${daily['cost']:.3f}")


def cmd_estimate(args):
    """Estimate cost for a batch."""
    cost_per = _lookup_cost(args.model, args.size, args.quality)
    total = round(cost_per * args.count, 3)
    print(f"Model:      {args.model}")
    print(f"Size:       {args.size}")
    print(f"Quality:    {args.quality}")
    print(f"Count:      {args.count}")
    print(f"Cost/image: ${cost_per:.3f}")
    print(f"Total est:  ${total:.3f}")


def cmd_reset(args):
    """Reset the ledger."""
    if not args.confirm:
        print("Error: Pass --confirm to reset the cost ledger.", file=sys.stderr)
        sys.exit(1)
    _save_ledger({"total_cost": 0.0, "total_images": 0, "entries": [], "daily": {}})
    print("Cost ledger reset.")


def main():
    parser = argparse.ArgumentParser(description="GPT Image Claude Cost Tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Log a generation")
    p_log.add_argument("--model", required=True, help="Model ID")
    p_log.add_argument("--size", required=True, help="Size (1024x1024, 1024x1536, 1536x1024, auto)")
    p_log.add_argument("--quality", required=True, help="Quality (low, medium, high, auto)")
    p_log.add_argument("--prompt", required=True, help="Brief prompt description")

    sub.add_parser("summary", help="Show cost summary")
    sub.add_parser("today", help="Show today's usage")

    p_est = sub.add_parser("estimate", help="Estimate batch cost")
    p_est.add_argument("--model", required=True, help="Model ID")
    p_est.add_argument("--size", required=True, help="Size")
    p_est.add_argument("--quality", required=True, help="Quality")
    p_est.add_argument("--count", required=True, type=int, help="Number of images")

    p_reset = sub.add_parser("reset", help="Reset cost ledger")
    p_reset.add_argument("--confirm", action="store_true", help="Confirm reset")

    args = parser.parse_args()
    cmds = {"log": cmd_log, "summary": cmd_summary, "today": cmd_today,
            "estimate": cmd_estimate, "reset": cmd_reset}
    cmds[args.command](args)


if __name__ == "__main__":
    main()
