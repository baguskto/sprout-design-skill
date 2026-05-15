# The Three Dials

Three integer dials, each on a 1–10 scale. They drive every aesthetic decision in the routing chain. Defaults are pinned in skill, overridable per session and per project.

## Sprout Defaults: `variance=7 motion=5 density=5`

**Why these values?** Sprout's portfolio (SixSeven, AuraCheck, TOCO) is B2B SaaS with dashboards, forms, and onboarding. The defaults are tuned for that context:

- `variance=7` — bolder than the safe baseline (centered hero, 3-column cards), forcing offset/asymmetric structures without going full art-gallery. Right for products that need to feel premium but still legible to enterprise buyers.
- `motion=5` — balanced. Fluid CSS transitions and `:hover` choreography are mandatory; full perpetual physics is optional. Right for dashboards where motion supports rather than dominates.
- `density=5` — normal app density. Standard padding, cards-when-justified, mono-for-numbers. Right for daily-use software.

Tune up for marketing pages (variance 8–9, motion 7–9, density 3–4). Tune down for data-heavy admin (variance 4, motion 3, density 8–9).

## DESIGN_VARIANCE (1–10)

How much the composition deviates from symmetrical, predictable layouts.

### 1–3 (Predictable)

Flexbox `justify-center`. Strict 12-column symmetrical grid. Equal paddings on all sides. Centered headers. 3-up card rows acceptable. This is the "no-surprise" register: legal pages, admin tables, enterprise settings panels.

### 4–7 (Offset)

Negative margins for intentional overlap (`margin-top: -2rem`). Varied image aspect ratios in the same row (e.g., 4:3 next to 16:9). Left-aligned headers paired with right-aligned data. Asymmetric padding (e.g., `pl-24 pr-8`). Centered hero is **BANNED** at this range — use split-screen, left/right content+asset, or asymmetric whitespace blocks.

### 8–10 (Asymmetric)

Masonry layouts. CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`). Massive empty zones (`padding-left: 20vw`). Type breaking out of its container. Editorial-style pull quotes. Reserved for hero pages and marketing surfaces where stopping power matters more than density.

### Mobile override (mandatory at variance ≥ 4)

Any asymmetric layout above the `md:` breakpoint MUST collapse to strict single-column (`w-full px-4 py-8`) below 768px. Asymmetric mobile is broken mobile.

## MOTION_INTENSITY (1–10)

How much movement the interface produces, both on user input and ambiently.

### 1–3 (Static)

No automatic animations. Only `:hover` and `:active` state transitions. Color shifts and `transform: scale(0.98)` on press. Right for terminal/brutalist aesthetics and accessibility-first surfaces.

### 4–7 (Fluid CSS)

`transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)` on interactive elements. `animation-delay` cascades for load-in. Strictly `transform` and `opacity` — never animate `width`, `height`, `top`, `left`. `will-change: transform` only where justified. No Framer Motion required.

### 8–10 (Advanced Choreography)

Scroll-triggered reveals via `IntersectionObserver` or Framer Motion `useScroll`. Parallax. Perpetual micro-interactions (pulse, typewriter, float, shimmer, infinite carousels) on standard components. Spring physics: `type: "spring", stiffness: 100, damping: 20`. Staggered orchestration with `staggerChildren`. **NEVER** use `window.addEventListener('scroll')` — always observer-based or motion-value-based to keep off the React render cycle.

## VISUAL_DENSITY (1–10)

How much content occupies a given pixel area.

### 1–3 (Art Gallery)

Lots of whitespace. Huge section gaps (`py-32` and up). Sparse type. Each element gets a lot of room. Right for luxury, marketing heroes, and meditation-app aesthetics.

### 4–7 (Daily App)

Normal padding for working software. `p-6` or `p-8` inside cards. Body type at `text-base leading-relaxed`. Mixed use of cards and bare lists. This is the default register for most B2B SaaS.

### 8–10 (Cockpit)

Tiny paddings. **No card containers** — use `border-t` and `divide-y` to separate data. Everything packed. **Mandatory:** all numerics in `font-mono`. Right for trading dashboards, analytics consoles, system-admin views. At density ≥ 8, generic card boxes are BANNED; use logic-grouping via borders and negative space.

## How the Dials Interact

- **High variance + high density** → asymmetric layouts inside dense data grids. Hard mode. Use Bento patterns from `arsenal.md` rather than freeform Masonry to keep it legible.
- **High variance + low density** → editorial / luxury register. Asymmetric layouts with massive negative space. Choose serif display + sans body if the flavor allows it.
- **High motion + high density** → mandatory `React.memo` + isolated Client Components for every perpetual animation. Density at 8+ means many active animation regions; un-memoized re-renders will tank framerate on mobile.
- **Low motion + high variance** → fine, but the static composition must do all the work. Type and color carry the weight.
- **High motion + low variance** → predictable layout with choreographed motion. Common for product walkthroughs and demo pages.

## Override Precedence

1. `DESIGN.md` frontmatter (`dials:` block) — pinned to the project.
2. CLI flags on the command (`--variance=N --motion=N --density=N`) — one command only.
3. Session `tune` (`/sprout-design tune 9 7 4`) — until the session ends or another `tune`.
4. Skill defaults (`7/5/5`) — when nothing else is set.
