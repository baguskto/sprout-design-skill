# Unified Anti-Slop List

The merged ban list from impeccable, taste-skill's AI Tells, and Anthropic's frontend-design. Read before any verb that builds or edits code. Each entry uses REJECT / ALLOW WHEN / REPLACE WITH so the override path is explicit.

## TYPOGRAPHY

### REJECT: Inter, Roboto, Arial, system-ui as display font
- **Why:** Highest-frequency AI tells. Every generic dashboard ships with Inter.
- **ALLOW WHEN:** Project's `DESIGN.md` explicitly specifies one of them with a documented reason (e.g., legacy brand alignment).
- **REPLACE WITH:** Cabinet Grotesk, Geist, Satoshi, Outfit, Tobias, GT America, Söhne, IBM Plex Sans (for display). For dashboards specifically, Geist Sans + Geist Mono is the house default.

### REJECT: Inter for body text on "premium" or "creative" surfaces
- **REPLACE WITH:** Geist Sans, Söhne, system-ui in that order. Inter is acceptable only on developer-utility surfaces where neutral legibility is the goal.

### REJECT: Serif display on dashboards / software UI
- **Why:** Reads as marketing-template inside an app shell.
- **ALLOW WHEN:** Editorial or luxury flavor explicitly chosen.
- **REPLACE WITH:** Sans-serif display pair (Cabinet Grotesk + Geist Mono or Satoshi + JetBrains Mono).

### REJECT: Oversized H1 ("scream heading")
- **Why:** `text-9xl font-black` is a panic move, not a hierarchy decision.
- **REPLACE WITH:** Control hierarchy with weight (400 vs 700) and color contrast, not just scale. Display max `text-4xl md:text-6xl tracking-tighter leading-none`.

### REJECT: Convergence on Space Grotesk as the "safe creative" font
- **Why:** It's the new Inter — overused once everyone realized Inter was overused.
- **REPLACE WITH:** Rotate through Cabinet Grotesk, Tobias, GT America, Söhne, Geist across projects. Never two projects in a row on the same display font.

## COLOR

### REJECT: Pure `#000000` and pure `#ffffff`
- **Why:** Reads as un-designed. Real interfaces always tint.
- **REPLACE WITH:** `oklch(0.05 0 0)` near-black, `oklch(0.99 0 0)` near-white. Or zinc-tinted (`oklch(0.15 0.01 240)` / `oklch(0.98 0.005 240)`).

### REJECT: Purple-blue gradient ("the AI Lila")
- **Why:** Single most diagnostic signal of generic AI output. `linear-gradient(135deg, #667eea, #764ba2)` and friends.
- **ALLOW WHEN:** Never, for hero/CTA. May appear as a subtle accent in data-viz with explicit user approval.
- **REPLACE WITH:** One singular accent in OKLCH at chroma 0.15–0.25, paired with neutral. Emerald (`oklch(0.7 0.18 145)`), electric blue (`oklch(0.65 0.2 240)`), deep rose (`oklch(0.6 0.2 20)`), etc. Pick one per project, don't mix.

### REJECT: Oversaturated accent (`#ff0000`, `#00ff00`, `#0000ff`)
- **REPLACE WITH:** Desaturated OKLCH (chroma ≤ 0.25). Saturation in HSL terms must stay under 80%.

### REJECT: Palette fluctuation within one project
- **Why:** Warm gray header + cool gray sidebar = obvious LLM stitch.
- **REPLACE WITH:** Pick zinc-tinted or stone-tinted neutrals globally. Document the chosen hue in `DESIGN.md`.

## LAYOUT

### REJECT: Centered hero with massive H1 above CTA when `variance > 4`
- **REPLACE WITH:** Split-screen (50/50 content+asset), asymmetric whitespace, left-aligned with negative-margin overlap, or full-bleed type-mask.

### REJECT: 3-column equal card row ("feature row")
- **Why:** The #1 generic SaaS layout.
- **ALLOW WHEN:** Variance ≤ 3 and the feature count is exactly 3 and the cards are visually customized (not stock shadcn).
- **REPLACE WITH:** 2-column zig-zag, Bento asymmetric grid, horizontal scroll gallery, or list with rich detail per row.

### REJECT: Card-overuse at `density > 7`
- **Why:** Cockpit-density data should not be boxed.
- **REPLACE WITH:** `border-t`, `divide-y`, negative space, or 1px line separators. Cards only when elevation (z-index) is functionally required.

### REJECT: Side-stripe colored border on cards
- **Why:** Bootstrap-era pattern. Reads as 2014 admin theme.
- **REPLACE WITH:** Full-bleed tinted background or no decoration.

### REJECT: Modal-first interactions for primary flows
- **Why:** Modals are a fallback, not an architecture.
- **REPLACE WITH:** Inline expansion, dedicated routes, sheet/drawer for secondary actions.

### REJECT: Hero-metric template ("99.99% uptime / 10k users / 5x faster" centered hero stats)
- **REPLACE WITH:** Embed metrics in context, not as a centered stat block.

### REJECT: Identical card grids across sections
- **Why:** Visually monotonous; reads as template.
- **REPLACE WITH:** Each section gets a structurally different composition (cards, list, gallery, bento).

### REJECT: `h-screen` on hero
- **Why:** Catastrophic iOS Safari layout-jump bug.
- **REPLACE WITH:** `min-h-[100dvh]`.

### REJECT: Flexbox percentage math (`w-[calc(33%-1rem)]`)
- **REPLACE WITH:** CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

## TEXT / COPY

### REJECT: Em dashes in UI copy
- **Why:** AI tell. Em dashes pile up in LLM output the way they don't in human writing.
- **REPLACE WITH:** Periods, commas, or restructure the sentence.

### REJECT: Filler verbs — "Elevate", "Seamless", "Unleash", "Unlock", "Empower", "Next-Gen", "Revolutionize", "Supercharge"
- **REPLACE WITH:** Concrete verbs tied to the actual product action (Capture, Route, Reconcile, Quote, Resolve).

### REJECT: Generic names — "John Doe", "Sarah Chan", "Jack Su", "Jane Smith"
- **REPLACE WITH:** Realistic, culturally varied names that don't read as stock.

### REJECT: Generic startup names — "Acme", "Nexus", "SmartFlow", "TechCorp"
- **REPLACE WITH:** Contextual names that fit the simulated industry.

### REJECT: Fake-perfect metrics — `99.99%`, `50%`, `1000+`, `1234567890`
- **REPLACE WITH:** Organic, messy numbers (`47.2%`, `1,847`, `+1 (312) 847-1928`).

## MOTION

### REJECT: Default `box-shadow` outer glow ("neon glow")
- **REPLACE WITH:** Inner border (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) for elevation, tinted ambient shadow for depth.

### REJECT: Custom mouse cursors
- **Why:** Performance hit, accessibility regression, dated aesthetic.
- **ALLOW WHEN:** Never on production product surfaces. Acceptable in single-page art experiments only.

### REJECT: `window.addEventListener('scroll')` for parallax / scroll animations
- **REPLACE WITH:** `IntersectionObserver` or Framer Motion `useScroll` / `useMotionValueEvent`.

## EFFECTS

### REJECT: Glassmorphism as default decoration
- **Why:** `backdrop-blur` slapped on everything reads as 2021 macOS-template.
- **ALLOW WHEN:** There is real content behind the glass that benefits from refraction (true overlay on imagery).
- **REPLACE WITH:** When justified, add inner border (`border-white/10`) and inner highlight (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) to simulate physical edge refraction. Don't just `backdrop-blur`.

### REJECT: Gradient text on display headers
- **REPLACE WITH:** Solid color in OKLCH. Reserve gradient strokes for small annotation type only.

### REJECT: Decorative grain on scrolling containers
- **Why:** Continuous GPU repaint kills mobile.
- **ALLOW WHEN:** Grain is on a fixed `pointer-events-none` overlay outside the scroll context.

## IMAGES

### REJECT: Unsplash URLs in code
- **Why:** Links break, attribution is missing, and AI consistently picks the same 12 photos.
- **REPLACE WITH:** Generated assets via `scripts/image-router.py`, or `https://picsum.photos/seed/{stable_seed}/800/600` for placeholders.

### REJECT: Emoji as iconography (anywhere)
- **Why:** Inconsistent cross-platform rendering, dated, accessibility issues.
- **REPLACE WITH:** `@phosphor-icons/react` or `@radix-ui/react-icons`, strokeWidth 1.5.

### REJECT: Lucide default user icon ("egg avatar") as avatar fallback
- **REPLACE WITH:** Generated initials avatar with a hashed accent color, or a creative placeholder photo.

## CODE

### REJECT: Tailwind v4 syntax in a v3 project (or vice versa)
- **REPLACE WITH:** Check `package.json` first. Use v4 features (`@tailwindcss/postcss`, native CSS layers) only when v4 is installed.

### REJECT: Importing a library that isn't in `package.json`
- **REPLACE WITH:** Output the `npm install` command first, then the code. Never assume `framer-motion`, `lucide-react`, `zustand`, etc. are present.

### REJECT: Spamming `z-50` / `z-10` without a layer system
- **REPLACE WITH:** Reserve z-indexes for systemic layers (sticky nav, modal, toast). Document them once.

### REJECT: Animating `width`, `height`, `top`, `left`
- **Why:** Triggers layout. Not hardware-accelerated.
- **REPLACE WITH:** Animate `transform` and `opacity` only.

### REJECT: Default shadcn/ui components untouched
- **Why:** Instantly recognizable.
- **REPLACE WITH:** Customize radii, colors, shadows, and typography to project tokens before shipping.

### REJECT: `useState` for magnetic / continuous animations
- **Why:** Re-renders 60 times per second collapse mobile.
- **REPLACE WITH:** Framer Motion `useMotionValue` + `useTransform` outside the React render cycle.
