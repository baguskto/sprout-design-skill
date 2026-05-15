#!/usr/bin/env python3
"""
Setup script for GPT Image Claude.

Prompts for OPENAI_API_KEY and writes it to ~/.gpt-image/config.json so
the generate/edit scripts can load it without requiring a shell export.
Also prints a shell-export hint for the user's profile.

Usage:
    python3 setup.py                    # Interactive
    python3 setup.py --key YOUR_KEY     # Non-interactive
    python3 setup.py --check            # Verify existing setup
    python3 setup.py --remove           # Remove stored key
    python3 setup.py --test             # Run a tiny test generation (~$0.011)
    python3 setup.py --help             # Show usage
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".gpt-image"
CONFIG_PATH = CONFIG_DIR / "config.json"
SCRIPT_DIR = Path(__file__).resolve().parent


def load_config() -> dict:
    """Load config.json."""
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config: dict) -> None:
    """Save config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    CONFIG_PATH.chmod(0o600)
    print(f"Config saved to {CONFIG_PATH} (mode 600)")


def mask_key(key: str) -> str:
    if not key:
        return "(not set)"
    if len(key) > 12:
        return key[:8] + "..." + key[-4:]
    return "(short/invalid)"


def check_setup() -> bool:
    """Check whether a key is configured."""
    cfg = load_config()
    key = cfg.get("OPENAI_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
    if key:
        print(f"OPENAI_API_KEY is configured: {mask_key(key)}")
        print(f"  Config file: {CONFIG_PATH}")
        print(f"  Env override: {'yes' if os.environ.get('OPENAI_API_KEY') else 'no'}")
        return True
    print("OPENAI_API_KEY is NOT configured.")
    return False


def remove_config() -> None:
    """Remove the stored key."""
    if CONFIG_PATH.exists():
        CONFIG_PATH.unlink()
        print(f"Removed {CONFIG_PATH}")
    else:
        print(f"{CONFIG_PATH} not found.")


def setup_key(api_key: str) -> None:
    """Store the API key."""
    if not api_key or not api_key.strip():
        print("Error: API key cannot be empty.")
        sys.exit(1)
    api_key = api_key.strip()
    cfg = load_config()
    cfg["OPENAI_API_KEY"] = api_key
    save_config(cfg)
    print()
    print("Setup complete.")
    print()
    print("Optional: add this to your shell profile for env-based access:")
    print()
    print(f'  export OPENAI_API_KEY="{mask_key(api_key)}"')
    print()
    print("Generated images will be saved to: ~/Documents/gpt_image_generated/")


def run_test_call(api_key: str) -> int:
    """Run a tiny 1024x1024 low-quality test call (~$0.011)."""
    print("Running test generation (~$0.011)...")
    generate_path = SCRIPT_DIR / "generate.py"
    proc = subprocess.run(
        [
            sys.executable, str(generate_path),
            "--prompt", "a single ripe banana on a plain white background, studio lighting, product photography",
            "--size", "1024x1024",
            "--quality", "low",
            "--api-key", api_key,
        ],
        capture_output=True, text=True,
    )
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


def main() -> None:
    parser = argparse.ArgumentParser(description="GPT Image Claude setup")
    parser.add_argument("--key", help="Provide API key non-interactively")
    parser.add_argument("--check", action="store_true", help="Verify existing setup")
    parser.add_argument("--remove", action="store_true", help="Remove stored API key")
    parser.add_argument("--test", action="store_true", help="Run a tiny test generation (~$0.011)")
    args = parser.parse_args()

    if args.check:
        check_setup()
        return

    if args.remove:
        remove_config()
        return

    api_key = args.key or os.environ.get("OPENAI_API_KEY")

    if not api_key:
        existing = load_config().get("OPENAI_API_KEY", "")
        if existing:
            print(f"Existing key found: {mask_key(existing)}")
            try:
                resp = input("Overwrite? [y/N]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nAborted.")
                sys.exit(1)
            if resp != "y":
                api_key = existing
        if not api_key:
            print("GPT Image Claude -- Setup")
            print("=" * 40)
            print()
            print("Get your API key at: https://platform.openai.com/api-keys")
            print()
            try:
                api_key = input("Enter your OpenAI API key: ")
            except (EOFError, KeyboardInterrupt):
                print("\nError: No input received. Provide a key with --key or set OPENAI_API_KEY env var.")
                sys.exit(1)

    setup_key(api_key)

    if args.test:
        rc = run_test_call(api_key.strip())
        sys.exit(rc)


if __name__ == "__main__":
    main()
