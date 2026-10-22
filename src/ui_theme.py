"""Futuristic Design System Tokens, 3D Vector Iconography, and GPU Motion Engine for AI Skills Compass.

Implements a high-craft 'Operate' + Futuristic AI Telemetry visual system:
- Dual-Mode Quantum Theme Architecture (Quantum Obsidian Dark default + Precision Daylight Slate)
- Complete 12-category design token system (Colors, Typography, Spacing, Radii, Borders,
  Elevation, Glow, Transitions, Durations, Easing, Z-Index, Surface Depth)
- Bespoke 3D-style multi-layered SVG iconography and interactive 3D Isometric AI Compass Hero visual
- GPU-friendly compositor motion (transform & opacity only, IntersectionObserver + rAF spotlight/tilt)
- Full WCAG AA/AAA contrast compliance and prefers-reduced-motion support
"""

from __future__ import annotations

# Shared SVG defs injected once in the document body so all 3D icons share gradients & lighting filters
SVG_3D_DEFS = """
<svg width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden;" aria-hidden="true" focusable="false">
  <defs>
    <linearGradient id="icon3d-primary" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="var(--icon-grad-start)" />
      <stop offset="55%" stop-color="var(--icon-grad-mid)" />
      <stop offset="100%" stop-color="var(--icon-grad-end)" />
    </linearGradient>
    <linearGradient id="icon3d-glass" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="var(--icon-glass-start)" stop-opacity="0.9" />
      <stop offset="100%" stop-color="var(--icon-glass-end)" stop-opacity="0.35" />
    </linearGradient>
    <linearGradient id="icon3d-specular" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="var(--icon-specular)" stop-opacity="0.95" />
      <stop offset="100%" stop-color="var(--icon-grad-mid)" stop-opacity="0.4" />
    </linearGradient>
    <radialGradient id="hero-core-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="var(--hero-orb-inner)" stop-opacity="0.55" />
      <stop offset="60%" stop-color="var(--hero-orb-mid)" stop-opacity="0.18" />
      <stop offset="100%" stop-color="var(--hero-orb-outer)" stop-opacity="0" />
    </radialGradient>
  </defs>
</svg>
"""

SVG_ICONS: dict[str, str] = {
    "compass": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<circle cx="12" cy="12" r="9.5" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.6"/>'
        '<circle cx="12" cy="12" r="6.5" stroke="url(#icon3d-specular)" stroke-width="0.9" stroke-dasharray="2 2"/>'
        '<polygon points="16.5,7.5 13.6,13.6 7.5,16.5 10.4,10.4" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.1"/>'
        '<circle cx="12" cy="12" r="1.6" fill="var(--icon-specular)"/>'
        '</svg>'
    ),
    "user": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M4.5 19.5c0-3.3 3.1-5.5 7.5-5.5s7.5 2.2 7.5 5.5v1H4.5v-1Z" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.6"/>'
        '<circle cx="12" cy="8" r="4" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.4"/>'
        '<path d="M9.8 6.5a2.5 2.5 0 0 1 3.2-.6" stroke="var(--icon-specular)" stroke-width="1.1" stroke-linecap="round"/>'
        '</svg>'
    ),
    "building": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<rect x="4" y="3.5" width="11" height="17" rx="2" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.6"/>'
        '<rect x="15" y="8.5" width="5.5" height="12" rx="1.5" fill="url(#icon3d-primary)" fill-opacity="0.35" stroke="url(#icon3d-specular)" stroke-width="1.4"/>'
        '<path d="M7.5 7.5h4M7.5 11h4M7.5 14.5h4" stroke="url(#icon3d-specular)" stroke-width="1.5" stroke-linecap="round"/>'
        '</svg>'
    ),
    "search": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<circle cx="10.8" cy="10.8" r="6.8" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.8"/>'
        '<path d="M7.8 8.2a4.2 4.2 0 0 1 5.2-.5" stroke="var(--icon-specular)" stroke-width="1.2" stroke-linecap="round"/>'
        '<path d="M16 16l4.5 4.5" stroke="url(#icon3d-primary)" stroke-width="2.2" stroke-linecap="round"/>'
        '</svg>'
    ),
    "layers": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<polygon points="12,3 21,7.8 12,12.5 3,7.8" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.4" stroke-linejoin="round"/>'
        '<polyline points="3,12.5 12,17.2 21,12.5" fill="none" stroke="url(#icon3d-primary)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polyline points="3,16.8 12,21.5 21,16.8" fill="none" stroke="url(#icon3d-specular)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>'
    ),
    "trend_up": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M3 18.5L9.5 12l4 4L21 7.5" stroke="url(#icon3d-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polygon points="15,6.5 21.5,6.5 21.5,13" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.2" stroke-linejoin="round"/>'
        '<path d="M3 20.5h18" stroke="url(#icon3d-specular)" stroke-width="1" stroke-opacity="0.5" stroke-linecap="round"/>'
        '</svg>'
    ),
    "trend_down": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M3 6.5L9.5 13l4-4L21 17.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polyline points="15 17.5 21 17.5 21 11.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>'
    ),
    "shield": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M12 2.8l7.5 3.2v5.8c0 5.2-3.2 8.6-7.5 10.2-4.3-1.6-7.5-5-7.5-10.2V6L12 2.8Z" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M9 12.2l2.1 2.1 4.2-4.2" stroke="url(#icon3d-specular)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>'
    ),
    "alert": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M10.3 3.9L2.2 18a2 2 0 0 0 1.7 3h16.2a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" fill="url(#icon3d-glass)" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<line x1="12" y1="9" x2="12" y2="13.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
        '<circle cx="12" cy="17" r="1" fill="currentColor"/>'
        '</svg>'
    ),
    "check": (
        '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<polyline points="20 6 9 17 4 12"/>'
        '</svg>'
    ),
    "plus": (
        '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>'
        '</svg>'
    ),
    "radio": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<circle cx="12" cy="12" r="3" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.3"/>'
        '<path d="M16.2 7.8a6 6 0 0 1 0 8.4m-8.4 0a6 6 0 0 1 0-8.4" stroke="url(#icon3d-primary)" stroke-width="1.7" stroke-linecap="round"/>'
        '<path d="M19.1 4.9a10 10 0 0 1 0 14.2M4.9 19.1a10 10 0 0 1 0-14.2" stroke="url(#icon3d-specular)" stroke-width="1.4" stroke-linecap="round" stroke-opacity="0.75"/>'
        '</svg>'
    ),
    "globe": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<circle cx="12" cy="12" r="9.2" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.6"/>'
        '<ellipse cx="12" cy="12" rx="4.2" ry="9.2" stroke="url(#icon3d-specular)" stroke-width="1.3"/>'
        '<line x1="2.8" y1="12" x2="21.2" y2="12" stroke="url(#icon3d-primary)" stroke-width="1.4"/>'
        '</svg>'
    ),
    "upload": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M20.5 15v3.5a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2V15" stroke="url(#icon3d-primary)" stroke-width="1.7" stroke-linecap="round"/>'
        '<polygon points="12,3.5 16.8,8.5 13.5,8.5 13.5,14.5 10.5,14.5 10.5,8.5 7.2,8.5" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.1" stroke-linejoin="round"/>'
        '</svg>'
    ),
    "external": (
        '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>'
        '</svg>'
    ),
    "sparkles": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M12 2.5l2.3 6.2 6.2 2.3-6.2 2.3L12 19.5l-2.3-6.2-6.2-2.3 6.2-2.3L12 2.5Z" fill="url(#icon3d-primary)" stroke="url(#icon3d-specular)" stroke-width="1.3" stroke-linejoin="round"/>'
        '<circle cx="19" cy="5" r="1.5" fill="var(--icon-specular)"/>'
        '</svg>'
    ),
    "book": (
        '<svg class="ui-icon ui-icon-3d" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5V5.5Z" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M8 7.5h8M8 11.5h6" stroke="url(#icon3d-specular)" stroke-width="1.5" stroke-linecap="round"/>'
        '</svg>'
    ),
    "chevron": (
        '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<polyline points="6 9 12 15 18 9"/>'
        '</svg>'
    ),
}


def icon_svg(name: str) -> str:
    """Return a 3D-layered inline SVG icon by semantic key."""
    return SVG_ICONS.get(name, SVG_ICONS["compass"])


def hero_3d_compass_svg(signal_count: int = 17, skill_count: int = 16, role_count: int = 6) -> str:
    """Render an interactive, hardware-accelerated 3D isometric AI Telemetry Core & Orbital Compass."""
    return f"""
    <div class="hero-3d-stage" data-tilt-card aria-hidden="true">
        <div class="hero-3d-glow"></div>
        <svg class="hero-3d-svg" viewBox="0 0 320 240" width="320" height="240" fill="none">
            <!-- Ambient Radial Field -->
            <circle cx="160" cy="120" r="108" fill="url(#hero-core-glow)" />

            <!-- Isometric Base Grid Plane -->
            <g class="iso-base-plane">
                <polygon points="160,198 274,142 160,86 46,142" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.2" stroke-opacity="0.55" />
                <polygon points="160,208 274,152 274,142 160,198" fill="url(#icon3d-primary)" fill-opacity="0.22" />
                <polygon points="160,208 46,152 46,142 160,198" fill="url(#icon3d-primary)" fill-opacity="0.12" />
                <line x1="103" y1="114" x2="217" y2="170" stroke="url(#icon3d-specular)" stroke-width="0.75" stroke-opacity="0.35" stroke-dasharray="3 3" />
                <line x1="217" y1="114" x2="103" y2="170" stroke="url(#icon3d-specular)" stroke-width="0.75" stroke-opacity="0.35" stroke-dasharray="3 3" />
            </g>

            <!-- Outer Orbital Ring (GPU CSS animated) -->
            <g class="hero-orbit-outer">
                <ellipse cx="160" cy="128" rx="92" ry="42" stroke="url(#icon3d-primary)" stroke-width="1.4" stroke-dasharray="6 4" stroke-opacity="0.75" />
                <circle cx="68" cy="128" r="4.5" fill="var(--icon-specular)" />
                <circle cx="252" cy="128" r="3.5" fill="url(#icon3d-primary)" />
            </g>

            <!-- Inner Counter-Orbit Ring -->
            <g class="hero-orbit-inner">
                <ellipse cx="160" cy="116" rx="64" ry="29" stroke="url(#icon3d-specular)" stroke-width="1.3" stroke-opacity="0.85" />
                <circle cx="160" cy="87" r="4" fill="var(--icon-specular)" />
            </g>

            <!-- Floating 3D Hexagonal AI Prism Core -->
            <g class="hero-prism-core">
                <!-- Top Isometric Facet -->
                <polygon points="160,64 202,84 160,104 118,84" fill="url(#icon3d-specular)" stroke="var(--icon-specular)" stroke-width="1.3" />
                <!-- Left Shaded Facet -->
                <polygon points="118,84 160,104 160,146 118,126" fill="url(#icon3d-glass)" stroke="url(#icon3d-primary)" stroke-width="1.3" />
                <!-- Right Illuminated Facet -->
                <polygon points="202,84 160,104 160,146 202,126" fill="url(#icon3d-primary)" fill-opacity="0.75" stroke="url(#icon3d-specular)" stroke-width="1.3" />
                <!-- Central Compass Vector Needle -->
                <polygon points="160,73 177,84 160,95 143,84" fill="var(--bg-header)" stroke="var(--icon-specular)" stroke-width="1.2" />
                <circle cx="160" cy="84" r="3.2" fill="var(--icon-specular)" />
            </g>

            <!-- Vertical Telemetry Laser Axis -->
            <line x1="160" y1="36" x2="160" y2="64" stroke="var(--icon-specular)" stroke-width="1.5" stroke-dasharray="2 3" />
            <circle cx="160" cy="34" r="3.5" fill="var(--icon-specular)" />
        </svg>

        <!-- Floating Spatial HUD Badges -->
        <div class="hero-hud-chip hero-hud-tl">
            <span class="hud-dot"></span>
            <span class="tabular">{skill_count} Taxonomy Skills</span>
        </div>
        <div class="hero-hud-chip hero-hud-tr">
            <span class="tabular">{role_count} Emerging AI Roles</span>
        </div>
        <div class="hero-hud-chip hero-hud-br">
            <span class="tabular">{signal_count} Dated Signals · CC0</span>
        </div>
    </div>
    """


DESIGN_SYSTEM_CSS = """
:root {
    /* =========================================================================
       1. PRIMITIVE PALETTE TOKENS (All raw hex/rgba values strictly in :root)
       ========================================================================= */
    /* Light Mode Primitives (Precision Daylight Slate) */
    --p-light-canvas: #F4F7FB;
    --p-light-surface: #FFFFFF;
    --p-light-elevated: #F8FAFC;
    --p-light-subtle: #EEF2F8;
    --p-light-muted: #E2E8F0;
    --p-light-active: #EFF6FF;
    --p-light-glass: rgba(255, 255, 255, 0.86);
    --p-light-header: #080E1E;
    --p-light-header-grad: radial-gradient(120% 140% at 85% 15%, rgba(56, 189, 248, 0.16) 0%, rgba(29, 78, 216, 0.12) 42%, rgba(8, 14, 30, 0.98) 100%);

    --p-light-text-1: #0B1120;
    --p-light-text-2: #283548;
    --p-light-text-3: #475569;

    --p-light-primary: #1D4ED8;
    --p-light-primary-hover: #1E40AF;
    --p-light-primary-fg: #FFFFFF;
    --p-light-primary-border: #60A5FA;
    --p-light-primary-subtle: #DBEAFE;

    --p-light-border-default: #CBD5E1;
    --p-light-border-subtle: #E2E8F0;
    --p-light-border-strong: #94A3B8;
    --p-light-border-glow: rgba(37, 99, 235, 0.32);

    --p-light-success-bg: #ECFDF5;
    --p-light-success-fg: #065F46;
    --p-light-success-border: #6EE7B7;

    --p-light-warn-bg: #FFFBEB;
    --p-light-warn-fg: #92400E;
    --p-light-warn-border: #FCD34D;

    --p-light-err-bg: #FEF2F2;
    --p-light-err-fg: #991B1B;
    --p-light-err-border: #FCA5A5;

    --p-light-info-bg: #F5F3FF;
    --p-light-info-fg: #5B21B6;
    --p-light-info-border: #C4B5FD;

    --p-light-shadow-sm: 0 1px 3px 0 rgba(11, 17, 32, 0.05), 0 1px 2px -1px rgba(11, 17, 32, 0.04);
    --p-light-shadow-md: 0 8px 24px -4px rgba(11, 17, 32, 0.08), 0 2px 6px -1px rgba(11, 17, 32, 0.04);
    --p-light-shadow-lg: 0 16px 36px -6px rgba(11, 17, 32, 0.12), 0 4px 12px -2px rgba(29, 78, 216, 0.06);
    --p-light-grid-line: rgba(148, 163, 184, 0.14);
    --p-light-spotlight: rgba(37, 99, 235, 0.07);

    /* Dark Mode Primitives (Quantum Obsidian Dark) */
    --p-dark-canvas: #060A12;
    --p-dark-surface: #0C1322;
    --p-dark-elevated: #111B2E;
    --p-dark-subtle: #152238;
    --p-dark-muted: #1E2E4A;
    --p-dark-active: #16284C;
    --p-dark-glass: rgba(12, 19, 34, 0.84);
    --p-dark-header: #050811;
    --p-dark-header-grad: radial-gradient(120% 140% at 85% 15%, rgba(56, 189, 248, 0.20) 0%, rgba(37, 99, 235, 0.16) 45%, rgba(5, 8, 17, 0.98) 100%);

    --p-dark-text-1: #F1F5F9;
    --p-dark-text-2: #CBD5E1;
    --p-dark-text-3: #94A3B8;

    --p-dark-primary: #3B82F6;
    --p-dark-primary-hover: #60A5FA;
    --p-dark-primary-fg: #050811;
    --p-dark-primary-border: #38BDF8;
    --p-dark-primary-subtle: #172B54;

    --p-dark-border-default: #1E2E4A;
    --p-dark-border-subtle: #162238;
    --p-dark-border-strong: #334E7B;
    --p-dark-border-glow: rgba(56, 189, 248, 0.42);

    --p-dark-success-bg: rgba(6, 95, 70, 0.28);
    --p-dark-success-fg: #6EE7B7;
    --p-dark-success-border: rgba(52, 211, 153, 0.45);

    --p-dark-warn-bg: rgba(146, 64, 14, 0.28);
    --p-dark-warn-fg: #FCD34D;
    --p-dark-warn-border: rgba(251, 191, 36, 0.45);

    --p-dark-err-bg: rgba(153, 27, 27, 0.28);
    --p-dark-err-fg: #FCA5A5;
    --p-dark-err-border: rgba(248, 113, 113, 0.45);

    --p-dark-info-bg: rgba(91, 33, 182, 0.28);
    --p-dark-info-fg: #C4B5FD;
    --p-dark-info-border: rgba(167, 139, 250, 0.45);

    --p-dark-shadow-sm: 0 2px 6px 0 rgba(0, 0, 0, 0.35);
    --p-dark-shadow-md: 0 10px 28px -4px rgba(0, 0, 0, 0.52), 0 0 1px 0 rgba(56, 189, 248, 0.16);
    --p-dark-shadow-lg: 0 20px 44px -8px rgba(0, 0, 0, 0.68), 0 0 24px -6px rgba(56, 189, 248, 0.18);
    --p-dark-grid-line: rgba(56, 189, 248, 0.06);
    --p-dark-spotlight: rgba(56, 189, 248, 0.09);

    /* Shared 3D Icon & Hero Orb Gradient Primitives */
    --icon-grad-start: #38BDF8;
    --icon-grad-mid: #2563EB;
    --icon-grad-end: #1D4ED8;
    --icon-glass-start: #93C5FD;
    --icon-glass-end: #1E3A8A;
    --icon-specular: #7DD3FC;
    --hero-orb-inner: #38BDF8;
    --hero-orb-mid: #2563EB;
    --hero-orb-outer: #080E1E;

    /* =========================================================================
       2. TYPOGRAPHY, SPACING, RADII, Z-INDEX & MOTION TOKENS
       ========================================================================= */
    --font-sans: 'Fira Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    --text-xs: 0.75rem;
    --text-sm: 0.84375rem;
    --text-base: 0.9375rem;
    --text-lg: 1.0625rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5625rem;

    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-pill: 9999px;

    --z-base: 1;
    --z-sticky-col: 2;
    --z-hud: 10;
    --z-nav: 50;
    --z-skip: 9999;

    /* Professional Motion & Easing Tokens (120ms micro -> 420ms reveal) */
    --dur-micro: 150ms;
    --dur-comp: 240ms;
    --dur-reveal: 420ms;
    --ease-out-expo: cubic-bezier(0.22, 1, 0.36, 1);
    --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);

    /* =========================================================================
       3. ACTIVE SEMANTIC SURFACE & COLOR TOKENS (Default: Daylight Slate)
       ========================================================================= */
    --bg-canvas: var(--p-light-canvas);
    --bg-surface: var(--p-light-surface);
    --bg-elevated: var(--p-light-elevated);
    --bg-subtle: var(--p-light-subtle);
    --bg-muted: var(--p-light-muted);
    --bg-active: var(--p-light-active);
    --bg-glass: var(--p-light-glass);
    --bg-header: var(--p-light-header);
    --bg-header-grad: var(--p-light-header-grad);

    --text-primary: var(--p-light-text-1);
    --text-secondary: var(--p-light-text-2);
    --text-muted: var(--p-light-text-3);
    --text-on-dark: #F8FAFC;
    --text-on-dark-muted: #CBD5E1;

    --primary: var(--p-light-primary);
    --primary-hover: var(--p-light-primary-hover);
    --primary-fg: var(--p-light-primary-fg);
    --primary-border: var(--p-light-primary-border);
    --primary-subtle: var(--p-light-primary-subtle);

    --border-default: var(--p-light-border-default);
    --border-subtle: var(--p-light-border-subtle);
    --border-strong: var(--p-light-border-strong);
    --border-glow: var(--p-light-border-glow);

    --status-success-bg: var(--p-light-success-bg);
    --status-success-fg: var(--p-light-success-fg);
    --status-success-border: var(--p-light-success-border);

    --status-warn-bg: var(--p-light-warn-bg);
    --status-warn-fg: var(--p-light-warn-fg);
    --status-warn-border: var(--p-light-warn-border);

    --status-err-bg: var(--p-light-err-bg);
    --status-err-fg: var(--p-light-err-fg);
    --status-err-border: var(--p-light-err-border);

    --status-info-bg: var(--p-light-info-bg);
    --status-info-fg: var(--p-light-info-fg);
    --status-info-border: var(--p-light-info-border);

    --shadow-sm: var(--p-light-shadow-sm);
    --shadow-md: var(--p-light-shadow-md);
    --shadow-lg: var(--p-light-shadow-lg);
    --grid-line: var(--p-light-grid-line);
    --card-spotlight: var(--p-light-spotlight);
}

/* Quantum Obsidian Dark Theme Override */
html[data-theme="dark"] {
    --bg-canvas: var(--p-dark-canvas);
    --bg-surface: var(--p-dark-surface);
    --bg-elevated: var(--p-dark-elevated);
    --bg-subtle: var(--p-dark-subtle);
    --bg-muted: var(--p-dark-muted);
    --bg-active: var(--p-dark-active);
    --bg-glass: var(--p-dark-glass);
    --bg-header: var(--p-dark-header);
    --bg-header-grad: var(--p-dark-header-grad);

    --text-primary: var(--p-dark-text-1);
    --text-secondary: var(--p-dark-text-2);
    --text-muted: var(--p-dark-text-3);

    --primary: var(--p-dark-primary);
    --primary-hover: var(--p-dark-primary-hover);
    --primary-fg: var(--p-dark-primary-fg);
    --primary-border: var(--p-dark-primary-border);
    --primary-subtle: var(--p-dark-primary-subtle);

    --border-default: var(--p-dark-border-default);
    --border-subtle: var(--p-dark-border-subtle);
    --border-strong: var(--p-dark-border-strong);
    --border-glow: var(--p-dark-border-glow);

    --status-success-bg: var(--p-dark-success-bg);
    --status-success-fg: var(--p-dark-success-fg);
    --status-success-border: var(--p-dark-success-border);

    --status-warn-bg: var(--p-dark-warn-bg);
    --status-warn-fg: var(--p-dark-warn-fg);
    --status-warn-border: var(--p-dark-warn-border);

    --status-err-bg: var(--p-dark-err-bg);
    --status-err-fg: var(--p-dark-err-fg);
    --status-err-border: var(--p-dark-err-border);

    --status-info-bg: var(--p-dark-info-bg);
    --status-info-fg: var(--p-dark-info-fg);
    --status-info-border: var(--p-dark-info-border);

    --shadow-sm: var(--p-dark-shadow-sm);
    --shadow-md: var(--p-dark-shadow-md);
    --shadow-lg: var(--p-dark-shadow-lg);
    --grid-line: var(--p-dark-grid-line);
    --card-spotlight: var(--p-dark-spotlight);
}

/* =========================================================================
   4. BASE & TECHNOLOGICAL ATMOSPHERE
   ========================================================================= */
*, *::before, *::after {
    box-sizing: border-box;
}

html {
    color-scheme: light dark;
    scroll-behavior: smooth;
    scrollbar-color: var(--border-strong) var(--bg-canvas);
}

::selection {
    background-color: var(--primary-subtle);
    color: var(--text-primary);
}

body {
    margin: 0;
    font-family: var(--font-sans);
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    line-height: 1.55;
    font-size: var(--text-base);
    accent-color: var(--primary);
    caret-color: var(--primary);
    overflow-x: clip;
    -webkit-font-smoothing: antialiased;
    transition: background-color var(--dur-comp) var(--ease-out-expo), color var(--dur-comp) var(--ease-out-expo);
}

a {
    color: var(--primary);
    text-decoration-thickness: 1px;
    text-underline-offset: 3px;
    transition: color var(--dur-micro) ease, opacity var(--dur-micro) ease;
}

a:hover {
    color: var(--primary-hover);
}

/* Keyboard Focus States */
a:focus-visible,
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
summary:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
    border-radius: var(--radius-sm);
}

/* Tabular Numerals for Data Alignment */
.mono,
.tabular,
.score-pill,
.metric-val,
.exec-kpi-value,
.data-table td.mono {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
}

.prose-measure {
    max-width: 72ch;
}

/* Inline 3D & Vector SVG Icons */
.ui-icon {
    width: 1.15rem;
    height: 1.15rem;
    vertical-align: -0.2em;
    flex-shrink: 0;
    display: inline-block;
}

.ui-icon-3d {
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.16));
    transition: transform var(--dur-micro) var(--ease-spring);
}

.ui-icon-sm {
    width: 0.9rem;
    height: 0.9rem;
    vertical-align: -0.12em;
}

/* Skip Link for Accessibility */
.skip-link {
    position: absolute;
    left: -9999px;
    top: var(--space-2);
    background: var(--bg-surface);
    color: var(--primary);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-sm);
    font-weight: 700;
    z-index: var(--z-skip);
    box-shadow: var(--shadow-md);
}

.skip-link:focus {
    left: var(--space-4);
}

/* =========================================================================
   5. FUTURISTIC HERO SECTION & 3D ISOMETRIC TELEMETRY STAGE
   ========================================================================= */
header.hero {
    position: relative;
    background: var(--bg-header);
    background-image: var(--bg-header-grad);
    color: var(--text-on-dark);
    padding: var(--space-6) var(--space-4) var(--space-8);
    border-bottom: 1px solid var(--border-strong);
    overflow: hidden;
}

header.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 18% 22%, rgba(56, 189, 248, 0.12), transparent 55%);
    pointer-events: none;
}

.hero-inner {
    position: relative;
    z-index: var(--z-base);
    max-width: 1320px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.85fr);
    gap: var(--space-6);
    align-items: center;
}

.hero-inner > *,
.workspace-nav-inner > *,
.exec-kpi-cell,
.grid-2 > *,
.persona-grid > *,
.scenario-grid > * {
    min-width: 0;
}

.hero-eyebrow-row {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    flex-wrap: wrap;
    margin-bottom: var(--space-3);
}

.hero-live-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: var(--radius-pill);
    background: rgba(56, 189, 248, 0.14);
    border: 1px solid rgba(125, 211, 252, 0.35);
    color: var(--icon-specular);
    font-size: var(--text-xs);
    font-weight: 600;
    letter-spacing: 0.03em;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--icon-specular);
    box-shadow: 0 0 8px var(--icon-specular);
    animation: telemetryPulse 2.4s var(--ease-out-expo) infinite;
}

@keyframes telemetryPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.35); opacity: 0.55; }
}

.hero-title-block h1 {
    margin: 0 0 var(--space-2) 0;
    font-size: var(--text-2xl);
    font-weight: 700;
    letter-spacing: -0.025em;
    display: flex;
    align-items: center;
    gap: var(--space-3);
    color: var(--text-on-dark);
    line-height: 1.2;
}

.hero-subtitle {
    margin: 0 0 var(--space-4) 0;
    color: var(--text-on-dark-muted);
    font-size: var(--text-base);
    max-width: 68ch;
    line-height: 1.6;
}

.hero-cta-row {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.hero-cta-primary {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: 9px 18px;
    border-radius: var(--radius-md);
    background: var(--primary);
    color: var(--primary-fg);
    font-size: var(--text-sm);
    font-weight: 600;
    text-decoration: none;
    border: 1px solid var(--primary-border);
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    transition: transform var(--dur-micro) var(--ease-spring), background-color var(--dur-micro) ease, box-shadow var(--dur-micro) ease;
}

.hero-cta-primary:hover {
    background: var(--primary-hover);
    color: var(--primary-fg);
    transform: translateY(-1px);
}

.hero-cta-secondary {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: 9px 16px;
    border-radius: var(--radius-md);
    background: rgba(255, 255, 255, 0.07);
    color: var(--text-on-dark);
    font-size: var(--text-sm);
    font-weight: 500;
    text-decoration: none;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: transform var(--dur-micro) var(--ease-spring), background-color var(--dur-micro) ease, border-color var(--dur-micro) ease;
}

.hero-cta-secondary:hover {
    background: rgba(255, 255, 255, 0.14);
    color: var(--text-on-dark);
    border-color: var(--icon-specular);
    transform: translateY(-1px);
}

.hero-meta-badges {
    display: flex;
    gap: var(--space-2);
    flex-wrap: wrap;
    margin-top: var(--space-4);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: var(--text-on-dark-muted);
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    font-weight: 500;
}

/* 3D Isometric Compass Stage */
.hero-3d-stage {
    position: relative;
    width: 100%;
    max-width: 340px;
    height: 240px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-lg);
    background: rgba(15, 23, 42, 0.48);
    border: 1px solid rgba(125, 211, 252, 0.22);
    box-shadow: 0 16px 40px -8px rgba(0, 0, 0, 0.45);
    transform: perspective(900px) rotateX(var(--tilt-x, 0deg)) rotateY(var(--tilt-y, 0deg));
    transition: transform var(--dur-comp) var(--ease-out-expo), border-color var(--dur-comp) ease;
}

.hero-3d-stage:hover {
    border-color: rgba(125, 211, 252, 0.48);
}

.hero-3d-svg {
    width: 100%;
    height: auto;
    max-width: 310px;
    overflow: visible;
}

.hero-prism-core {
    transform-origin: 160px 105px;
    animation: prismFloat 4.8s ease-in-out infinite;
}

.hero-orbit-outer {
    transform-origin: 160px 128px;
    animation: orbitPulse 6s ease-in-out infinite;
}

.hero-orbit-inner {
    transform-origin: 160px 116px;
    animation: orbitPulse 4.2s ease-in-out infinite reverse;
}

@keyframes prismFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

@keyframes orbitPulse {
    0%, 100% { transform: scale(1); opacity: 0.82; }
    50% { transform: scale(1.03); opacity: 1; }
}

.hero-hud-chip {
    position: absolute;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 9px;
    border-radius: var(--radius-sm);
    background: rgba(8, 14, 30, 0.85);
    border: 1px solid rgba(125, 211, 252, 0.32);
    color: var(--text-on-dark);
    font-size: 0.7rem;
    font-weight: 600;
    z-index: var(--z-hud);
    backdrop-filter: blur(6px);
}

.hero-hud-tl { top: 10px; left: 10px; }
.hero-hud-tr { top: 10px; right: 10px; }
.hero-hud-br { bottom: 10px; right: 10px; }

.hud-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--status-success-border);
}

/* =========================================================================
   6. GLASSMORPHIC STICKY WORKSPACE NAVIGATION & THEME SWITCHER
   ========================================================================= */
.workspace-nav-bar {
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-default);
    position: sticky;
    top: 0;
    z-index: var(--z-nav);
    box-shadow: var(--shadow-sm);
}

.workspace-nav-inner {
    max-width: 1320px;
    margin: 0 auto;
    padding: var(--space-2) var(--space-4);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.view-tabs {
    display: inline-flex;
    background: var(--bg-subtle);
    padding: 3px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-default);
    gap: 2px;
}

.view-tab {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    padding: 6px 14px;
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--text-secondary);
    text-decoration: none;
    transition: background-color var(--dur-micro) ease, color var(--dur-micro) ease, transform var(--dur-micro) var(--ease-spring);
}

.view-tab:hover {
    color: var(--text-primary);
    background: var(--bg-surface);
}

.view-tab.active-mode {
    background: var(--primary);
    color: var(--primary-fg);
    box-shadow: var(--shadow-sm);
}

.nav-right-cluster {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.step-jump-nav {
    display: flex;
    align-items: center;
    gap: var(--space-1);
    flex-wrap: wrap;
}

.step-jump-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 10px;
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--text-secondary);
    text-decoration: none;
    border: 1px solid transparent;
    transition: background-color var(--dur-micro) ease, border-color var(--dur-micro) ease, color var(--dur-micro) ease;
}

.step-jump-link:hover {
    background: var(--bg-subtle);
    border-color: var(--border-default);
    color: var(--primary);
}

.step-num-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--bg-muted);
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-size: 0.6875rem;
    font-weight: 700;
}

.theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 11px;
    border-radius: var(--radius-sm);
    background: var(--bg-subtle);
    color: var(--text-primary);
    border: 1px solid var(--border-default);
    font-family: var(--font-sans);
    font-size: var(--text-xs);
    font-weight: 600;
    cursor: pointer;
    transition: background-color var(--dur-micro) ease, border-color var(--dur-micro) ease, transform var(--dur-micro) var(--ease-spring);
}

.theme-toggle-btn:hover {
    background: var(--bg-elevated);
    border-color: var(--primary);
    transform: translateY(-1px);
}

/* =========================================================================
   7. MAIN CONTAINER, MOTION REVEAL & STATUS BANNERS
   ========================================================================= */
.container {
    max-width: 1320px;
    margin: 0 auto;
    padding: var(--space-5) var(--space-4) var(--space-10);
}

/* GPU-Friendly Staggered Section Reveal (only active when JS initializes) */
html.js-motion-ready .reveal-section {
    opacity: 0;
    transform: translateY(14px);
    transition: opacity var(--dur-reveal) var(--ease-out-expo), transform var(--dur-reveal) var(--ease-out-expo);
}

html.js-motion-ready .reveal-section.is-visible {
    opacity: 1;
    transform: translateY(0);
}

.status-strip {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-3);
    margin-bottom: var(--space-5);
}

.top-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
    font-weight: 600;
    flex-wrap: wrap;
}

.banner-live {
    background: var(--status-success-bg);
    border: 1px solid var(--status-success-border);
    color: var(--status-success-fg);
}

.banner-fallback {
    background: var(--status-warn-bg);
    border: 1px solid var(--status-warn-border);
    color: var(--status-warn-fg);
}

.banner-error {
    background: var(--status-err-bg);
    border: 1px solid var(--status-err-border);
    color: var(--status-err-fg);
}

.synthetic-guardrail {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-4);
    font-size: var(--text-xs);
    color: var(--text-secondary);
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
    box-shadow: var(--shadow-sm);
}

.guardrail-icon {
    color: var(--primary);
    margin-top: 1px;
}

/* =========================================================================
   8. EXECUTIVE READINESS SUMMARY STRIP (5 UX Questions at a Glance)
   ========================================================================= */
.exec-summary-strip {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-lg);
    padding: var(--space-4) var(--space-5);
    margin-bottom: var(--space-5);
    box-shadow: var(--shadow-md);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-4);
    align-items: stretch;
}

.exec-kpi-cell {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-right: var(--space-3);
    border-right: 1px solid var(--border-subtle);
}

.exec-kpi-cell:last-child {
    border-right: none;
    padding-right: 0;
}

.exec-kpi-label {
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: var(--space-1);
    display: flex;
    align-items: center;
    gap: 6px;
}

.exec-kpi-value {
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.25;
    margin-bottom: var(--space-1);
}

.exec-kpi-sub {
    font-size: var(--text-xs);
    color: var(--text-secondary);
}

/* =========================================================================
   9. SECTION CARDS, SPOTLIGHT & HEADER HIERARCHY
   ========================================================================= */
.card {
    position: relative;
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    margin-bottom: var(--space-5);
    box-shadow: var(--shadow-md);
    transition: border-color var(--dur-comp) ease, box-shadow var(--dur-comp) ease;
}

.card:hover {
    border-color: var(--border-strong);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: var(--space-3);
    margin-bottom: var(--space-4);
    flex-wrap: wrap;
}

.section-header h2 {
    margin: 0;
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: var(--space-2);
    letter-spacing: -0.015em;
}

.section-sub {
    margin: 0 0 var(--space-4) 0;
    color: var(--text-secondary);
    font-size: var(--text-sm);
    max-width: 75ch;
}

/* =========================================================================
   10. INTERACTIVE PERSONA & SCENARIO CARDS (3D Perspective + Pointer Glow)
   ========================================================================= */
.persona-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
    gap: var(--space-3);
    margin-bottom: var(--space-5);
}

.persona-card,
.scenario-card {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-decoration: none;
    color: inherit;
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    background: var(--bg-elevated);
    background-image: radial-gradient(260px circle at var(--spot-x, 50%) var(--spot-y, 50%), var(--card-spotlight), transparent 80%);
    transform: perspective(800px) rotateX(var(--tilt-x, 0deg)) rotateY(var(--tilt-y, 0deg));
    transition: border-color var(--dur-micro) ease, background-color var(--dur-micro) ease, box-shadow var(--dur-micro) ease, transform var(--dur-comp) var(--ease-out-expo);
}

.persona-card:hover,
.scenario-card:hover {
    border-color: var(--primary);
    background-color: var(--bg-surface);
    box-shadow: var(--shadow-lg);
}

.persona-card.active,
.scenario-card.active {
    border-color: var(--primary);
    background-color: var(--bg-active);
    box-shadow: inset 0 0 0 1px var(--primary), var(--shadow-md);
}

.persona-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-2);
    margin-bottom: var(--space-1);
}

.persona-card-header .tag,
.scenario-header-row .tag {
    white-space: nowrap;
    flex-shrink: 0;
}

.persona-name {
    font-weight: 700;
    font-size: var(--text-base);
    color: var(--text-primary);
}

.persona-role {
    font-size: var(--text-xs);
    color: var(--primary);
    font-weight: 600;
    margin-bottom: var(--space-2);
}

.persona-bio {
    font-size: var(--text-xs);
    color: var(--text-secondary);
    line-height: 1.45;
}

/* =========================================================================
   11. INTAKE FORM, FILE UPLOAD & SKILL DRAWER
   ========================================================================= */
.intake-form {
    background: var(--bg-subtle);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    padding: var(--space-5);
}

.form-grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: var(--space-4);
    margin-bottom: var(--space-4);
}

.form-field {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
}

.form-field label {
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--text-primary);
}

.form-control {
    width: 100%;
    padding: 9px 12px;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    font-family: var(--font-sans);
    font-size: var(--text-sm);
    background: var(--bg-surface);
    color: var(--text-primary);
    transition: border-color var(--dur-micro) ease, box-shadow var(--dur-micro) ease;
}

.form-control:hover {
    border-color: var(--primary);
}

textarea.form-control {
    resize: vertical;
    min-height: 76px;
    line-height: 1.5;
}

.file-upload-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
    flex-wrap: wrap;
    margin-top: var(--space-2);
    padding: var(--space-2) var(--space-3);
    background: var(--bg-surface);
    border: 1px dashed var(--border-strong);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    color: var(--text-secondary);
}

.form-helper {
    font-size: var(--text-xs);
    color: var(--text-muted);
    margin-top: var(--space-1);
}

details.skill-drawer {
    margin-bottom: var(--space-4);
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-sm);
    padding: var(--space-3) var(--space-4);
}

details.skill-drawer summary {
    cursor: pointer;
    font-weight: 600;
    font-size: var(--text-sm);
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 5px;
    user-select: none;
}

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: var(--space-2);
    margin-top: var(--space-3);
    padding-top: var(--space-3);
    border-top: 1px solid var(--border-subtle);
}

.skill-check {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-xs);
    padding: 7px 10px;
    background: var(--bg-subtle);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-sm);
    cursor: pointer;
    color: var(--text-primary);
    transition: border-color var(--dur-micro) ease, background-color var(--dur-micro) ease, transform var(--dur-micro) var(--ease-spring);
}

.skill-check:hover {
    border-color: var(--primary);
    background: var(--bg-active);
    transform: translateY(-1px);
}

.skill-check input[type="checkbox"] {
    width: 15px;
    height: 15px;
    margin: 0;
    cursor: pointer;
}

.form-actions-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    background: var(--primary);
    color: var(--primary-fg);
    border: 1px solid var(--primary-border);
    padding: 9px 18px;
    border-radius: var(--radius-sm);
    font-family: var(--font-sans);
    font-weight: 600;
    font-size: var(--text-sm);
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    transition: background-color var(--dur-micro) ease, transform var(--dur-micro) var(--ease-spring), box-shadow var(--dur-micro) ease;
}

.btn-primary:hover {
    background: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn-primary:active {
    transform: translateY(1px);
}

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    background: var(--bg-subtle);
    color: var(--text-primary);
    border: 1px solid var(--border-strong);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-family: var(--font-sans);
    font-weight: 600;
    font-size: var(--text-xs);
    cursor: pointer;
    text-decoration: none;
    transition: background-color var(--dur-micro) ease, border-color var(--dur-micro) ease, transform var(--dur-micro) var(--ease-spring);
}

.btn-secondary:hover {
    background: var(--bg-elevated);
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-1px);
}

.profile-summary-bar {
    margin-top: var(--space-4);
    padding-top: var(--space-3);
    border-top: 1px solid var(--border-subtle);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
    font-size: var(--text-xs);
    color: var(--text-secondary);
}

/* =========================================================================
   12. SCENARIO SELECTOR & COMPARISON MATRIX
   ========================================================================= */
.scenario-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: var(--space-3);
}

.scenario-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-2);
    margin-bottom: var(--space-2);
}

.scenario-title {
    font-weight: 700;
    font-size: var(--text-base);
    color: var(--text-primary);
}

/* =========================================================================
   13. PROGRESSIVE DISCLOSURE ROLE RANKINGS & GPU METRIC BARS
   ========================================================================= */
.roles-stack {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

details.role-disclosure {
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    background: var(--bg-surface);
    transition: border-color var(--dur-comp) ease, box-shadow var(--dur-comp) ease;
}

details.role-disclosure[open] {
    border-color: var(--border-strong);
    box-shadow: var(--shadow-md);
}

details.role-disclosure.top-rank {
    border-color: var(--primary);
}

summary.role-summary-bar {
    list-style: none;
    cursor: pointer;
    padding: var(--space-4) var(--space-5);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
    background: var(--bg-elevated);
    border-radius: var(--radius-md);
    transition: background-color var(--dur-micro) ease;
}

details.role-disclosure[open] > summary.role-summary-bar {
    border-bottom: 1px solid var(--border-subtle);
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}

summary.role-summary-bar::-webkit-details-marker {
    display: none;
}

summary.role-summary-bar:hover {
    background: var(--bg-active);
}

.role-summary-left {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    font-weight: 700;
    background: var(--bg-muted);
    color: var(--text-primary);
}

details.role-disclosure.top-rank .rank-badge {
    background: var(--primary);
    color: var(--primary-fg);
}

.role-title {
    margin: 0;
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--text-primary);
}

.role-summary-right {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    flex-wrap: wrap;
}

.score-pill {
    background: var(--bg-header);
    color: var(--text-on-dark);
    padding: 5px 12px;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: var(--text-sm);
    border: 1px solid var(--border-strong);
}

details.role-disclosure.top-rank .score-pill {
    background: var(--primary);
    color: var(--primary-fg);
    border-color: var(--primary-border);
}

.disclosure-chevron {
    font-size: var(--text-xs);
    color: var(--text-muted);
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

details.role-disclosure[open] .disclosure-chevron-text::before {
    content: "Hide Details";
}

details.role-disclosure:not([open]) .disclosure-chevron-text::before {
    content: "Inspect Pathway & Gaps";
}

.role-body {
    padding: var(--space-5);
    animation: panelFadeIn var(--dur-comp) var(--ease-out-expo);
}

@keyframes panelFadeIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
}

.role-desc {
    margin: 0 0 var(--space-4) 0;
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.explain-box {
    background: var(--bg-subtle);
    border: 1px solid var(--border-default);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    margin-bottom: var(--space-4);
    color: var(--text-primary);
}

/* Score Breakdown Metric Bars (Compositor scaleX animation) */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: var(--space-4);
    margin-bottom: var(--space-5);
    padding: var(--space-3) var(--space-4);
    background: var(--bg-subtle);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-subtle);
}

.metric-box {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.metric-label {
    font-size: var(--text-xs);
    color: var(--text-secondary);
    font-weight: 600;
    display: flex;
    justify-content: space-between;
}

.metric-val {
    font-weight: 700;
    color: var(--text-primary);
}

.metric-bar-bg {
    height: 7px;
    background: var(--bg-muted);
    border-radius: var(--radius-pill);
    overflow: hidden;
}

.metric-bar-fill {
    height: 100%;
    width: 100%;
    background: linear-gradient(90deg, var(--primary) 0%, var(--icon-grad-start) 100%);
    border-radius: var(--radius-pill);
    transform-origin: left center;
    transition: transform var(--dur-reveal) var(--ease-spring);
}

/* Two-Column Structural Layout Inside Role Body (No Nested Cards) */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
    gap: var(--space-5);
}

.structural-pane {
    padding-top: var(--space-3);
    border-top: 2px solid var(--border-default);
}

.structural-pane h4 {
    margin: 0 0 var(--space-3) 0;
    font-size: var(--text-sm);
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.skill-group-label {
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
}

/* Semantic Tags & Chips */
.tag-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 9px;
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    font-weight: 600;
    line-height: 1.35;
}

.tag-match {
    background: var(--status-success-bg);
    color: var(--status-success-fg);
    border: 1px solid var(--status-success-border);
}

.tag-gap {
    background: var(--status-err-bg);
    color: var(--status-err-fg);
    border: 1px solid var(--status-err-border);
}

.tag-blue {
    background: var(--primary-subtle);
    color: var(--primary);
    border: 1px solid var(--primary-border);
}

.tag-amber {
    background: var(--status-warn-bg);
    color: var(--status-warn-fg);
    border: 1px solid var(--status-warn-border);
}

.tag-green {
    background: var(--status-success-bg);
    color: var(--status-success-fg);
    border: 1px solid var(--status-success-border);
}

.tag-purple {
    background: var(--status-info-bg);
    color: var(--status-info-fg);
    border: 1px solid var(--status-info-border);
}

.tag-muted {
    background: var(--bg-subtle);
    color: var(--text-secondary);
    border: 1px solid var(--border-default);
}

.tag-sdg {
    background: var(--primary-subtle);
    color: var(--primary);
    border: 1px solid var(--primary-border);
    font-family: var(--font-mono);
}

.tag-skill {
    background: var(--bg-subtle);
    color: var(--text-primary);
    border: 1px solid var(--border-default);
}

/* =========================================================================
   14. ORDERED LEARNING PATHWAY TIMELINE & SDG TARGETS
   ========================================================================= */
.pathway-list {
    position: relative;
    padding-left: var(--space-4);
    border-left: 2px solid var(--border-strong);
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
}

.pathway-step {
    position: relative;
    padding-bottom: var(--space-3);
    border-bottom: 1px solid var(--border-subtle);
}

.pathway-step:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.pathway-step::before {
    content: "";
    position: absolute;
    left: calc(-1 * var(--space-4) - 5px);
    top: 5px;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--primary);
    border: 2px solid var(--bg-surface);
}

.pathway-step.req-gap::before {
    background: var(--status-err-fg);
}

.step-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-2);
    flex-wrap: wrap;
    margin-bottom: 4px;
}

.step-title {
    font-weight: 700;
    font-size: var(--text-sm);
    color: var(--text-primary);
}

.step-obj {
    margin: 4px 0 6px 0;
    font-size: var(--text-xs);
    color: var(--text-secondary);
}

.step-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-2);
    font-size: var(--text-xs);
    color: var(--text-muted);
}

.sdg-footer {
    margin-top: var(--space-4);
    padding-top: var(--space-3);
    border-top: 1px solid var(--border-subtle);
}

.sdg-item {
    background: var(--bg-subtle);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-sm);
    padding: var(--space-2) var(--space-3);
    margin-bottom: var(--space-2);
    font-size: var(--text-xs);
}

.uncertainty-foot {
    margin-top: var(--space-2);
    font-size: var(--text-xs);
    color: var(--text-secondary);
}

.small-note {
    font-size: var(--text-xs);
    color: var(--text-muted);
    margin: 6px 0 0 0;
}

/* =========================================================================
   15. DATA TABLES, STICKY COHORT HEATMAP & SIGNAL FEED
   ========================================================================= */
.table-scroll {
    overflow-x: auto;
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    background: var(--bg-surface);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--text-xs);
}

.data-table th,
.data-table td {
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-subtle);
    vertical-align: top;
}

.data-table th {
    background: var(--bg-subtle);
    font-weight: 700;
    color: var(--text-primary);
    font-size: var(--text-xs);
    white-space: nowrap;
}

.data-table tbody tr {
    transition: background-color var(--dur-micro) ease;
}

.data-table tbody tr:hover {
    background: var(--bg-elevated);
}

/* Sticky First Column for Wide Employer/HR Heatmap Table */
.heatmap-table th:first-child,
.heatmap-table td:first-child {
    position: sticky;
    left: 0;
    z-index: var(--z-sticky-col);
    background: var(--bg-surface);
    border-right: 1px solid var(--border-default);
    min-width: 190px;
}

.heatmap-table th:first-child {
    background: var(--bg-subtle);
}

.sig-summary {
    color: var(--text-secondary);
    margin-top: 3px;
    line-height: 1.45;
}

/* Rising vs Declining Radar Panels */
.radar-panel-rising {
    background: var(--bg-surface);
    border: 1px solid var(--status-success-border);
    border-top: 2px solid var(--status-success-fg);
    border-radius: var(--radius-md);
    padding: var(--space-4);
}

.radar-panel-rising h4 {
    margin: 0 0 4px 0;
    color: var(--status-success-fg);
    font-size: var(--text-base);
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.radar-panel-declining {
    background: var(--bg-surface);
    border: 1px solid var(--status-err-border);
    border-top: 2px solid var(--status-err-fg);
    border-radius: var(--radius-md);
    padding: var(--space-4);
}

.radar-panel-declining h4 {
    margin: 0 0 4px 0;
    color: var(--status-err-fg);
    font-size: var(--text-base);
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

/* Signal Mode Bar & Guardrail Alert */
.mode-bar {
    display: flex;
    gap: var(--space-2);
    flex-wrap: wrap;
    margin-bottom: var(--space-4);
}

.mode-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    font-weight: 600;
    border: 1px solid var(--border-strong);
    color: var(--text-primary);
    background: var(--bg-surface);
    transition: background-color var(--dur-micro) ease, border-color var(--dur-micro) ease, transform var(--dur-micro) var(--ease-spring);
}

.mode-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-1px);
}

.mode-btn.active {
    background: var(--primary);
    color: var(--primary-fg);
    border-color: var(--primary);
}

.guardrail-alert {
    background: var(--status-err-bg);
    border: 1px solid var(--status-err-border);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    color: var(--status-err-fg);
    margin-bottom: var(--space-5);
}

.guardrail-alert h3 {
    margin: 0 0 var(--space-2) 0;
    font-size: var(--text-lg);
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

footer {
    text-align: center;
    padding: var(--space-6) var(--space-4);
    color: var(--text-muted);
    font-size: var(--text-xs);
    border-top: 1px solid var(--border-default);
    background: var(--bg-surface);
}

/* =========================================================================
   16. MULTI-BREAKPOINT RESPONSIVE SYSTEM (1920px -> 390px)
   ========================================================================= */
@media (min-width: 1600px) {
    .hero-inner,
    .workspace-nav-inner,
    .container {
        max-width: 1400px;
    }
}

@media (max-width: 1024px) {
    .hero-inner {
        grid-template-columns: minmax(0, 1fr);
    }
    .hero-3d-stage {
        max-width: 100%;
        height: 210px;
    }
    .exec-summary-strip {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .exec-kpi-cell:nth-child(2) {
        border-right: none;
        padding-right: 0;
    }
}

@media (max-width: 768px) {
    .workspace-nav-inner {
        flex-direction: column;
        align-items: stretch;
    }
    .view-tabs {
        width: 100%;
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    }
    .view-tab {
        justify-content: center;
        text-align: center;
        min-height: 42px;
    }
    .nav-right-cluster {
        justify-content: space-between;
        width: 100%;
    }
    .step-jump-nav {
        overflow-x: auto;
        flex-wrap: nowrap;
        max-width: 100%;
        padding-bottom: 2px;
    }
    .step-jump-link {
        white-space: nowrap;
        min-height: 36px;
    }
    .card {
        padding: var(--space-4);
    }
    .grid-2 {
        grid-template-columns: minmax(0, 1fr);
    }
}

@media (max-width: 600px) {
    header.hero {
        padding: var(--space-4) var(--space-3) var(--space-5);
    }
    .hero-title-block h1 {
        font-size: var(--text-xl);
    }
    .hero-cta-row {
        flex-direction: column;
        align-items: stretch;
    }
    .hero-cta-primary,
    .hero-cta-secondary {
        justify-content: center;
        width: 100%;
    }
    .view-tabs,
    .persona-grid,
    .scenario-grid,
    .form-grid-3,
    .skills-grid,
    .metrics-row {
        grid-template-columns: minmax(0, 1fr);
    }
    .exec-summary-strip {
        grid-template-columns: minmax(0, 1fr);
        padding: var(--space-3) var(--space-4);
    }
    .exec-kpi-cell {
        border-right: none;
        border-bottom: 1px solid var(--border-subtle);
        padding-right: 0;
        padding-bottom: var(--space-3);
    }
    .exec-kpi-cell:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    .hero-3d-stage {
        height: 190px;
    }
    .hero-hud-chip {
        font-size: 0.65rem;
        padding: 3px 7px;
    }
    summary.role-summary-bar {
        padding: var(--space-3);
    }
    .role-body {
        padding: var(--space-3);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
    html.js-motion-ready .reveal-section {
        opacity: 1 !important;
        transform: none !important;
    }
    .persona-card,
    .scenario-card,
    .hero-3d-stage {
        transform: none !important;
    }
}
"""

MOTION_ENGINE_JS = """
function updateSkillCount() {
    const checked = document.querySelectorAll('input[name="skills"]:checked').length;
    const el = document.getElementById('selected-skill-counter');
    if (el) el.textContent = checked;
}

function toggleAllRoles(btn) {
    const disclosures = document.querySelectorAll('.role-disclosure');
    const anyClosed = Array.from(disclosures).some(d => !d.open);
    disclosures.forEach((d, idx) => {
        d.open = anyClosed ? true : (idx < 2);
    });
    btn.textContent = anyClosed ? 'Collapse Roles #3–#6' : 'Expand All 6 Roles';
}

function toggleThemeMode() {
    const root = document.documentElement;
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('asc_theme', next); } catch (e) {}
    syncThemeButtonLabel(next);
}

function syncThemeButtonLabel(theme) {
    const label = document.getElementById('theme-mode-label');
    if (label) {
        label.textContent = theme === 'dark' ? 'Quantum Dark' : 'Daylight Slate';
    }
}

(function initFuturisticMotion() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme') || 'dark';
    syncThemeButtonLabel(currentTheme);

    const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reducedMotion) return;

    // 1. IntersectionObserver Staggered Section Reveal (zero scroll listener overhead)
    if ('IntersectionObserver' in window) {
        root.classList.add('js-motion-ready');
        const sections = document.querySelectorAll('.reveal-section');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.06, rootMargin: '0px 0px -24px 0px' });
        sections.forEach((sec) => observer.observe(sec));
    }

    // 2. Desktop-only rAF Pointer Spotlight & Restrained 3D Perspective Tilt
    const finePointer = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
    if (!finePointer) return;

    const tiltCards = document.querySelectorAll('.persona-card, .scenario-card, .hero-3d-stage');
    tiltCards.forEach((card) => {
        let rafId = null;
        card.addEventListener('pointermove', (e) => {
            if (rafId) return;
            rafId = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const pctX = (x / Math.max(rect.width, 1)) - 0.5;
                const pctY = (y / Math.max(rect.height, 1)) - 0.5;
                card.style.setProperty('--spot-x', x.toFixed(0) + 'px');
                card.style.setProperty('--spot-y', y.toFixed(0) + 'px');
                card.style.setProperty('--tilt-x', (-pctY * 3.5).toFixed(2) + 'deg');
                card.style.setProperty('--tilt-y', (pctX * 3.5).toFixed(2) + 'deg');
                rafId = null;
            });
        }, { passive: true });

        card.addEventListener('pointerleave', () => {
            if (rafId) {
                cancelAnimationFrame(rafId);
                rafId = null;
            }
            card.style.setProperty('--tilt-x', '0deg');
            card.style.setProperty('--tilt-y', '0deg');
        }, { passive: true });
    });
})();
"""
