"""Design System Tokens, CSS Architecture, and Inline SVG Iconography for AI Skills Compass.

Follows Operate-mode principles (DESIGN.md):
- Fixed rem typography scale with tabular numerals
- 4px/8px spacing rhythm
- High-contrast WCAG AA/AAA semantic color tokens
- Zero >1px colored side borders, zero nested card-in-card containers, zero emoji icons
- Themed browser surfaces (selection, caret, focus-visible, scrollbars, underline-offset)
"""

from __future__ import annotations

SVG_ICONS: dict[str, str] = {
    "compass": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    "user": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "building": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/></svg>',
    "search": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "trend_up": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    "trend_down": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/></svg>',
    "check": '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>',
    "plus": '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "alert": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "shield": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "layers": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "book": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "globe": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "upload": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "radio": '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/></svg>',
    "chevron": '<svg class="ui-icon chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>',
    "external": '<svg class="ui-icon ui-icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
}


def icon_svg(name: str) -> str:
    """Return an inline SVG icon by semantic key."""
    return SVG_ICONS.get(name, "")


DESIGN_SYSTEM_CSS = """
:root {
    /* Typography Scale (Fixed rem for Operate UI) */
    --font-sans: 'Fira Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'Fira Code', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    --text-xs: 0.75rem;
    --text-sm: 0.84375rem;
    --text-base: 0.9375rem;
    --text-lg: 1.0625rem;
    --text-xl: 1.25rem;
    --text-2xl: 1.5rem;

    /* Spacing Scale (4px / 8px rhythm) */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;

    /* Semantic Surfaces & Colors (WCAG AA/AAA Verified) */
    --bg-canvas: #F8FAFC;
    --bg-surface: #FFFFFF;
    --bg-subtle: #F1F5F9;
    --bg-muted: #E2E8F0;
    --bg-active: #EFF6FF;
    --bg-header: #0F172A;

    --text-primary: #0F172A;
    --text-secondary: #334155;
    --text-muted: #475569;
    --text-on-dark: #F8FAFC;
    --text-on-dark-muted: #CBD5E1;

    --primary: #1D4ED8;
    --primary-hover: #1E40AF;
    --primary-fg: #FFFFFF;
    --primary-border: #93C5FD;
    --primary-subtle: #DBEAFE;

    --border-default: #CBD5E1;
    --border-subtle: #E2E8F0;
    --border-strong: #94A3B8;

    /* Semantic Status Tokens */
    --status-success-bg: #ECFDF5;
    --status-success-fg: #065F46;
    --status-success-border: #A7F3D0;

    --status-warn-bg: #FFFBEB;
    --status-warn-fg: #92400E;
    --status-warn-border: #FDE68A;

    --status-err-bg: #FEF2F2;
    --status-err-fg: #991B1B;
    --status-err-border: #FECACA;

    --status-info-bg: #F5F3FF;
    --status-info-fg: #5B21B6;
    --status-info-border: #DDD6FE;

    --radius-sm: 6px;
    --radius-md: 8px;
    --radius-lg: 10px;
    --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
    --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.08);
}

/* Base & Browser Surface Theming */
*, *::before, *::after {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
    scrollbar-width: thin;
    scrollbar-color: var(--border-strong) var(--bg-subtle);
}

::selection {
    background-color: var(--primary-subtle);
    color: var(--primary-hover);
}

body {
    margin: 0;
    font-family: var(--font-sans);
    font-size: var(--text-base);
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
}

a {
    color: var(--primary);
    text-underline-offset: 3px;
    text-decoration-thickness: 1px;
    transition: color 150ms ease;
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

.mono, .tabular {
    font-family: var(--font-mono);
    font-size: 0.86em;
    font-variant-numeric: tabular-nums;
}

.prose-measure {
    max-width: 68ch;
}

/* Icons */
.ui-icon {
    width: 16px;
    height: 16px;
    vertical-align: -0.18em;
    flex-shrink: 0;
    display: inline-block;
}

.ui-icon-sm {
    width: 14px;
    height: 14px;
    vertical-align: -0.12em;
}

/* Skip Link */
.skip-link {
    position: absolute;
    left: -9999px;
    top: var(--space-2);
    background: var(--primary);
    color: var(--primary-fg);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-sm);
    font-weight: 600;
    z-index: 1000;
    text-decoration: none;
}

.skip-link:focus {
    left: var(--space-4);
}

/* Top Application Header */
.app-header {
    background-color: var(--bg-header);
    color: var(--text-on-dark);
    border-bottom: 1px solid #1E293B;
    padding: var(--space-4) var(--space-6);
}

.header-inner {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-4);
}

.brand-group {
    display: flex;
    align-items: center;
    gap: var(--space-3);
}

.brand-mark {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    background: var(--primary);
    color: var(--primary-fg);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.brand-mark .ui-icon {
    width: 20px;
    height: 20px;
}

.header-title h1 {
    margin: 0;
    font-size: var(--text-xl);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.header-title p {
    margin: 2px 0 0;
    color: var(--text-on-dark-muted);
    font-size: var(--text-xs);
}

.header-badges {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
}

/* Sticky Sub-Navigation & View Switcher Bar */
.workspace-nav-bar {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border-default);
    padding: var(--space-2) var(--space-6);
    box-shadow: var(--shadow-sm);
}

.workspace-nav-inner {
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
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
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    font-weight: 600;
    text-decoration: none;
    color: var(--text-secondary);
    transition: background-color 150ms ease, color 150ms ease;
}

.view-tab:hover {
    color: var(--text-primary);
    background: rgba(255, 255, 255, 0.6);
}

.view-tab.active-mode {
    background: var(--bg-surface);
    color: var(--primary);
    box-shadow: var(--shadow-sm);
}

.step-jump-nav {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--space-1);
    font-size: var(--text-xs);
}

.step-jump-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 10px;
    border-radius: var(--radius-sm);
    text-decoration: none;
    color: var(--text-secondary);
    font-weight: 500;
    transition: background-color 150ms ease, color 150ms ease;
}

.step-jump-link:hover {
    background: var(--bg-subtle);
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
    font-size: 11px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
}

/* Main Workspace Container */
.container {
    max-width: 1280px;
    margin: 0 auto;
    padding: var(--space-6) var(--space-6) var(--space-10);
}

/* Status Banner & Guardrail Notice */
.status-strip {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-3);
    margin-bottom: var(--space-6);
}

.top-banner {
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    font-size: var(--text-sm);
    font-weight: 500;
    border: 1px solid transparent;
}

.banner-live {
    background: var(--status-success-bg);
    color: var(--status-success-fg);
    border-color: var(--status-success-border);
}

.banner-fallback {
    background: var(--status-warn-bg);
    color: var(--status-warn-fg);
    border-color: var(--status-warn-border);
}

.banner-error {
    background: var(--status-err-bg);
    color: var(--status-err-fg);
    border-color: var(--status-err-border);
}

.synthetic-guardrail {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
    color: var(--text-secondary);
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
}

.synthetic-guardrail .guardrail-icon {
    color: var(--primary);
    margin-top: 2px;
}

/* Executive Summary Bar (Immediate User Orientation) */
.exec-summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-lg);
    margin-bottom: var(--space-6);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

.exec-cell {
    padding: var(--space-4) var(--space-5);
    border-right: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: var(--space-1);
}

.exec-cell:last-child {
    border-right: none;
}

.exec-label {
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
}

.exec-value {
    font-size: var(--text-lg);
    font-weight: 700;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1.3;
}

.exec-sub {
    font-size: var(--text-xs);
    color: var(--text-muted);
}

/* Primary Workbench Sections */
.card {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    margin-bottom: var(--space-6);
    box-shadow: var(--shadow-sm);
}

.section-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    padding-bottom: var(--space-3);
    margin-bottom: var(--space-4);
    border-bottom: 1px solid var(--border-subtle);
}

.section-header h2 {
    margin: 0;
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.015em;
    display: flex;
    align-items: center;
    gap: var(--space-2);
}

.section-sub {
    margin: 0 0 var(--space-4);
    color: var(--text-secondary);
    font-size: var(--text-base);
    max-width: 72ch;
}

/* Semantic Badges / Tags */
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
    border: 1px solid transparent;
    font-variant-numeric: tabular-nums;
}

.tag-skill {
    background: #F0F9FF;
    color: #0369A1;
    border-color: #BAE6FD;
}

.tag-green {
    background: var(--status-success-bg);
    color: var(--status-success-fg);
    border-color: var(--status-success-border);
}

.tag-amber {
    background: var(--status-warn-bg);
    color: var(--status-warn-fg);
    border-color: var(--status-warn-border);
}

.tag-gap {
    background: var(--status-err-bg);
    color: var(--status-err-fg);
    border-color: var(--status-err-border);
}

.tag-blue {
    background: var(--bg-active);
    color: var(--primary-hover);
    border-color: var(--primary-border);
}

.tag-muted {
    background: var(--bg-subtle);
    color: var(--text-secondary);
    border-color: var(--border-default);
}

.tag-sdg {
    background: var(--status-info-bg);
    color: var(--status-info-fg);
    border-color: var(--status-info-border);
}

/* Step 1: Persona Quick-Selector Pills & Intake Form */
.persona-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: var(--space-3);
    margin-bottom: var(--space-4);
}

.persona-pill {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-default);
    text-decoration: none;
    color: var(--text-primary);
    background: var(--bg-surface);
    transition: border-color 150ms ease, background-color 150ms ease, box-shadow 150ms ease;
}

.persona-pill:hover {
    border-color: var(--primary);
    background: var(--bg-canvas);
}

.persona-pill.active-pill {
    border-color: var(--primary);
    background: var(--bg-active);
    box-shadow: inset 0 0 0 1px var(--primary);
}

.persona-pill strong {
    font-size: var(--text-sm);
    color: var(--text-primary);
}

.persona-pill span {
    font-size: var(--text-xs);
    color: var(--text-muted);
    margin-top: 4px;
}

/* Form Architecture */
.intake-form {
    background: var(--bg-subtle);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    margin-bottom: var(--space-5);
}

.form-grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: var(--space-4);
    margin-bottom: var(--space-4);
}

.form-field label {
    font-weight: 600;
    font-size: var(--text-sm);
    color: var(--text-primary);
    display: block;
    margin-bottom: 6px;
}

.form-control {
    width: 100%;
    padding: 9px 12px;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
    font-family: var(--font-sans);
    background: var(--bg-surface);
    color: var(--text-primary);
    accent-color: var(--primary);
    caret-color: var(--primary);
    transition: border-color 150ms ease, box-shadow 150ms ease;
}

.form-control:hover {
    border-color: var(--text-secondary);
}

.form-control:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12);
    outline: none;
}

.file-upload-bar {
    margin-top: var(--space-2);
    margin-bottom: var(--space-2);
    padding: var(--space-2) var(--space-3);
    background: var(--bg-surface);
    border: 1px dashed var(--border-strong);
    border-radius: var(--radius-sm);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-2);
    font-size: var(--text-xs);
    color: var(--text-secondary);
}

.form-helper {
    display: block;
    color: var(--text-muted);
    font-size: var(--text-xs);
    margin-top: 4px;
}

.skill-drawer {
    margin-bottom: var(--space-4);
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-sm);
    padding: var(--space-3) var(--space-4);
}

.skill-drawer summary {
    cursor: pointer;
    font-weight: 600;
    font-size: var(--text-sm);
    color: var(--primary);
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
    align-items: flex-start;
    gap: var(--space-2);
    padding: 7px 10px;
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    font-size: var(--text-xs);
    cursor: pointer;
    background: var(--bg-surface);
    transition: border-color 150ms ease, background-color 150ms ease;
}

.skill-check:hover {
    border-color: var(--primary-border);
    background: var(--bg-canvas);
}

.skill-check input[type="checkbox"] {
    margin-top: 2px;
    accent-color: var(--primary);
}

.skill-check small {
    color: var(--text-muted);
    display: block;
}

.form-actions-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-3);
}

.btn-primary {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    background: var(--primary);
    color: var(--primary-fg);
    border: 1px solid var(--primary);
    padding: 10px 18px;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-family: var(--font-sans);
    font-size: var(--text-sm);
    cursor: pointer;
    transition: background-color 150ms ease, transform 100ms ease;
}

.btn-primary:hover {
    background: var(--primary-hover);
}

.btn-primary:active {
    transform: translateY(1px);
}

.btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-surface);
    color: var(--text-secondary);
    border: 1px solid var(--border-default);
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-family: var(--font-sans);
    font-size: var(--text-xs);
    cursor: pointer;
    text-decoration: none;
    transition: border-color 150ms ease, color 150ms ease, background-color 150ms ease;
}

.btn-secondary:hover {
    border-color: var(--primary);
    color: var(--primary);
    background: var(--bg-canvas);
}

/* Active Profile Summary Strip inside Step 1 */
.profile-summary-bar {
    background: var(--bg-canvas);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: var(--space-3) var(--space-4);
    margin-top: var(--space-3);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-3);
    font-size: var(--text-sm);
}

/* Step 2: Scenario Selector Grid */
.scenario-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--space-3);
    margin-bottom: var(--space-4);
}

.scenario-tab {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: var(--space-4);
    border-radius: var(--radius-md);
    border: 1px solid var(--border-default);
    text-decoration: none;
    color: var(--text-primary);
    background: var(--bg-surface);
    transition: border-color 150ms ease, background-color 150ms ease, box-shadow 150ms ease;
}

.scenario-tab:hover {
    border-color: var(--primary);
    background: var(--bg-canvas);
}

.scenario-tab.active-scenario {
    border-color: var(--primary);
    background: var(--bg-active);
    box-shadow: inset 0 0 0 1px var(--primary);
}

.scenario-tab-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-2);
    margin-bottom: var(--space-2);
}

.scenario-tab strong {
    font-size: var(--text-base);
    line-height: 1.35;
}

.scenario-tab small {
    font-size: var(--text-xs);
    color: var(--text-muted);
}

/* Data Tables */
.table-scroll {
    overflow-x: auto;
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    background: var(--bg-surface);
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--text-sm);
    font-variant-numeric: tabular-nums;
}

.data-table th,
.data-table td {
    border-bottom: 1px solid var(--border-subtle);
    padding: 10px 14px;
    text-align: left;
    vertical-align: top;
}

.data-table tr:last-child td {
    border-bottom: none;
}

.data-table th {
    background: var(--bg-subtle);
    color: var(--text-secondary);
    font-weight: 600;
    font-size: var(--text-xs);
    white-space: nowrap;
}

.current-sc-row {
    background: var(--bg-active);
}

.sig-summary {
    font-size: var(--text-xs);
    color: var(--text-muted);
    margin-top: 4px;
    max-width: 70ch;
}

/* Sticky First Column for Employer/HR Heatmap */
.heatmap-table th:first-child,
.heatmap-table td:first-child {
    position: sticky;
    left: 0;
    background: var(--bg-surface);
    z-index: 2;
    border-right: 1px solid var(--border-default);
}

.heatmap-table th:first-child {
    background: var(--bg-subtle);
    z-index: 3;
}

/* Step 3: Role Evaluation Modules (Zero Card-in-Card Nesting) */
.roles-stack {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

.role-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-md);
    overflow: hidden;
    transition: border-color 150ms ease;
}

.role-card.top-rank-role {
    border-color: var(--primary-border);
}

.role-disclosure {
    width: 100%;
}

.role-disclosure > summary {
    list-style: none;
    cursor: pointer;
    padding: var(--space-4) var(--space-5);
    background: var(--bg-surface);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--space-4);
    flex-wrap: wrap;
    transition: background-color 150ms ease;
}

.role-disclosure > summary::-webkit-details-marker {
    display: none;
}

.role-disclosure > summary:hover {
    background: var(--bg-canvas);
}

.role-disclosure[open] > summary {
    border-bottom: 1px solid var(--border-subtle);
    background: var(--bg-canvas);
}

.role-title-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
    min-width: 240px;
}

.role-badges-row {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-2);
}

.rank-badge {
    display: inline-flex;
    align-items: center;
    background: var(--primary);
    color: var(--primary-fg);
    padding: 2px 9px;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: var(--text-xs);
    font-variant-numeric: tabular-nums;
}

.role-title-group h3 {
    margin: 2px 0 0;
    font-size: var(--text-lg);
    color: var(--text-primary);
}

.role-summary {
    margin: 0;
    color: var(--text-muted);
    font-size: var(--text-sm);
    max-width: 68ch;
}

.role-score-cluster {
    display: flex;
    align-items: center;
    gap: var(--space-4);
}

.score-box {
    background: var(--bg-active);
    border: 1px solid var(--primary-border);
    border-radius: var(--radius-sm);
    padding: 8px 14px;
    text-align: right;
    min-width: 115px;
}

.score-num {
    font-size: var(--text-xl);
    font-weight: 700;
    color: var(--primary);
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
}

.score-num span {
    font-size: var(--text-xs);
    color: var(--text-muted);
    font-weight: 500;
}

.score-label {
    font-size: 11px;
    color: var(--primary-hover);
    font-weight: 600;
}

.chevron-icon {
    color: var(--text-muted);
    transition: transform 180ms ease;
}

.role-disclosure[open] > summary .chevron-icon {
    transform: rotate(180deg);
}

/* Role Body Internal Layout (Dividers instead of nested cards) */
.role-body {
    padding: var(--space-5);
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
}

.explain-box {
    background: var(--bg-subtle);
    border: 1px solid var(--border-default);
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-sm);
    font-size: var(--text-sm);
}

.formula-breakdown {
    margin-top: var(--space-2);
    padding-top: var(--space-2);
    border-top: 1px solid var(--border-default);
    color: var(--text-secondary);
    font-size: var(--text-xs);
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-3);
}

.meter-bar {
    height: 6px;
    background: var(--bg-muted);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 4px;
    width: 100%;
    max-width: 160px;
}

.meter-fill {
    height: 100%;
    background: var(--primary);
    border-radius: 3px;
}

.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-5);
}

.structural-pane {
    padding-top: var(--space-3);
    border-top: 1px solid var(--border-subtle);
}

.structural-pane h4 {
    margin: 0 0 var(--space-2);
    font-size: var(--text-sm);
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 6px;
}

.structural-pane p {
    margin: 4px 0;
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.skill-group-label {
    font-size: var(--text-xs);
    font-weight: 600;
    color: var(--text-muted);
    margin: var(--space-2) 0 4px;
}

.citation-list {
    margin: var(--space-2) 0 0;
    padding-left: var(--space-5);
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.citation-list li {
    margin-bottom: 6px;
}

/* Connected Pathway Timeline (Replaces Nested Step Cards) */
.pathway-list {
    display: flex;
    flex-direction: column;
    gap: 0;
    margin-top: var(--space-3);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    background: var(--bg-surface);
    overflow: hidden;
}

.pathway-step {
    padding: var(--space-3) var(--space-4);
    border-bottom: 1px solid var(--border-subtle);
    display: grid;
    grid-template-columns: auto 1fr;
    gap: var(--space-3);
    align-items: start;
}

.pathway-step:last-child {
    border-bottom: none;
}

.step-index-circle {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: var(--status-success-bg);
    color: var(--status-success-fg);
    border: 1px solid var(--status-success-border);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: var(--text-xs);
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    margin-top: 2px;
}

.pathway-step-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: baseline;
    gap: var(--space-2);
    margin-bottom: 4px;
}

.pathway-step h4 {
    margin: 0;
    color: var(--text-primary);
    font-size: var(--text-base);
    font-weight: 600;
}

.verify-note {
    font-size: var(--text-xs);
    color: var(--text-muted);
    margin-top: 6px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
}

/* SDG & Uncertainty Notice Items */
.sdg-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.sdg-item {
    background: var(--bg-canvas);
    border: 1px solid var(--border-subtle);
    padding: var(--space-3);
    border-radius: var(--radius-sm);
}

.sdg-item strong {
    font-size: var(--text-sm);
    color: var(--status-info-fg);
    display: block;
    margin-bottom: 2px;
}

.uncertainty-panel {
    background: var(--status-warn-bg);
    border: 1px solid var(--status-warn-border);
    padding: var(--space-4);
    border-radius: var(--radius-md);
}

.uncertainty-panel h4 {
    color: var(--status-warn-fg);
}

/* Guardrail Alert Box */
.insufficient-box {
    background: var(--status-err-bg);
    color: var(--status-err-fg);
    border: 1px solid var(--status-err-border);
    border-radius: var(--radius-md);
    padding: var(--space-5);
    margin-bottom: var(--space-5);
}

.insufficient-box h3 {
    margin: 0 0 var(--space-2);
    display: flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-lg);
}

.panel-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-2);
}

.badge-time {
    background: var(--status-success-bg);
    color: var(--status-success-fg);
    border: 1px solid var(--status-success-border);
    padding: 3px 9px;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: var(--text-xs);
}

.small-note {
    color: var(--text-muted);
    font-size: var(--text-xs);
    margin-bottom: var(--space-2);
}

/* Signal Mode Bar */
.mode-bar {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
    margin-bottom: var(--space-4);
}

.mode-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 13px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-default);
    text-decoration: none;
    color: var(--text-secondary);
    font-size: var(--text-xs);
    font-weight: 600;
    background: var(--bg-surface);
    transition: border-color 150ms ease, background-color 150ms ease, color 150ms ease;
}

.mode-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.mode-btn.active-mode {
    background: var(--primary);
    color: var(--primary-fg);
    border-color: var(--primary);
}

/* Rising vs Declining Radar Panels */
.radar-panel-rising {
    border: 1px solid var(--status-success-border);
    background: var(--status-success-bg);
    border-radius: var(--radius-md);
    padding: var(--space-4);
}

.radar-panel-rising h4 {
    margin: 0 0 4px;
    color: var(--status-success-fg);
    font-size: var(--text-base);
    display: flex;
    align-items: center;
    gap: 6px;
}

.radar-panel-declining {
    border: 1px solid var(--status-err-border);
    background: var(--status-err-bg);
    border-radius: var(--radius-md);
    padding: var(--space-4);
}

.radar-panel-declining h4 {
    margin: 0 0 4px;
    color: var(--status-err-fg);
    font-size: var(--text-base);
    display: flex;
    align-items: center;
    gap: 6px;
}

footer {
    border-top: 1px solid var(--border-default);
    padding: var(--space-6);
    text-align: center;
    font-size: var(--text-xs);
    color: var(--text-muted);
    background: var(--bg-surface);
}

@media (max-width: 768px) {
    .app-header, .workspace-nav-bar, .container {
        padding-left: var(--space-4);
        padding-right: var(--space-4);
    }
    .card {
        padding: var(--space-4);
    }
    .exec-cell {
        border-right: none;
        border-bottom: 1px solid var(--border-subtle);
    }
    .exec-cell:last-child {
        border-bottom: none;
    }
    .step-jump-nav {
        display: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition: none !important;
        animation: none !important;
        scroll-behavior: auto !important;
    }
}
"""
