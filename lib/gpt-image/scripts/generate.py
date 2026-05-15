#!/usr/bin/env python3
"""GPT Image Claude -- Direct API: Image Generation

Generate images via OpenAI Images API.
Uses only Python stdlib (no pip dependencies).

Usage:
    generate.py --prompt "a cat in space" [--size 1024x1024] [--quality high]
                [--model MODEL] [--api-key KEY]
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_QUALITY = "high"
OUTPUT_DIR = Path.home() / "Documents" / "gpt_image_generated"
API_URL = "https://api.openai.com/v1/images/generations"
CONFIG_PATH = Path.home() / ".gpt-image" / "config.json"

VALID_SIZES = {"1024x1024", "1024x1536", "1536x1024", "auto"}
VALID_QUALITIES = {"low", "medium", "high", "auto"}


def load_api_key(cli_key=None):
    """Resolve API key from CLI, env, or config file."""
    if cli_key:
        return cli_key
    env = os.environ.get("OPENAI_API_KEY")
    if env:
        return env
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                cfg = json.load(f)
            key = cfg.get("OPENAI_API_KEY", "")
            if key:
                return key
        except (json.JSONDecodeError, OSError):
            pass
    return None


def generate_image(prompt, model, size, quality, api_key):
    """Call OpenAI Images API to generate an image."""
    body = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "n": 1,
    }

    data = json.dumps(body).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    max_retries = 3
    result = None
    for attempt in range(max_retries):
        req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            try:
                err_json = json.loads(error_body)
                err_code = err_json.get("error", {}).get("code", "")
                err_msg = err_json.get("error", {}).get("message", error_body)
            except json.JSONDecodeError:
                err_code = ""
                err_msg = error_body

            if e.code == 429 and attempt < max_retries - 1:
                wait = 2 ** (attempt + 1)
                print(json.dumps({"retry": True, "attempt": attempt + 1, "wait_seconds": wait, "reason": "rate_limited"}), file=sys.stderr)
                time.sleep(wait)
                continue
            if e.code == 401:
                print(json.dumps({"error": True, "status": 401, "code": err_code, "message": "Invalid API key. Generate a new one at https://platform.openai.com/api-keys"}))
                sys.exit(1)
            if err_code in ("content_policy_violation", "moderation_blocked"):
                print(json.dumps({"error": True, "status": e.code, "code": err_code, "message": err_msg}))
                sys.exit(1)
            print(json.dumps({"error": True, "status": e.code, "code": err_code, "message": err_msg}))
            sys.exit(1)
        except urllib.error.URLError as e:
            print(json.dumps({"error": True, "message": str(e.reason)}))
            sys.exit(1)

    if result is None:
        print(json.dumps({"error": True, "message": "Max retries exceeded"}))
        sys.exit(1)

    data_arr = result.get("data", [])
    if not data_arr:
        print(json.dumps({"error": True, "message": "No data in response"}))
        sys.exit(1)

    b64 = data_arr[0].get("b64_json")
    if not b64:
        print(json.dumps({"error": True, "message": "No b64_json in response"}))
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"gptimage_{timestamp}.png"
    output_path = (OUTPUT_DIR / filename).resolve()

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(b64))

    return {
        "path": str(output_path),
        "model": model,
        "size": size,
        "quality": quality,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate images via OpenAI Images API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--size", default=DEFAULT_SIZE, help=f"Size: 1024x1024, 1024x1536, 1536x1024, auto (default: {DEFAULT_SIZE})")
    parser.add_argument("--quality", default=DEFAULT_QUALITY, help=f"Quality: low, medium, high, auto (default: {DEFAULT_QUALITY})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-key", default=None, help="OpenAI API key (or set OPENAI_API_KEY env)")

    args = parser.parse_args()

    if args.size not in VALID_SIZES:
        print(json.dumps({"error": True, "message": f"Invalid size '{args.size}'. Valid: {sorted(VALID_SIZES)}"}))
        sys.exit(1)

    if args.quality not in VALID_QUALITIES:
        print(json.dumps({"error": True, "message": f"Invalid quality '{args.quality}'. Valid: {sorted(VALID_QUALITIES)}"}))
        sys.exit(1)

    api_key = load_api_key(args.api_key)
    if not api_key:
        print(json.dumps({"error": True, "message": "No API key. Set OPENAI_API_KEY env, pass --api-key, or run setup.py"}))
        sys.exit(1)

    result = generate_image(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        quality=args.quality,
        api_key=api_key,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
