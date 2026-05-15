# Prompt Engineering Reference -- GPT Image Claude

> Load this on-demand when constructing complex prompts or when the user
> asks about prompt techniques. Do NOT load at startup.

## The 5-Component Prompt Formula

> A universally strong prompt structure. Write as natural narrative paragraphs --
> NEVER as comma-separated keyword lists.

### Component 1 -- SUBJECT
Who or what is the primary focus. Be specific about physical characteristics,
material, species, age, expression. Never write just "a person" or "a product."

**Good:** "A weathered Japanese ceramicist in his 70s, deep sun-etched
wrinkles mapping decades of kiln work, calloused hands cradling a
freshly thrown tea bowl with an irregular, organic rim"

**Bad:** "old man, ceramic, bowl"

### Component 2 -- ACTION
What the subject is doing, or the primary visual state. Use strong present-
tense verbs. "floats weightlessly," "holds a glowing lantern," "sits perfectly
still." If no action, describe pose or arrangement.

**Good:** "leaning forward with intense concentration, gently smoothing
the rim with a wet thumb, a thin trail of slip running down his wrist"

**Bad:** "making pottery"

### Component 3 -- LOCATION / CONTEXT
Where the scene takes place. Include environmental details, time of day,
atmospheric conditions. "inside the cupola module of the International Space
Station," "on a rain-slicked Tokyo alley at 2am."

**Good:** "inside a traditional wood-fired anagama kiln workshop,
stacked shelves of drying pots visible in the soft background, late
afternoon light filtering through rice paper screens"

**Bad:** "workshop, afternoon"

### Component 4 -- COMPOSITION
Camera perspective, framing, and spatial relationship. "medium shot centered
against the window," "extreme low-angle looking up," "bird's-eye view from
30 meters," "tight close-up on hands."

**Good:** "intimate close-up shot from slightly below eye level,
shallow depth of field isolating the hands and bowl against the
soft bokeh of the workshop behind"

**Bad:** "close up"

### Component 5 -- STYLE (includes lighting)
The visual register, aesthetic, medium, and lighting combined. Reference real
cameras, film stock, photographers, publications, or art movements. Lighting
lives here as a sub-element, not a separate component.

**Good:** "shot on a Fujifilm X-T4 with warm color science and natural
bokeh, warm directional light from a single high window camera-left
creating gentle Rembrandt lighting on the face with deep warm shadows.
Reminiscent of Dorothea Lange's documentary portraiture"

## GPT Image 2 Strengths

GPT Image 2 has two distinguishing capabilities you should lean on:

1. **Best-in-class text rendering.** It can produce typographically clean
   headlines, body copy, exact wordmarks, product labels, and infographic
   numerals reliably. Always quote text verbatim in the prompt.
2. **Layout reasoning ("thinking latent space").** It handles natural-language
   spatial instructions ("the chart sits in the lower-right, headline above,
   three-column footer with logo centered") better than purely diffusion-based
   models. Write layout as prose, not as cryptic keyword stacks.

GPT Image 2 is generally tolerant of common image-prompt keywords. You do not
need to scrub words like "photorealistic" or "high resolution" -- they're
mostly noise, but they don't actively degrade output. Prefer specific anchors
(camera, film, publication) over generic quality terms regardless.

## Domain Mode Modifier Libraries

### Cinema Mode
**Camera specs:** RED V-Raptor, ARRI Alexa 65, Sony Venice 2, Blackmagic URSA
**Lenses:** Cooke S7/i, Zeiss Supreme Prime, Atlas Orion anamorphic
**Film stocks:** Kodak Vision3 500T (tungsten), Kodak Vision3 250D (daylight), Fuji Eterna Vivid
**Lighting setups:** three-point, chiaroscuro, Rembrandt, split, butterfly, rim/backlight
**Shot types:** establishing wide, medium close-up, extreme close-up, Dutch angle, overhead crane, Steadicam tracking
**Color grading:** teal and orange, desaturated cold, warm vintage, high-contrast noir

### Product Mode
**Surfaces:** polished marble, brushed concrete, raw linen, acrylic riser, gradient sweep
**Lighting:** softbox diffused, hard key with fill card, rim separation, tent lighting, light painting
**Angles:** 45-degree hero, flat lay, three-quarter, straight-on, worm's-eye
**Style refs:** Apple product photography, Aesop minimal, Bang & Olufsen clean, luxury cosmetics

### Portrait Mode
**Focal lengths:** 85mm (classic), 105mm (compression), 135mm (telephoto), 50mm (environmental)
**Apertures:** f/1.4 (dreamy bokeh), f/2.8 (subject-sharp), f/5.6 (environmental context)
**Pose language:** candid mid-gesture, direct-to-camera confrontational, profile silhouette, over-shoulder glance
**Skin/texture:** freckles visible, pores at macro distance, catch light in eyes, subsurface scattering

### Editorial/Fashion Mode
**Publication refs:** Vogue Italia, Harper's Bazaar, GQ, National Geographic, Kinfolk
**Styling notes:** layered textures, statement accessories, monochromatic palette, contrast patterns
**Locations:** marble staircase, rooftop at golden hour, industrial loft, desert dunes, neon-lit alley
**Poses:** power stance, relaxed editorial lean, movement blur, fabric in wind

### UI/Web Mode
**Styles:** flat vector, isometric 3D, line art, glassmorphism, neumorphism, material design
**Colors:** specify exact hex or descriptive palette (e.g., "cool blues #2563EB to #1E40AF")
**Sizing:** design at 2x for retina, specify exact pixel dimensions needed
**Backgrounds:** transparent (request solid white then post-process), gradient, solid color

### Logo Mode (GPT Image 2 sweet spot)
**Construction:** geometric primitives, golden ratio, grid-based, negative space
**Typography:** bold sans-serif, elegant serif, custom lettermark, monogram
**Colors:** max 2-3 colors, works in monochrome, high contrast
**Output:** request on solid white background, post-process to transparent
**Text:** quote the wordmark exactly -- GPT Image 2 will reliably spell it

### Landscape Mode
**Depth layers:** foreground interest, midground subject, background atmosphere
**Atmospherics:** fog, mist, haze, volumetric light rays, dust particles
**Time of day:** blue hour (pre-dawn), golden hour, magic hour (post-sunset), midnight blue
**Weather:** dramatic storm clouds, clearing after rain, snow-covered, sun-dappled

### Infographic Mode (GPT Image 2 sweet spot)
**Layout:** modular sections, clear visual hierarchy, bento grid, flow top-to-bottom
**Text:** use quotes for exact text, descriptive font style, specify size hierarchy
**Data viz:** bar charts, pie charts, flow diagrams, timelines, comparison tables
**Colors:** high-contrast, accessible palette, consistent brand colors

### Abstract Mode
**Geometry:** fractals, voronoi tessellation, spirals, fibonacci, organic flow, crystalline
**Textures:** marble veining, fluid dynamics, smoke wisps, ink diffusion, watercolor bleed
**Color palettes:** analogous harmony, complementary clash, monochromatic gradient, neon-on-black
**Styles:** generative art, data visualization art, glitch, procedural, macro photography of materials

## Advanced Techniques

### Character Consistency (across calls)
The API is stateless. To keep a character consistent across calls:
- First call: Generate the character with exhaustive physical description
- Following calls: Repeat the exact same identifying anchors verbatim
  (hair color/style, distinctive clothing, facial features, age, ethnicity)
- For higher fidelity, use `edit.py` against a previously generated image
  with delta instructions ("same woman, now wearing a navy suit in a boardroom")

### Style Transfer Without Reference Images
Describe the target style exhaustively:
```
Render this scene in the style of a 1950s travel poster: flat areas of
color in a limited palette of teal, coral, and cream. Bold geometric
shapes with visible paper texture. Hand-lettered title text with a
mid-century modern typeface feel.
```

### Text Rendering Tips (GPT Image 2)
GPT Image 2 renders typography reliably. To get the best results:
- Quote exact text: `with the text "OPEN DAILY" in bold condensed sans-serif`
- Specify font character: weight, serif/sans, style era, hand-drawn vs geometric
- Specify placement: "centered at the top third", "along the bottom edge", "lower-right corner"
- Specify size hierarchy explicitly when multiple text elements exist
- High contrast: light text on dark, or vice versa
- For paragraphs of body copy, place them in a clearly defined block region
  ("a left column 40% of the canvas width, body copy in 14pt serif")
- Very small text (<16px equivalent) may still need iteration

GPT Image 2 handles longer copy better than most models, but extremely dense
paragraphs may still degrade. If the asset is text-driven (infographic,
typographic poster), use `quality: "high"`.

### Positive Framing (No Negative Prompts)
The OpenAI image API has no `negative_prompt` parameter. Rephrase exclusions:
- Instead of "no blur" → "sharp, in-focus, tack-sharp detail"
- Instead of "no people" → "empty, deserted, uninhabited"
- Instead of "no text" → "clean, uncluttered, text-free"
- Instead of "not dark" → "brightly lit, high-key lighting"

For critical constraints, ALL CAPS emphasis improves adherence:
- "MUST contain exactly three figures"
- "NEVER include any visible horizon line"
- "ONLY show the product, nothing else in frame"

## Prompt Length Guide

| Use case | Target length | Notes |
|---|---|---|
| Quick draft / concept | 20–60 words (1–2 sentences) | Good for ideation |
| Standard generation | 100–200 words (3–5 sentences) | Production default |
| Complex professional | 200–400 words | Full 5-component treatment |
| Maximum specification | Up to ~4,000 chars | Verify current API max |

Do not artificially truncate a prompt to hit a word count target -- quality
and specificity matter more.

## Prompt Adaptation Rules

When adapting prompts from databases (Midjourney/DALL-E/etc.) to GPT Image 2's
natural-language format:

| Source Syntax | GPT Image 2 Equivalent |
|---------------|------------------------|
| `--ar 16:9` | Pick `size: "1536x1024"` and crop in post if needed |
| `--v 6`, `--style raw` | Remove -- GPT Image has no version/style flags |
| `--chaos 50` | Describe variety: "unexpected, surreal composition" |
| `--no trees` | Positive framing: "open clearing with no vegetation" |
| `(word:1.5)` weight | Descriptive emphasis: "prominently featuring [word]" |
| Comma-separated tags | Expand into descriptive narrative paragraphs |
| `shot on Hasselblad` | Keep -- camera specs work well |

## Common Prompt Mistakes

1. **Keyword stuffing** -- stacking generic quality terms helps less than specific anchors. Use camera models, lens specs, and prestigious context anchors instead.
2. **Tag lists** -- GPT Image 2 wants prose, not "red car, sunset, mountain, cinematic"
3. **Missing lighting** -- The single biggest quality differentiator
4. **No composition direction** -- Results in generic centered framing
5. **Vague style** -- "make it look cool" vs specific art direction
6. **Ignoring size** -- Pick a size that matches the use case before generating
7. **Burying key details at the end** -- In long prompts, place critical specifics (exact text, key constraints) in the first third
8. **Not iterating** -- Refine with `edit.py` rather than trying to get everything right in one generation
9. **Under-specifying text** -- If text matters, quote it exactly and describe font, placement, and size hierarchy

## Proven Prompt Templates

> Patterns that consistently produce high-quality results. Use as starting
> points and adapt to the request.

### The Winning Formula (Weight Distribution)

| Component | Weight | What to include |
|-----------|--------|-----------------|
| **Subject** | 30% | Age, skin tone, hair color/style, eye color, body type, expression |
| **Action** | 10% | Movement, pose, gesture, interaction, state of being |
| **Context** | 15% | Location + time of day + weather + context details |
| **Composition** | 10% | Shot type, camera angle, framing, focal length, f-stop |
| **Lighting** | 10% | Quality, direction, color temperature, shadows |
| **Style** | 25% | Art medium, brand names, textures, camera model, color grading |

### Instagram Ad / Social Media

**Pattern:** `[Subject with age/appearance] + [outfit with brand/texture] + [action verb] + [setting] + [camera spec] + [lighting] + [platform aesthetic]`

**Example (Product Placement):**
```
Hyper-realistic gym selfie of athletic 24yo influencer with glowing olive
skin, wearing crinkle-textured athleisure set in mauve. iPhone 16 Pro Max
front-facing portrait mode capturing sweat droplets on collarbones, hazel
eyes enhanced by gym LED lighting. Mirror reflection shows perfect form,
golden morning light through floor-to-ceiling windows. Frayed chestnut
ponytail with baby hairs, visible skin texture with natural erythema from
workout. Vanity Fair wellness editorial aesthetic.
```

**Example (Lifestyle Ad):**
```
A 24-year-old blonde fitness model in a high-energy sports drink
advertisement. Mid-run on a beach, wearing a vibrant orange sports bra
and black shorts, playful smile and sparkling blue eyes exuding vitality.
Bottle of the drink held in hand, waves crashing in background. Shot on
Nikon D850 with 70-200mm f/2.8 lens, natural light, fast shutter speed
capturing motion. Visible skin texture, water droplets, product label
clearly visible. National Geographic fitness feature aesthetic.
```

### Product / Commercial Photography

**Pattern:** `[Product with brand/detail] + [dynamic elements] + [surface/setting] + "commercial photography for advertising campaign" + [lighting] + [prestigious publication reference]`

**Example (Beverage):**
```
Gatorade bottle with condensation dripping down the sides, surrounded by
lightning bolts and a burst of vibrant blue and orange light rays. The
Gatorade logo is prominently displayed on the bottle, with splashes of
water frozen in mid-air. Commercial food photography for an advertising
campaign, vibrant complementary colors. Bon Appetit magazine cover aesthetic.
```

### Fashion / Editorial

**Pattern:** `[Subject with ethnicity/age/features] + [outfit with texture/brand/cut] + [location] + [pose/action] + [camera + lens] + [lighting quality]`

**Example (Street Style):**
```
A 24-year-old female AI influencer posing confidently in an urban cityscape
during golden hour. Flawless sun-kissed skin, long wavy brown hair, deep
green eyes. Wearing a chic streetwear outfit -- oversized beige blazer,
white top, high-waisted jeans. Captured with Sony A7R IV at 85mm f/1.4,
shallow depth of field with warm golden bokeh.
```

### SaaS / Tech Marketing

**Pattern:** `[UI mockup or abstract visual] + "on [dark/light] background" + [specific colors with hex] + [typography description] + "clean, premium SaaS aesthetic"`

**Example (Dashboard Hero):**
```
A floating glassmorphism UI card on a deep charcoal background showing a
content analytics dashboard with the title "REVENUE PULSE" in bold white
sans-serif at the top, a rising line graph in teal (#14B8A6), bar charts
in coral (#F97316), and a circular progress indicator at 94%. Subtle grid
lines, frosted glass effect with 20% opacity, teal glow bleeding from the
card edges. Clean premium SaaS aesthetic.
```

### Logo / Branding (GPT Image 2 sweet spot)

**Pattern:** `[Logo construction] + "with the wordmark "[EXACT TEXT]" in [font description]" + [color palette] + [layout] + [output spec]`

**Example:**
```
A minimalist tech startup logo featuring a geometric mark of three
overlapping triangles forming an upward arrow, paired with the wordmark
"NORTHBEAM" in a bold modern geometric sans-serif. Two-color palette:
deep indigo #1E1B4B for the mark and wordmark, on a clean white
background. Wordmark sits horizontally to the right of the mark with
generous letter-spacing. Vector-style flat illustration, sharp clean
edges, suitable for scaling.
```

### Infographic with Exact Text

**Pattern:** `[Layout description] + [each text block quoted exactly with placement] + [chart description] + [palette] + [overall aesthetic]`

**Example:**
```
A clean modern infographic on a soft cream background (#FAFAF5) titled
"2026 STATE OF AI" in bold black sans-serif centered at the top. Three
horizontal sections stacked vertically, each with a numeric stat:
"78%" in large coral red (#FF3B30) on the left with the label "of
teams use AI daily" in smaller black serif on the right; "$4.2B" in
the second row with "invested in image generation startups"; "12x" in
the third row with "faster prototype-to-ship cycles". Thin horizontal
dividers between sections. Editorial magazine aesthetic, generous
whitespace, no decorative illustrations.
```

### Key Tactics That Make Prompts Work

1. **Name real cameras** -- "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max" anchor realism
2. **Specify exact lens** -- "85mm f/1.4" gives the model precise depth-of-field information
3. **Use age + ethnicity + features** -- "24yo with olive skin, hazel eyes" beats "a person"
4. **Name brands for styling** -- "Lululemon mat", "Tom Ford suit" triggers specific visual associations
5. **Include micro-details** -- "sweat droplets on collarbones", "baby hairs stuck to neck"
6. **Add platform context** -- "Instagram aesthetic", "commercial photography for advertising"
7. **Describe textures** -- "crinkle-textured", "metallic silver", "frosted glass"
8. **Use action verbs** -- "mid-run", "posing confidently", "captured mid-stride"
9. **Use prestigious context anchors** -- "Pulitzer Prize-winning photograph," "Vanity Fair editorial," "National Geographic cover" actively improve quality
10. **For products, say "prominently displayed"** -- ensures the product/logo isn't hidden
11. **Quote text verbatim** -- GPT Image 2's biggest advantage; use it

### Anti-Patterns (What NOT to Do)

- **"A dark-themed Instagram ad showing..."** -- too meta, describes the concept not the image
- **"A sleek SaaS dashboard visualization..."** -- abstract, no visual anchors
- **"Modern, clean, professional..."** -- vague adjectives that mean nothing to the model
- **"A bold call to action with..."** -- describes marketing intent, not visual content
- **Describing what the viewer should feel** -- instead, describe what creates that feeling

## Safety Filter Rephrase Strategies

OpenAI applies content moderation at two layers: input prompt screening and
output image moderation. Filters cannot be disabled. When blocked, the only
path forward is rephrasing.

### Block error codes

| Error | Meaning |
|-------|---------|
| `content_policy_violation` | Input prompt violates content policy |
| `moderation_blocked` | Generated image was blocked by output moderation |

### Common Trigger Categories

| Category | Triggers on | Rephrase approach |
|----------|------------|-------------------|
| Violence/weapons | Combat, blood, injuries, firearms | Use metaphor or aftermath: "battle-worn" → "weathered veteran" |
| Medical/gore | Surgery, wounds, anatomical detail | Abstract or clinical: "open wound" → "medical illustration" |
| Real public figures | Named celebrities, politicians | Use archetypes: "Elon Musk" → "a tech entrepreneur in a minimalist office" |
| Minors + risk | Children in any ambiguous context | Add safety context: specify educational, family, or playful framing |
| NSFW/suggestive | Revealing clothing, intimate poses | Use artistic framing: "fashion editorial, fully clothed, editorial pose" |
| Copyrighted IP | Disney characters, branded media | Generic archetype: "a friendly cartoon mouse" → "a cheerful round-eared cartoon rodent" |

### Rephrase Patterns

1. **Abstraction** -- Replace specific dangerous elements with abstract concepts
2. **Artistic framing** -- Frame content as art, editorial, or documentary
3. **Metaphor** -- Use symbolic language instead of literal descriptions
4. **Positive emphasis** -- Describe what IS present, not what's dangerous
5. **Context shift** -- Move from threatening to educational/professional context

### Example Rephrases

| Blocked prompt | Successful rephrase |
|----------------|---------------------|
| "a soldier in combat firing a rifle" | "a determined soldier standing guard at dawn, rifle slung over shoulder, morning mist over the outpost" |
| "a scary horror monster" | "a fantastical creature from a dark fairy tale, intricate organic textures, bioluminescent accents, concept art style" |
| "dog in a fight" | "a friendly golden retriever playing energetically in a sunny park, action shot, joyful expression" |
| "medical surgery scene" | "a clean modern operating room viewed from the observation gallery, soft blue surgical lights, professional documentary style" |
| "celebrity portrait of [name]" | "a distinguished middle-aged man in a tailored navy suit, warm studio lighting, editorial portrait style" |

### Key Principle

Output moderation analyzes the generated image, not just the prompt. Even
well-phrased prompts can be blocked if the model's interpretation triggers
the output filter. When this happens, shift the visual concept further from
the trigger rather than just changing words.
