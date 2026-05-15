# House Tokens

Sprout's default design tokens. Applied by every verb unless `DESIGN.md` overrides them. Override at project root, not in this file.

## Typography

- **Display:** Cabinet Grotesk (700, 600). Fallback chain: `Satoshi, "Inter Display", system-ui, sans-serif`.
- **Body:** Geist Sans. Fallback: `system-ui, -apple-system, sans-serif`.
- **Mono:** Geist Mono. Fallback: `ui-monospace, "JetBrains Mono", "SF Mono", monospace`.
- **Modular scale:** 1.333 (perfect fourth). Steps from `0.75rem` upward: 0.75, 1.0, 1.333, 1.777, 2.369, 3.157, 4.209, 5.61.
- **Body measure:** `max-width: 65ch` for paragraph blocks.
- **Display tracking:** `tracking-tight` to `tracking-tighter` depending on weight. Never default tracking on display.
- **Body leading:** `leading-relaxed` (1.625) for paragraphs, `leading-snug` (1.375) for UI labels.

## Color

OKLCH-restrained strategy. One accent per project, neutrals carry the load.

- **Neutral light foundation:** `oklch(0.98 0.005 240)` (background), `oklch(0.96 0.006 240)` (surface raised), `oklch(0.15 0.01 240)` (foreground primary).
- **Neutral dark foundation:** `oklch(0.13 0.008 240)` (background), `oklch(0.17 0.01 240)` (surface raised), `oklch(0.96 0.005 240)` (foreground primary).
- **Accent:** Exactly one per project. Saturation (chroma) in OKLCH `0.15–0.25`. Pick a hue family in `DESIGN.md`; do not mix two accent families.
- **Banned:** Pure `#000000` and pure `#ffffff`. Use `oklch(0.05 0 0)` and `oklch(0.99 0 0)` if true neutral is required.
- **Semantic:**
    - Success: `oklch(0.65 0.15 145)` (desaturated emerald).
    - Warning: `oklch(0.75 0.15 75)` (desaturated amber).
    - Error: `oklch(0.6 0.18 25)` (desaturated rose).
    - These are darkened/lightened for dark mode by ±0.1 lightness.

## Spacing

Tailwind scale, 0.25rem base. Standard steps: `1, 2, 3, 4, 6, 8, 12, 16, 24, 32` (in 0.25rem units → 0.25rem, 0.5rem, 0.75rem, 1rem, 1.5rem, 2rem, 3rem, 4rem, 6rem, 8rem).

- Page container: `max-w-[1400px] mx-auto px-6 md:px-10`.
- Section vertical rhythm: `py-16 md:py-24` standard, `py-24 md:py-32` for marketing.
- Card interior: `p-6` standard, `p-8` or `p-10` for hero cards.

## Radius

`0`, `4px`, `8px`, `12px`, `999px`.

- **Default card:** 8px.
- **Default button:** 999px (full pill).
- **Default input:** 8px.
- **Large surface (bento tile, hero card):** 12px or 2.5rem for the "Bento 2.0" register.
- **Hard-edge mode (brutalist / editorial flavor):** 0 across the board.

## Motion

- **Easings:**
    - `ease-out-quart`: `cubic-bezier(0.25, 1, 0.5, 1)` — default for state changes.
    - `ease-out-expo`: `cubic-bezier(0.16, 1, 0.3, 1)` — for confident layout transitions.
    - `spring (Framer):` `{ type: "spring", stiffness: 100, damping: 20 }` — for interactive elements at motion ≥ 6.
- **Durations:**
    - `150ms` — instant (hover, focus ring).
    - `300ms` — state change (modal open, accordion expand).
    - `500ms` — layout shift (route transition, sheet slide).
- Animate `transform` and `opacity` only.

## Icons

- **Preferred:** `@phosphor-icons/react`.
- **Acceptable:** `@radix-ui/react-icons`.
- **Banned:** Lucide default icons (overused), emoji as iconography.
- **Standardize:** `strokeWidth = 1.5` for Phosphor, `width/height = 16` or `20` consistently within a surface.

## How to override per project

Edit `DESIGN.md` in the project root. Frontmatter accepts:

```yaml
---
dials:
  variance: 9
  motion: 4
  density: 5
fonts:
  display: "Tobias"
  body: "Inter Display"
  mono: "JetBrains Mono"
palette:
  neutral_hue: 30          # warmer (stone-tinted) instead of 240 zinc-tinted
  accent: "oklch(0.65 0.2 25)"
  background_light: "oklch(0.985 0.008 30)"
spacing:
  base: "0.25rem"
  container_max: "1400px"
radius:
  card: "12px"
  button: "8px"
motion:
  default_duration: "200ms"
  default_easing: "cubic-bezier(0.16, 1, 0.3, 1)"
---
```

Any key absent from `DESIGN.md` falls back to the values defined above.
