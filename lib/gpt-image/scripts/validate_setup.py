#!/usr/bin/env python3
"""
Validate that GPT Image Claude is properly configured.

Checks:
1. API key is reachable (env or config file)
2. Output directory exists or can be created
3. API key actually works (lightweight authenticated request)

Usage:
    python3 validate_setup.py
    python3 validate_setup.py --no-network    # Skip the live API check
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / ".gpt-image" / "config.json"
OUTPUT_DIR = Path.home() / "Documents" / "gpt_image_generated"
MODELS_URL = "https://api.openai.com/v1/models"


def check(label: str, passed: bool, detail: str = "") -> bool:
    status = "PASS" if passed else "FAIL"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f" -- {detail}"
    print(msg)
    return passed


def resolve_key() -> str:
    env = os.environ.get("OPENAI_API_KEY")
    if env:
        return env
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                cfg = json.load(f)
            return cfg.get("OPENAI_API_KEY", "")
        except (json.JSONDecodeError, OSError):
            return ""
    return ""


def network_check(api_key: str) -> tuple[bool, str]:
    """Hit /v1/models with the key to verify auth without spending image credits."""
    req = urllib.request.Request(
        MODELS_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            count = len(data.get("data", []))
            return True, f"{count} models accessible"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"Network error: {e.reason}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-network", action="store_true", help="Skip live API check")
    args = parser.parse_args()

    print("GPT Image Claude -- Setup Validation")
    print("=" * 40)
    results = []

    key = resolve_key()
    results.append(check(
        "OPENAI_API_KEY is set",
        bool(key),
        f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "(empty or short)",
    ))

    source = "env" if os.environ.get("OPENAI_API_KEY") else ("config" if CONFIG_PATH.exists() else "none")
    results.append(check(
        "API key source",
        source != "none",
        source,
    ))

    if OUTPUT_DIR.exists():
        results.append(check("Output directory exists", True, str(OUTPUT_DIR)))
    else:
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            results.append(check("Output directory created", True, str(OUTPUT_DIR)))
        except OSError as e:
            results.append(check("Output directory writable", False, str(e)))

    if key and not args.no_network:
        ok, detail = network_check(key)
        results.append(check("API key works (GET /v1/models)", ok, detail))

    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"\n{'=' * 40}")
    print(f"Results: {passed}/{total} checks passed")

    if passed == total:
        print("Status: Ready to generate images!")
        return 0
    else:
        print("Status: Some checks failed. Fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
