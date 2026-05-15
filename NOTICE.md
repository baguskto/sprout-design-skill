# NOTICE

`sprout-design` wraps and orchestrates the following dependencies. Their original `SKILL.md` files are bundled in `lib/` and remain under their respective licenses.

## impeccable

- Author: Paul Bakaus
- Version: 3.1.1
- License: Apache License 2.0
- Source: https://github.com/pbakaus/impeccable
- Location: `lib/impeccable/`

Provides the 23-verb design workflow (craft, shape, audit, critique, polish, bolder, quieter, distill, harden, animate, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, onboard, teach, document, extract, live). `sprout-design` routes verbs to `lib/impeccable/reference/<verb>.md` rather than re-implementing them.

A copy of the Apache 2.0 license is included in `lib/impeccable/LICENSE` (or the upstream repository). Use of impeccable is subject to that license.

## taste-skill

- Bundled at `lib/taste-skill/`

`sprout-design` extracts the dial system (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY) and the Creative Arsenal pattern catalog into `reference/dials.md` and `reference/arsenal.md`. Content is reworded and re-grouped in Sprout's voice rather than copied verbatim.

## banana

- Bundled at `lib/banana/`

Google Gemini Nano Banana image generation. Invoked by `scripts/image-router.py` when prompts are photo-realistic.

## gpt-image

- Bundled at `lib/gpt-image/`

OpenAI GPT Image 2 generation. Invoked by `scripts/image-router.py` when prompts are text-heavy (logos, banners, infographics).

## frontend-design (Anthropic)

The philosophical seed for `reference/house-philosophy.md` — the "pick a bold aesthetic direction, differentiate or be forgettable" framing — is adapted from Anthropic's `frontend-design` skill. Not bundled. Principle is rephrased in Sprout's voice.

## Summary

`sprout-design` is the conductor. It does not redistribute upstream code under its own license; each dependency under `lib/` retains its original license. The Sprout-authored material — `SKILL.md`, `reference/*.md`, `scripts/*` — is internal to Sprout.
