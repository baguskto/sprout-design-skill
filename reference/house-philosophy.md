# House Philosophy

Sprout's design baseline. Read before any verb that builds or edits UI.

## 1. Pick a bold aesthetic direction. Commit to it.

Before laying down a single component, decide what this thing wants to feel like. Don't drift into a generic "modern SaaS" default — that's how every AI-generated interface ends up looking like a slightly different shade of the same Linear clone. Pick a flavor and commit.

Flavor examples (not an exhaustive list — invent your own):

- **Brutalist** — exposed grids, raw type, no decoration, monospace for everything numeric.
- **Editorial** — magazine spreads, generous serifs for display, asymmetric columns, oversized pull quotes.
- **Retro-futuristic** — 80s terminal greens, scan lines, blocky type, intentional CRT artifacts.
- **Organic** — soft blobs, hand-drawn iconography, warm desaturated palette, irregular spacing.
- **Luxury** — extreme negative space, thin display weights, restrained gold/champagne accent, slow easing.
- **Cyber-utility** — Vercel-core meets terminal: dense data, micro-charts everywhere, monospace, single neon accent.
- **Editorial-tech** — Stripe-style: clean sans pairing, subtle gradients, choreographed scroll, illustrative SVG.
- **Bauhaus-digital** — primary colors, geometric blocks, strict grid, Futura-adjacent display.

The flavor is not a mood board; it's a constraint. It tells you which patterns from `arsenal.md` are admissible and which would clash. A brutalist landing page does not get magnetic buttons. A luxury dashboard does not get neon glow.

## 2. Differentiate or be forgettable.

If the output could plausibly belong to ten other YC companies, it has failed. The product's value lives in its surface — the surface has to claim territory.

Check yourself: "Does this look like the default Vercel template? Does this look like a shadcn demo? Does this look like the first result on Dribbble for 'SaaS dashboard'?" If yes to any, change the most generic component first (usually the hero, the card grid, or the type pairing).

## 3. Match implementation complexity to aesthetic.

A brutalist site needs almost no JS — just sharp type and ruthless grid. A cyber-utility dashboard needs real motion, real perpetual micro-interactions, real Framer Motion choreography. Don't ship Framer Motion in a brutalist site (the motion fights the aesthetic). Don't ship plain CSS transitions in a cinematic landing page (it'll feel hollow).

## 4. Vary across generations. Never converge on the same defaults.

The single most diagnostic signal of generic AI design is fontpair drift: every output ends up with Inter + Roboto Mono, every accent ends up a violet gradient, every hero ends up centered. Sprout's rule: **never converge**. Each project picks fonts the previous project did not use. The accent shifts hue family between projects. The hero composition rotates (asymmetric split, full-bleed image, type-only, video-bg, kinetic-marquee).

The dial system enforces this mechanically: variance > 4 bans centered hero, density > 7 bans card-overuse, motion > 5 mandates perpetual micro-interactions. The dials are the guardrail against default-drift.

## 5. Production-grade AND visually striking. Both, not either.

The code must compile, type-check, work on iOS Safari, hit 60fps on a mid-range Android, and not require dependencies the user has not installed. AND the surface must be memorable enough that someone scrolling past wants to stop. If you trade one for the other, the deliverable has failed. The dials and the anti-slop list exist precisely to prevent that trade.
