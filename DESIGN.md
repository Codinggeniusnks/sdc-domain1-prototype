# DESIGN.md — AI Skills Compass Design System

## 1. Visual Direction & Surface Philosophy
- **Mode**: `Operate` — Precision, clarity, high scanability, earned familiarity, and zero decorative slop.
- **Aesthetic Character**: Technical civic workbench (inspired by high-trust statistical and policy-intelligence platforms such as Our World in Data, Gov.uk / MyDIGITAL civic systems, and Linear's crisp operational hierarchy).
- **Anti-Patterns Refused**:
  - No nested cards (`card-inside-a-card` syndrome). Sections use structural dividers (`1px solid var(--border-subtle)`), clean whitespace, and tonal surface shifts.
  - No thick colored `border-left` stripes (`>1px`) on callouts, steps, or cards. Status is communicated via semantic badges, subtle 1px full borders, and crisp SVG iconography.
  - No Unicode emoji costumes (`🚀`, `🏢`, `📈`). All icons are consistent 16×16 inline vector SVGs (`stroke-width: 1.75`).
  - No uppercase eyebrow kickers stacked above headings. Badges sit inline or in right-aligned metadata slots.

## 2. Typography Scale (Fixed `rem` Scale for Operate UI)
- **Font Stack**:
  - UI & Prose: `'Fira Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
  - Tabular Data, Formulas & Dates: `'Fira Code', ui-monospace, SFMono-Regular, Consolas, monospace` with `font-variant-numeric: tabular-nums`
- **Scale Steps**:
  - `--text-xs`: `0.75rem` (12px, line-height `1.4`) — Badges, table column headers, provenance metadata
  - `--text-sm`: `0.84375rem` (13.5px, line-height `1.5`) — Secondary descriptions, form helper text, table cells
  - `--text-base`: `0.9375rem` (15px, line-height `1.55`) — Primary body copy, form controls (measure capped at `68ch`)
  - `--text-lg`: `1.0625rem` (17px, line-height `1.4`, weight `600`) — Sub-section and role titles
  - `--text-xl`: `1.25rem` (20px, line-height `1.3`, weight `700`, tracking `-0.015em`) — Primary section headings
  - `--text-2xl`: `1.5rem` (24px, line-height `1.2`, weight `700`, tracking `-0.02em`) — Application title & primary KPI readouts

## 3. Spacing System (4px / 8px Base Rhythm)
- `--space-1`: `0.25rem` (4px)
- `--space-2`: `0.5rem` (8px)
- `--space-3`: `0.75rem` (12px)
- `--space-4`: `1rem` (16px)
- `--space-5`: `1.25rem` (20px)
- `--space-6`: `1.5rem` (24px)
- `--space-8`: `2rem` (32px)
- `--space-10`: `2.5rem` (40px)

## 4. Semantic Color Tokens (WCAG AA/AAA Verified)
- **Canvas & Surfaces**:
  - `--bg-canvas`: `#F8FAFC` (Cool alabaster workspace canvas)
  - `--bg-surface`: `#FFFFFF` (Primary elevated module surface)
  - `--bg-subtle`: `#F1F5F9` (Secondary structural well / toolbar background)
  - `--bg-active`: `#EFF6FF` (Selected state tint)
- **Text Hierarchy**:
  - `--text-primary`: `#0F172A` (Contrast 17.4:1 on white)
  - `--text-secondary`: `#334155` (Contrast 9.8:1 on white)
  - `--text-muted`: `#475569` (Contrast 6.8:1 on white — never low-contrast light gray)
- **Brand & Interactive**:
  - `--primary`: `#1D4ED8` (Civic royal blue)
  - `--primary-hover`: `#1E40AF`
  - `--primary-border`: `#93C5FD`
- **Borders & Dividers**:
  - `--border-default`: `#CBD5E1`
  - `--border-subtle`: `#E2E8F0`
- **Semantic Status**:
  - Success: `--status-success-bg: #ECFDF5`, `--status-success-fg: #065F46`, `--status-success-border: #A7F3D0`
  - Warning: `--status-warn-bg: #FFFBEB`, `--status-warn-fg: #92400E`, `--status-warn-border: #FDE68A`
  - Danger/Gap: `--status-err-bg: #FEF2F2`, `--status-err-fg: #991B1B`, `--status-err-border: #FECACA`
  - Info/SDG: `--status-info-bg: #F5F3FF`, `--status-info-fg: #5B21B6`, `--status-info-border: #DDD6FE`
