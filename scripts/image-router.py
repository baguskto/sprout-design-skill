#!/usr/bin/env python3
"""Image router for sprout-design.

Picks GPT Image 2 (text-heavy) or Gemini Nano Banana (photo-realistic) by
keyword-scoring the prompt, then invokes the matching engine script.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = Path.home() / "Documents" / "sprout-design-assets"
LOG_DIR = Path.home() / ".sprout-design"
LOG_FILE = LOG_DIR / "cost.jsonl"

TEXT_HEAVY_KEYWORDS = [
    "logo", "banner", "infographic", "poster",
    "headline", "typography", "text overlay",
    "with the text", "with copy", "diagram",
    "chart", "title card", "ad copy", "callout",
]
PHOTO_KEYWORDS = [
    "portrait", "photo", "photograph", "lifestyle",
    "photorealistic", "candid", "person ", "model ",
    "scene", "landscape", "interior", "product shot",
    "lookbook", "editorial photo",
]

GPT_COST_BY_QUALITY = {
    "low": 0.011,
    "medium": 0.042,
    "high": 0.167,
    "auto": 0.042,
}
BANANA_COST_ESTIMATE = 0.039


def pick_engine(prompt: str, override):
    if override in ("banana", "gpt"):
        return override
    p = prompt.lower()
    text_score = sum(k in p for k in TEXT_HEAVY_KEYWORDS)
    photo_score = sum(k in p for k in PHOTO_KEYWORDS)
    if text_score > photo_score:
        return "gpt"
    if photo_score > text_score:
        return "banana"
    return "gpt"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "default"


def estimate_cost(engine: str, quality: str) -> float:
    if engine == "gpt":
        return GPT_COST_BY_QUALITY.get(quality, GPT_COST_BY_QUALITY["auto"])
    return BANANA_COST_ESTIMATE


def log_cost(entry: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def run_gpt(prompt: str, size: str, quality: str, out_dir: Path):
    script = SKILL_DIR / "lib" / "gpt-image" / "scripts" / "generate.py"
    cmd = [
        "python3", str(script),
        "--prompt", prompt,
        "--size", size,
        "--quality", quality,
        "--output-dir", str(out_dir),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def run_banana(prompt: str, aspect_ratio: str, out_dir: Path):
    script = SKILL_DIR / "lib" / "banana" / "scripts" / "generate.py"
    cmd = [
        "python3", str(script),
        "--prompt", prompt,
        "--aspect-ratio", aspect_ratio,
        "--resolution", "2K",
        "--output-dir", str(out_dir),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def main():
    parser = argparse.ArgumentParser(description="sprout-design image router")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--engine", choices=["banana", "gpt"], default=None)
    parser.add_argument("--size", default="1024x1024",
                        choices=["1024x1024", "1024x1536", "1536x1024"])
    parser.add_argument("--quality", default="high",
                        choices=["low", "medium", "high", "auto"])
    parser.add_argument("--aspect-ratio", default="1:1")
    parser.add_argument("--project", default="default")
    args = parser.parse_args()

    engine = pick_engine(args.prompt, args.engine)
    project_slug = slugify(args.project)
    out_dir = ASSETS_DIR / project_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    if engine == "gpt":
        result = run_gpt(args.prompt, args.size, args.quality, out_dir)
    else:
        result = run_banana(args.prompt, args.aspect_ratio, out_dir)

    cost = estimate_cost(engine, args.quality)
    log_cost({
        "ts": int(time.time()),
        "engine": engine,
        "prompt": args.prompt[:80],
        "size": args.size if engine == "gpt" else args.aspect_ratio,
        "estimated_cost_usd": cost,
    })

    if result.returncode != 0:
        print(json.dumps({
            "error": True,
            "engine": engine,
            "stderr": result.stderr.strip(),
            "stdout": result.stdout.strip(),
        }))
        sys.exit(result.returncode)

    print(json.dumps({
        "path": str(out_dir),
        "engine": engine,
        "estimated_cost_usd": cost,
        "engine_output": result.stdout.strip(),
    }))


if __name__ == "__main__":
    main()
