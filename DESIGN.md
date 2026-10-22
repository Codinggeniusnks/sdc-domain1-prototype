# Design System Specification — AI Skills Compass (`DESIGN.md`)

## 1. Aesthetic Direction & Surface Mode
- **Surface Mode**: **Operate** (Diagnostic Precision + High-Craft Futuristic Telemetry).
- **Theme Polarity**: **Dual-Mode Quantum Theme System**:
  - **Quantum Obsidian Dark (`data-theme="dark"`, Default)**: Deep layered obsidian/slate surfaces (`#060A12` → `#0C1322` → `#111B2E`), subtle cyan/cobalt specular borders, and high-contrast `#F1F5F9` / `#CBD5E1` typography.
  - **Precision Daylight Slate (`data-theme="light"`)**: Architectural neutral slate (`#F4F7FB` → `#FFFFFF`), deep `#0B1120` ink, and royal blue (`#1D4ED8`) interactive accents.
  - Instant theme switching persisted in `localStorage` (`asc_theme`) with zero first-paint flash.

## 2. Typography & Scannable Hierarchy
- **Primary UI & Prose (`--font-sans`)**: `'Fira Sans'`, system sans-serif fallback.
- **Technical, Scores, Formulas & ISO-8601 Dates (`--font-mono`)**: `'Fira Code'`, monospace fallback with `font-variant-numeric: tabular-nums` enforced on all numeric columns, scores, percentages, and timelines.
- **Fixed `rem` Scale**:
  - `--text-xs`: `0.75rem` (`12px`) — Badges, metadata, table headers, HUD chips
  - `--text-sm`: `0.84375rem` (`13.5px`) — Secondary descriptions, table cells, form controls
  - `--text-base`: `0.9375rem` (`15px`) — Primary body copy (constrained to `60ch–75ch`)
  - `--text-lg`: `1.0625rem` (`17px`) — Role card titles & executive KPI values
  - `--text-xl`: `1.25rem` (`20px`) — Step section headings (`h2`)
  - `--text-2xl`: `1.5625rem` (`25px`) — Hero display title (`h1`)

## 3. Spacing, Radii, Elevation & Z-Index Scale
- **Spacing (`4px` / `8px` rhythm)**: `--space-1` (`4px`) through `--space-10` (`40px`).
- **Radii**: `--radius-sm` (`6px`), `--radius-md` (`10px`), `--radius-lg` (`14px`), `--radius-pill` (`9999px`).
- **Z-Index**: `--z-base` (`1`), `--z-sticky-col` (`2`), `--z-hud` (`10`), `--z-nav` (`50`), `--z-skip` (`9999`).

## 4. Bespoke 3D Vector Iconography & Hero Visual
- **Shared 3D SVG Lighting Defs (`SVG_3D_DEFS`)**: Multi-stop linear and radial gradients (`#icon3d-primary`, `#icon3d-glass`, `#icon3d-specular`, `#hero-core-glow`) give all 18 domain icons a semi-translucent glass/metallic 3D appearance with zero WebGL bundle overhead.
- **Interactive 3D Isometric AI Compass Stage (`hero_3d_compass_svg`)**:
  - Isometric coordinate grid plane, counter-rotating orbital telemetry rings, floating 3D hexagonal AI prism core, and live spatial HUD chips (`16 Taxonomy Skills`, `6 Emerging AI Roles`, `17 Dated Signals · CC0`).

## 5. Fluid Motion System & Performance Guardrails
- **Compositor-Only Properties**: Animations strictly target `transform` and `opacity` (e.g., `transform: scaleX(...)` on score breakdown bars, `translateY` on section reveals, `rotateX/rotateY` on 3D perspective cards).
- **Easing & Durations**:
  - `--dur-micro`: `150ms` (button/chip hover & press feedback)
  - `--dur-comp`: `240ms` (`<details>` role disclosure expansion & card transitions)
  - `--dur-reveal`: `420ms` (`IntersectionObserver` section entrance with `--ease-out-expo: cubic-bezier(0.22, 1, 0.36, 1)`)
- **Desktop Pointer Spotlight & 3D Tilt**: Throttled via `requestAnimationFrame` (`passive: true`), automatically disabled on coarse/touch pointers and `prefers-reduced-motion: reduce`.
