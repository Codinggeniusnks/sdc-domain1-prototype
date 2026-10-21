"""AI Skills Compass — SDC Hackathon 2026 (Domain 1: The Aiversecity Future-Ready Workforce Domain).

Runs as a zero-secret-required web application on Replit (`python src/main.py`) and locally.
Demonstrates the complete Domain 1 journey:
  Synthetic User Profile -> Dated AI/Market Signal Layer -> Explainable Role Ranking
  -> Skill Gaps -> Ordered Low-Cost Reskilling Pathway -> UN SDG Mapping -> Future Scenarios.
"""

from __future__ import annotations

import html
import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from matcher import normalize_profile_skills, rank_roles_for_profile
from signals import fetch_market_signals
from taxonomy import ROLES_CATALOG, SCENARIOS, SKILLS_CATALOG, SYNTHETIC_PROFILES
from utils import format_greeting, summarize


def esc(val: object) -> str:
    return html.escape(str(val) if val is not None else "")


def resolve_request_state(query_params: dict[str, list[str]]) -> dict:
    profile_id = (query_params.get("profile_id", ["aisyah_ops"])[0] or "aisyah_ops").strip()
    scenario_id = (query_params.get("scenario_id", ["moderate_copilot"])[0] or "moderate_copilot").strip()
    signal_mode = (query_params.get("signal_mode", ["fallback"])[0] or "fallback").strip()
    custom_skills_raw = query_params.get("skills", [])
    custom_name = (query_params.get("custom_name", [""])[0] or "").strip()
    cv_bio_text = (query_params.get("cv_bio_text", [""])[0] or "").strip()
    target_interest = (query_params.get("target_interest", [""])[0] or "").strip()
    experience_level = (query_params.get("experience_level", ["mid"])[0] or "mid").strip()

    selected_persona = next(
        (p for p in SYNTHETIC_PROFILES if p["id"] == profile_id),
        SYNTHETIC_PROFILES[0],
    )

    # If user submitted free-text CV/bio, extract skills automatically via whole-word taxonomy regex
    extracted_from_bio = []
    if cv_bio_text:
        extracted_from_bio, _ = extract_taxonomy_entities(cv_bio_text)

    if profile_id == "custom" or cv_bio_text:
        flat_skills: list[str] = list(extracted_from_bio)
        for item in custom_skills_raw:
            flat_skills.extend([s.strip() for s in item.split(",") if s.strip()])
        
        user_interests = [target_interest] if target_interest else []
        active_profile = {
            "id": "custom",
            "name": custom_name or ("Interactive Learner (Custom Intake)" if cv_bio_text else "Custom Synthetic Learner Profile"),
            "current_role": f"User-Entered Background ({experience_level.capitalize()} Level)",
            "persona_type": f"Interactive Custom Intake ({len(flat_skills)} skills detected)",
            "background_summary": cv_bio_text if cv_bio_text else "Custom synthetic skill combination entered for live judge evaluation (no real PII stored).",
            "skills": normalize_profile_skills(flat_skills),
            "interests": user_interests,
            "cv_bio_text": cv_bio_text,
            "experience_level": experience_level,
            "target_interest": target_interest,
        }
    else:
        active_profile = dict(selected_persona)
        if custom_skills_raw:
            flat_skills = []
            for item in custom_skills_raw:
                flat_skills.extend([s.strip() for s in item.split(",") if s.strip()])
            active_profile["skills"] = normalize_profile_skills(flat_skills)
        active_profile["cv_bio_text"] = ""
        active_profile["experience_level"] = "mid"
        active_profile["target_interest"] = active_profile.get("interests", [""])[0] if active_profile.get("interests") else ""

    signals_payload = fetch_market_signals(mode=signal_mode)
    evaluation = rank_roles_for_profile(
        profile=active_profile,
        signals_payload=signals_payload,
        scenario_id=scenario_id,
    )
    return {
        "profile_id": profile_id,
        "scenario_id": evaluation["scenario"]["id"],
        "signal_mode": signal_mode,
        "active_profile": active_profile,
        "signals_payload": signals_payload,
        "evaluation": evaluation,
    }


def render_dashboard_html(state: dict) -> str:
    prof = state["active_profile"]
    ev = state["evaluation"]
    sig_payload = state["signals_payload"]
    scenario = ev["scenario"]
    profile_skills_set = set(prof.get("skills", []))

    # Signal status banner styling
    if sig_payload["source_mode"] in ("live_arxiv", "live_feed") and not sig_payload["is_fallback"]:
        banner_class = "banner-live"
        badge_text = "LIVE PUBLIC FEED (OpenAlex / arXiv API)"
    elif sig_payload["source_mode"] == "malformed_test":
        banner_class = "banner-error"
        badge_text = "GUARDRAIL TEST: MALFORMED / EMPTY SIGNALS"
    else:
        banner_class = "banner-fallback"
        badge_text = "DATED SNAPSHOT FALLBACK (NOT LIVE)"

    # Persona buttons
    persona_links = []
    for p in SYNTHETIC_PROFILES:
        is_active = "active-pill" if state["profile_id"] == p["id"] else ""
        href = f"/?profile_id={urllib.parse.quote(p['id'])}&scenario_id={urllib.parse.quote(state['scenario_id'])}&signal_mode={urllib.parse.quote(state['signal_mode'])}"
        persona_links.append(
            f'<a href="{href}" class="persona-pill {is_active}" data-testid="persona-{esc(p["id"])}">'
            f'<strong>{esc(p["name"])}</strong><span>{esc(p["current_role"])}</span></a>'
        )

    # Scenario buttons
    scenario_links = []
    for sc_id, sc_info in SCENARIOS.items():
        is_active = "active-scenario" if state["scenario_id"] == sc_id else ""
        href = f"/?profile_id={urllib.parse.quote(state['profile_id'])}&scenario_id={urllib.parse.quote(sc_id)}&signal_mode={urllib.parse.quote(state['signal_mode'])}"
        scenario_links.append(
            f'<a href="{href}" class="scenario-tab {is_active}" data-testid="scenario-{esc(sc_id)}">'
            f'<span class="sc-badge">{esc(sc_info["badge"])}</span>'
            f'<strong>{esc(sc_info["name"])}</strong>'
            f'<small>{esc(sc_info["uncertainty_level"])}</small></a>'
        )

    # Signal mode buttons
    signal_modes = [
        ("fallback", "Reviewed Dated Snapshot (Reliable Default)"),
        ("live", "Fetch Live Research API Feed (OpenAlex / arXiv)"),
        ("malformed_test", "Simulate Malformed Signal Feed (Guardrail Check)"),
    ]
    sig_mode_links = []
    for m_id, m_label in signal_modes:
        is_active = "active-mode" if state["signal_mode"] == m_id else ""
        href = f"/?profile_id={urllib.parse.quote(state['profile_id'])}&scenario_id={urllib.parse.quote(state['scenario_id'])}&signal_mode={urllib.parse.quote(m_id)}"
        sig_mode_links.append(
            f'<a href="{href}" class="mode-btn {is_active}" data-testid="sigmode-{esc(m_id)}">{esc(m_label)}</a>'
        )

    # Skill checkboxes for custom/interactive refinement
    skill_checkboxes = []
    for sk_id, sk_info in SKILLS_CATALOG.items():
        checked = "checked" if sk_id in profile_skills_set else ""
        skill_checkboxes.append(
            f'<label class="skill-check"><input type="checkbox" name="skills" value="{esc(sk_id)}" {checked}>'
            f'<span>{esc(sk_info["name"])} <small>({esc(sk_info["category"])})</small></span></label>'
        )

    # Signals table rows
    signal_rows = []
    for sig in sig_payload.get("signals", []):
        sk_badges = "".join(
            f'<span class="tag tag-skill">{esc(SKILLS_CATALOG[s]["name"])}</span>'
            for s in sig.get("extracted_skills", [])
            if s in SKILLS_CATALOG
        )
        fb_tag = (
            '<span class="tag tag-amber">SNAPSHOT FALLBACK</span>'
            if sig.get("is_fallback")
            else '<span class="tag tag-green">LIVE RESEARCH API</span>'
        )
        signal_rows.append(
            f'<tr data-testid="signal-row">'
            f'<td>{fb_tag}<br><strong>{esc(sig["title"])}</strong><div class="sig-summary">{esc(sig.get("summary", ""))}</div></td>'
            f'<td class="mono">Pub: {esc(sig["published_date"])}<br>Ret: {esc(sig["retrieved_date"])}</td>'
            f'<td><a href="{esc(sig["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(sig["source_name"])}</a></td>'
            f'<td><div class="tag-wrap">{sk_badges}</div></td>'
            f'</tr>'
        )
    signals_table_html = (
        "".join(signal_rows)
        if signal_rows
        else '<tr><td colspan="4" class="empty-cell">Zero valid dated signals passed schema validation.</td></tr>'
    )

    # Role cards or Insufficient Evidence state
    top_guardrail_banner = ""
    if ev["status"] != "ok":
        warnings_list = "".join(f"<li>{esc(w)}</li>" for w in ev["signal_validation"].get("warnings", []))
        roles_section_html = f"""
        <div class="insufficient-box" role="alert" data-testid="insufficient-evidence-alert">
            <h3>Insufficient Evidence — Honest Guardrail Triggered</h3>
            <p><strong>Reason Code:</strong> <code class="mono">{esc(ev["reason"])}</code></p>
            <p>{esc(ev["message"])}</p>
            {f'<ul>{warnings_list}</ul>' if warnings_list else ''}
            <p class="guardrail-note">
                Why this matters for Domain 1: Rather than inventing a confident career prediction from an empty/sparse
                profile or unverified signal feed, AI Skills Compass halts ranking and shows what evidence is missing.
            </p>
        </div>
        """
        top_guardrail_banner = roles_section_html
        scenario_matrix_html = ""
    else:
        # Scenario comparison matrix
        comp_rows = []
        for comp in ev.get("scenario_comparison", []):
            is_cur = "current-sc-row" if comp["scenario_id"] == state["scenario_id"] else ""
            comp_rows.append(
                f'<tr class="{is_cur}">'
                f'<td><strong>{esc(comp["scenario_name"])}</strong><br><small>{esc(comp["assumptions"])}</small></td>'
                f'<td><span class="tag tag-amber">{esc(comp["uncertainty_level"])}</span></td>'
                f'<td><strong>#1 {esc(comp["top_role"])}</strong> ({esc(comp["top_role_score"])}/100)</td>'
                f'<td>#2 {esc(comp["runner_up_role"])} ({esc(comp["runner_up_score"])}/100)</td>'
                f'</tr>'
            )
        scenario_matrix_html = f"""
        <section class="card" aria-labelledby="scenario-matrix-heading" data-testid="scenario-comparison-section">
            <div class="section-header">
                <h2 id="scenario-matrix-heading">Multi-Scenario Uncertainty Comparison (Must-Have #6)</h2>
                <span class="tag tag-blue">Estimates, Not Single-Point Predictions</span>
            </div>
            <p class="section-sub">
                AI adoption speed and policy enforcement are uncertain. Compare how your top role rankings shift across three explicit future scenarios:
            </p>
            <div class="table-scroll">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Future Scenario & Explicit Assumptions</th>
                            <th>Uncertainty Band</th>
                            <th>#1 Ranked Role</th>
                            <th>#2 Runner-Up Role</th>
                        </tr>
                    </thead>
                    <tbody>{"".join(comp_rows)}</tbody>
                </table>
            </div>
        </section>
        """

        role_cards = []
        for role in ev["ranked_roles"]:
            bd = role["score_breakdown"]
            matched_req_html = (
                "".join(f'<span class="tag tag-green">✓ {esc(s["name"])}</span>' for s in role["matched_required_skills"])
                or '<span class="muted-inline">None yet</span>'
            )
            missing_req_html = (
                "".join(f'<span class="tag tag-gap">+ {esc(s["name"])}</span>' for s in role["missing_required_skills"])
                or '<span class="tag tag-green">All core required skills matched!</span>'
            )
            matched_sup_html = (
                "".join(f'<span class="tag tag-blue">✓ {esc(s["name"])}</span>' for s in role["matched_supporting_skills"])
                or '<span class="muted-inline">None yet</span>'
            )
            missing_sup_html = (
                "".join(f'<span class="tag tag-muted">+ {esc(s["name"])}</span>' for s in role["missing_supporting_skills"])
                or '<span class="muted-inline">None</span>'
            )

            sig_citations = []
            for cs in role["supporting_signals"]:
                mode_tag = "[Snapshot Fallback]" if cs.get("is_fallback") else "[Live Feed]"
                sig_citations.append(
                    f'<li><a href="{esc(cs["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(cs["title"])}</a> '
                    f'<span class="mono">({esc(cs["source_name"])}, Published {esc(cs["published_date"])}, Retrieved {esc(cs["retrieved_date"])} {mode_tag})</span> '
                    f'— Matched: <em>{esc(", ".join(cs["matched_skills"]))}</em></li>'
                )
            sig_citations_html = (
                f'<ul class="citation-list">{"".join(sig_citations)}</ul>'
                if sig_citations
                else '<p class="muted-inline">Insufficient role-specific signals in current window (score penalized).</p>'
            )

            pathway_steps = []
            for st in role["pathway"]["steps"]:
                sdg_badges = "".join(f'<span class="tag tag-sdg">{esc(t)}</span>' for t in st["sdg_tags"])
                pathway_steps.append(
                    f'<div class="pathway-step">'
                    f'<div class="step-num">Step {esc(st["step_number"])} · Stage {esc(st["stage"])} ({esc(st["priority"])})</div>'
                    f'<h4>{esc(st["skill_name"])} — <span class="mono">{esc(st["estimated_hours"])} hrs (~{esc(st["estimated_weeks"])} wk)</span></h4>'
                    f'<p><strong>Learning Objective:</strong> {esc(st["objective"])}</p>'
                    f'<p><strong>Verified Low-Cost / Free Option:</strong> <a href="{esc(st["resource_url"])}" target="_blank" rel="noopener noreferrer">{esc(st["resource_title"])}</a> '
                    f'<span class="tag tag-green">{esc(st["cost_tier"])}</span></p>'
                    f'<p class="verify-note">Provenance: {esc(st["verification_status"])} {sdg_badges}</p>'
                    f'</div>'
                )
            pathway_html = (
                "".join(pathway_steps)
                if pathway_steps
                else '<p class="tag tag-green">Your profile already satisfies all required and supporting skills for this role.</p>'
            )

            sdg_cards = []
            for sl in role["sdg_links"]:
                sdg_cards.append(
                    f'<div class="sdg-item">'
                    f'<strong>{esc(sl["sdg"])} ({esc(sl["target"])})</strong>'
                    f'<p>{esc(sl["explanation"])}</p>'
                    f'</div>'
                )

            role_cards.append(
                f"""
                <article class="role-card" data-testid="role-card-{esc(role['rank'])}">
                    <div class="role-header">
                        <div>
                            <span class="rank-badge">Rank #{esc(role["rank"])}</span>
                            <span class="tag tag-blue">{esc(role["category"])}</span>
                            <h3>{esc(role["title"])}</h3>
                            <p class="role-summary">{esc(role["summary"])}</p>
                        </div>
                        <div class="score-box">
                            <div class="score-num" data-testid="role-score-{esc(role['rank'])}">{esc(role["total_score"])}<span>/100</span></div>
                            <div class="score-label">Estimated Match</div>
                        </div>
                    </div>

                    <div class="explain-box">
                        <strong>Why This Role Ranks #{esc(role["rank"])}:</strong> {esc(role["why_ranked_here"])}
                        <div class="formula-breakdown mono">
                            Formula ({esc(bd["formula"])}):
                            Readiness = {esc(bd["skill_readiness_score"])}% |
                            Research Signal Coverage = {esc(bd["signal_momentum_score"])}% |
                            Scenario Fit = {esc(bd["scenario_fit_score"])}%
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="sub-panel">
                            <h4>Matched Profile Skills</h4>
                            <p><strong>Required Core Matched:</strong></p>
                            <div class="tag-wrap">{matched_req_html}</div>
                            <p style="margin-top:8px;"><strong>Supporting Matched:</strong></p>
                            <div class="tag-wrap">{matched_sup_html}</div>
                        </div>
                        <div class="sub-panel">
                            <h4>Identified Skill Gaps (To Reskill)</h4>
                            <p><strong>Missing Required Skills:</strong></p>
                            <div class="tag-wrap">{missing_req_html}</div>
                            <p style="margin-top:8px;"><strong>Missing Supporting Skills:</strong></p>
                            <div class="tag-wrap">{missing_sup_html}</div>
                        </div>
                    </div>

                    <div class="sub-panel">
                        <h4>Dated Research Signals (Scholarly Publications) Mentioning This Role's Skills</h4>
                        {sig_citations_html}
                    </div>

                    <div class="sub-panel" data-testid="pathway-section-{esc(role['rank'])}">
                        <div class="panel-title-row">
                            <h4>Ordered Low-Cost / Free Reskilling Pathway (Must-Have #4)</h4>
                            <span class="mono badge-time">Total Est: {esc(role["pathway"]["total_estimated_hours"])} hrs (~{esc(role["pathway"]["total_estimated_weeks"])} weeks)</span>
                        </div>
                        <p class="small-note">{esc(role["pathway"]["disclaimer"])}</p>
                        <div class="pathway-list">{pathway_html}</div>
                    </div>

                    <div class="grid-2">
                        <div class="sub-panel" data-testid="sdg-section-{esc(role['rank'])}">
                            <h4>UN SDG Alignment & Contribution (Must-Have #5)</h4>
                            {"".join(sdg_cards)}
                        </div>
                        <div class="sub-panel uncertainty-panel" data-testid="uncertainty-section-{esc(role['rank'])}">
                            <h4>Uncertainty, Limitations & Human-in-Charge Notice</h4>
                            <p><strong>Role Limitation:</strong> {esc(role["uncertainty_note"])}</p>
                            <p><strong>Active Scenario Assumption ({esc(scenario["name"])}):</strong> {esc(scenario["assumptions"])}</p>
                            <p><strong>Epistemic Boundary:</strong> Signals are dated scholarly AI publications (OpenAlex). They show research activity around a skill, NOT job postings, vacancy counts, hiring demand, or salaries in Malaysia. Final career decisions remain with the human learner.</p>
                        </div>
                    </div>
                </article>
                """
            )
        roles_section_html = "".join(role_cards)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Skills Compass — SDC Hackathon 2026 Domain 1 Prototype</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-primary: #1E40AF;
            --color-secondary: #2563EB;
            --color-accent: #B45309;
            --color-bg: #F8FAFC;
            --color-fg: #0F172A;
            --color-card: #FFFFFF;
            --color-muted: #EFF6FF;
            --color-muted-fg: #334155;
            --color-border: #CBD5E1;
            --color-success-bg: #DCFCE7;
            --color-success-fg: #14532D;
            --color-warn-bg: #FEF3C7;
            --color-warn-fg: #78350F;
            --color-err-bg: #FEE2E2;
            --color-err-fg: #7F1D1D;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: 'Fira Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--color-bg);
            color: var(--color-fg);
            line-height: 1.5;
        }}
        .mono {{ font-family: 'Fira Code', monospace; font-size: 0.88em; }}
        .skip-link {{
            position: absolute; left: -9999px; top: 8px;
            background: var(--color-primary); color: #fff; padding: 8px 14px; z-index: 999;
        }}
        .skip-link:focus {{ left: 12px; }}
        a:focus-visible, button:focus-visible, input:focus-visible {{
            outline: 3px solid var(--color-primary);
            outline-offset: 2px;
        }}
        header {{
            background: #0F172A;
            color: #FFFFFF;
            padding: 20px 24px;
            border-bottom: 4px solid var(--color-primary);
        }}
        .container {{ max-width: 1240px; margin: 0 auto; padding: 18px 20px 48px; }}
        .header-inner {{
            max-width: 1240px; margin: 0 auto;
            display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;
        }}
        .header-title h1 {{ margin: 0; font-size: 1.55rem; letter-spacing: -0.01em; }}
        .header-title p {{ margin: 4px 0 0; color: #CBD5E1; font-size: 0.92rem; }}
        .header-badges {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .top-banner {{
            padding: 12px 16px; border-radius: 8px; margin-bottom: 16px;
            display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;
            font-weight: 500; border: 1px solid transparent;
        }}
        .banner-live {{ background: var(--color-success-bg); color: var(--color-success-fg); border-color: #86EFAC; }}
        .banner-fallback {{ background: var(--color-warn-bg); color: var(--color-warn-fg); border-color: #FCD34D; }}
        .banner-error {{ background: var(--color-err-bg); color: var(--color-err-fg); border-color: #FCA5A5; }}
        .synthetic-guardrail {{
            background: #EFF6FF; border-left: 4px solid var(--color-primary);
            padding: 10px 14px; border-radius: 6px; margin-bottom: 18px; font-size: 0.92rem; color: #1E3A8A;
        }}
        .card {{
            background: var(--color-card); border: 1px solid var(--color-border);
            border-radius: 10px; padding: 18px 20px; margin-bottom: 20px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }}
        .section-header {{
            display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
            gap: 8px; margin-bottom: 10px;
        }}
        .section-header h2 {{ margin: 0; font-size: 1.2rem; color: #1E3A8A; }}
        .section-sub {{ margin: 0 0 12px; color: var(--color-muted-fg); font-size: 0.93rem; }}
        .persona-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-bottom: 14px;
        }}
        .persona-pill {{
            display: flex; flex-direction: column; padding: 12px 14px; border-radius: 8px;
            border: 1.5px solid var(--color-border); text-decoration: none; color: var(--color-fg);
            background: #F8FAFC; transition: background-color 150ms ease, border-color 150ms ease;
        }}
        .persona-pill:hover {{ border-color: var(--color-secondary); background: #EFF6FF; }}
        .persona-pill.active-pill {{
            border-color: var(--color-primary); background: #DBEAFE; color: #1E3A8A;
        }}
        .persona-pill span {{ font-size: 0.83rem; color: var(--color-muted-fg); margin-top: 3px; }}
        .scenario-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; margin-bottom: 12px;
        }}
        .scenario-tab {{
            display: flex; flex-direction: column; padding: 12px 14px; border-radius: 8px;
            border: 1.5px solid var(--color-border); text-decoration: none; color: var(--color-fg);
            background: #F8FAFC;
        }}
        .scenario-tab.active-scenario {{
            border-color: var(--color-primary); background: #DBEAFE; color: #1E3A8A;
        }}
        .sc-badge {{
            display: inline-block; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
            color: var(--color-accent); margin-bottom: 4px;
        }}
        .mode-bar {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }}
        .mode-btn {{
            padding: 8px 12px; border-radius: 6px; border: 1px solid var(--color-border);
            text-decoration: none; color: var(--color-fg); font-size: 0.88rem; font-weight: 500; background: #F8FAFC;
        }}
        .mode-btn.active-mode {{ background: var(--color-primary); color: #FFFFFF; border-color: var(--color-primary); }}
        .skills-grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 8px; margin: 10px 0 14px;
        }}
        .skill-check {{
            display: flex; align-items: flex-start; gap: 8px; padding: 6px 8px;
            border: 1px solid #E2E8F0; border-radius: 6px; font-size: 0.87rem; cursor: pointer; background: #fff;
        }}
        .skill-check small {{ color: #64748B; }}
        .btn-primary {{
            background: var(--color-primary); color: #FFFFFF; border: none; padding: 9px 16px;
            border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 0.92rem;
        }}
        .btn-primary:hover {{ background: #1E3A8A; }}
        .table-scroll {{ overflow-x: auto; }}
        .data-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        .data-table th, .data-table td {{
            border-bottom: 1px solid #E2E8F0; padding: 10px 12px; text-align: left; vertical-align: top;
        }}
        .data-table th {{ background: #F1F5F9; color: #1E3A8A; font-weight: 600; }}
        .current-sc-row {{ background: #EFF6FF; }}
        .sig-summary {{ font-size: 0.83rem; color: #475569; margin-top: 4px; }}
        .tag-wrap {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .tag {{
            display: inline-block; padding: 3px 8px; border-radius: 5px; font-size: 0.78rem; font-weight: 600;
        }}
        .tag-skill {{ background: #E0F2FE; color: #0369A1; }}
        .tag-green {{ background: var(--color-success-bg); color: var(--color-success-fg); }}
        .tag-amber {{ background: var(--color-warn-bg); color: var(--color-warn-fg); }}
        .tag-gap {{ background: #FEE2E2; color: #991B1B; }}
        .tag-blue {{ background: #DBEAFE; color: #1E40AF; }}
        .tag-muted {{ background: #F1F5F9; color: #334155; }}
        .tag-sdg {{ background: #EDE9FE; color: #5B21B6; }}
        .role-card {{
            background: #FFFFFF; border: 1.5px solid var(--color-border); border-radius: 10px;
            padding: 18px 20px; margin-bottom: 18px;
        }}
        .role-header {{
            display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;
        }}
        .role-header h3 {{ margin: 6px 0 4px; font-size: 1.25rem; color: #0F172A; }}
        .role-summary {{ margin: 0; color: var(--color-muted-fg); font-size: 0.94rem; }}
        .rank-badge {{
            display: inline-block; background: var(--color-primary); color: #fff;
            padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.82rem; margin-right: 6px;
        }}
        .score-box {{
            background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px;
            padding: 10px 14px; text-align: center; min-width: 120px;
        }}
        .score-num {{ font-size: 1.55rem; font-weight: 700; color: var(--color-primary); font-family: 'Fira Code', monospace; }}
        .score-num span {{ font-size: 0.85rem; color: #475569; }}
        .score-label {{ font-size: 0.76rem; color: #1E3A8A; font-weight: 600; }}
        .explain-box {{
            background: #F8FAFC; border-left: 4px solid var(--color-secondary);
            padding: 10px 12px; margin: 12px 0; border-radius: 4px; font-size: 0.91rem;
        }}
        .formula-breakdown {{ margin-top: 6px; color: #334155; font-size: 0.82rem; }}
        .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; margin: 12px 0; }}
        .sub-panel {{
            background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px;
        }}
        .sub-panel h4 {{ margin: 0 0 8px; font-size: 0.98rem; color: #1E3A8A; }}
        .sub-panel p {{ margin: 4px 0; font-size: 0.89rem; }}
        .citation-list {{ margin: 6px 0 0; padding-left: 18px; font-size: 0.88rem; }}
        .citation-list li {{ margin-bottom: 6px; }}
        .pathway-list {{ display: grid; gap: 10px; margin-top: 10px; }}
        .pathway-step {{
            background: #FFFFFF; border: 1px solid #CBD5E1; border-left: 4px solid #059669;
            border-radius: 6px; padding: 10px 12px;
        }}
        .pathway-step h4 {{ margin: 4px 0; color: #0F172A; font-size: 0.95rem; }}
        .step-num {{ font-size: 0.76rem; font-weight: 700; color: #047857; text-transform: uppercase; }}
        .verify-note {{ font-size: 0.8rem; color: #475569; }}
        .sdg-item {{
            background: #FFFFFF; border: 1px solid #DDD6FE; border-left: 4px solid #7C3AED;
            padding: 8px 10px; border-radius: 6px; margin-bottom: 8px;
        }}
        .uncertainty-panel {{ background: #FFFBEB; border-color: #FDE68A; }}
        .insufficient-box {{
            background: var(--color-err-bg); color: var(--color-err-fg);
            border: 2px solid #F87171; border-radius: 10px; padding: 18px 20px; margin-bottom: 20px;
        }}
        .insufficient-box h3 {{ margin-top: 0; }}
        .panel-title-row {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }}
        .badge-time {{ background: #DCFCE7; color: #14532D; padding: 3px 8px; border-radius: 4px; font-weight: 600; }}
        .small-note {{ color: #475569; font-size: 0.83rem; margin-bottom: 8px; }}
        footer {{
            border-top: 1px solid var(--color-border); padding: 18px 20px; text-align: center;
            font-size: 0.85rem; color: var(--color-muted-fg); background: #fff;
        }}
        @media (prefers-reduced-motion: reduce) {{
            * {{ transition: none !important; animation: none !important; }}
        }}
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <header>
        <div class="header-inner">
            <div class="header-title">
                <h1>AI Skills Compass</h1>
                <p>SDC Hackathon 2026 · Domain 1 (The Aiversecity Future-Ready Workforce Domain)</p>
            </div>
            <div class="header-badges">
                <span class="tag tag-blue">SDG 4 (4.3, 4.4) & SDG 8 (8.2, 8.5)</span>
                <span class="tag tag-green">Human-in-Charge Advisory</span>
                <span class="tag tag-amber">Synthetic Profiles Only</span>
            </div>
        </div>
    </header>

    <main id="main-content" class="container">
        <div class="top-banner {banner_class}" role="status" data-testid="signal-status-banner">
            <div>
                <strong>[{esc(badge_text)}]</strong> {esc(sig_payload.get("banner_label", ""))}
            </div>
            <div class="mono">Valid Signals: {len(sig_payload.get("signals", []))}</div>
        </div>

        <div class="synthetic-guardrail" data-testid="synthetic-data-notice">
            <strong>Data & Privacy Guardrail (Domain 1 Rule §6):</strong> This prototype uses <strong>synthetic personas and public dated research-publication signals only</strong>. Do not enter real personal identifiers or upload real CVs. Every recommendation cites its dated signal source and never fabricates courses, job statistics, or hiring guarantees. This prototype has no vacancy or hiring data source.
            <div style="margin-top:6px; font-weight:600;">
                Quick Judge Navigation:
                <a href="#step1-heading" style="color:#1E40AF; margin-right:10px;">1. Profile Intake</a> ·
                <a href="#step2-heading" style="color:#1E40AF; margin:0 10px;">2. Future Scenarios</a> ·
                <a href="#step3-heading" style="color:#1E40AF; margin:0 10px;">3. Ranked Roles, Pathways &amp; SDGs</a> ·
                <a href="#step4-heading" style="color:#1E40AF; margin-left:10px;">4. Dated Research Signal Radar</a>
            </div>
        </div>

        {top_guardrail_banner}

        <!-- STEP 1: PROFILE INTAKE -->
        <section class="card" aria-labelledby="step1-heading" data-testid="profile-intake-section">
            <div class="section-header">
                <h2 id="step1-heading">1. Skills Profile Intake — "Tell Us About Yourself" (Must-Have #1)</h2>
                <span class="tag tag-blue">Active Profile: {esc(prof["name"])}</span>
            </div>
            <p class="section-sub">
                Enter your skills, experience, and interests through the <strong>interactive CV/bio questionnaire</strong> below, or select a pre-built synthetic Malaysian worker persona:
            </p>

            <!-- INTERACTIVE QUESTIONNAIRE & CV PASTE FORM -->
            <form method="GET" action="/" class="intake-form" data-testid="interactive-intake-form" style="background:#F1F5F9; border:1px solid #CBD5E1; border-radius:8px; padding:16px; margin-bottom:16px;">
                <input type="hidden" name="profile_id" value="custom">
                <input type="hidden" name="scenario_id" value="{esc(state['scenario_id'])}">
                <input type="hidden" name="signal_mode" value="{esc(state['signal_mode'])}">
                
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:12px; margin-bottom:12px;">
                    <div>
                        <label style="font-weight:600; font-size:0.88rem; color:#1E293B; display:block; margin-bottom:4px;">
                            Your Name / Identifier (Synthetic Only):
                        </label>
                        <input type="text" name="custom_name" value="{esc(prof.get('name', 'Custom Learner'))}" placeholder="e.g. Farhan Tan / Fresh Grad" style="width:100%; padding:8px 10px; border:1px solid #94A3B8; border-radius:6px; font-size:0.9rem;">
                    </div>
                    <div>
                        <label style="font-weight:600; font-size:0.88rem; color:#1E293B; display:block; margin-bottom:4px;">
                            Experience Level:
                        </label>
                        <select name="experience_level" style="width:100%; padding:8px 10px; border:1px solid #94A3B8; border-radius:6px; font-size:0.9rem; background:#fff;">
                            <option value="entry" {"selected" if prof.get("experience_level") == "entry" else ""}>Fresh Graduate / Career Switcher (&lt; 2 yrs)</option>
                            <option value="mid" {"selected" if prof.get("experience_level") in ("mid", None) else ""}>Mid-Level Practitioner (2–6 yrs)</option>
                            <option value="senior" {"selected" if prof.get("experience_level") == "senior" else ""}>Senior Specialist / Lead (&gt; 6 yrs)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-weight:600; font-size:0.88rem; color:#1E293B; display:block; margin-bottom:4px;">
                            Career Interest Track:
                        </label>
                        <select name="target_interest" style="width:100%; padding:8px 10px; border:1px solid #94A3B8; border-radius:6px; font-size:0.9rem; background:#fff;">
                            <option value="">Explore All Emerging AI Tracks</option>
                            <option value="operations" {"selected" if prof.get("target_interest") == "operations" else ""}>Operations & Process Optimization</option>
                            <option value="quality assurance" {"selected" if prof.get("target_interest") == "quality assurance" else ""}>Quality Assurance & LLM Evaluation</option>
                            <option value="governance" {"selected" if prof.get("target_interest") == "governance" else ""}>AI Ethics, PDPA & Governance</option>
                            <option value="engineering" {"selected" if prof.get("target_interest") == "engineering" else ""}>RAG & Knowledge Engineering</option>
                            <option value="sustainability" {"selected" if prof.get("target_interest") == "sustainability" else ""}>Green Tech & ESG Analytics</option>
                        </select>
                    </div>
                </div>

                <div style="margin-bottom:12px;">
                    <label style="font-weight:600; font-size:0.88rem; color:#1E293B; display:block; margin-bottom:4px;">
                        Paste Sample CV / Experience Bio / Skill Summary (Domain 1 Item #1):
                    </label>
                    <textarea name="cv_bio_text" rows="3" placeholder="Paste your background, e.g.: 'Operations analyst with 3 years experience. Skilled in workflow automation, process mapping, and basic SQL data analysis. Interested in prompt engineering and human-in-the-loop quality evaluation.'" style="width:100%; padding:8px 10px; border:1px solid #94A3B8; border-radius:6px; font-size:0.88rem; font-family:inherit;">{esc(prof.get("cv_bio_text", ""))}</textarea>
                    <small style="color:#64748B; font-size:0.8rem;">
                        Our whole-word regex parser automatically detects and matches your skills against the 16 reviewed taxonomy competencies without sending your text to any external third-party server.
                    </small>
                </div>

                <details style="margin-bottom:12px; background:#fff; border:1px solid #CBD5E1; border-radius:6px; padding:10px;">
                    <summary style="cursor:pointer; font-weight:600; color:#1E40AF;">
                        Or Manually Fine-Tune Skill Checkboxes ({len(profile_skills_set)} of {len(SKILLS_CATALOG)} selected)
                    </summary>
                    <div class="skills-grid" style="margin-top:10px;">
                        {"".join(skill_checkboxes)}
                    </div>
                </details>

                <button type="submit" class="btn-primary" style="background:#2563EB; color:#fff; font-weight:700; padding:10px 18px; border:none; border-radius:6px; cursor:pointer;" data-testid="apply-skills-btn">
                    🔍 Analyze Profile & Match Future Roles
                </button>
            </form>

            <div style="margin-top:16px;">
                <p style="font-weight:600; font-size:0.88rem; color:#475569; margin-bottom:6px;">
                    Or quick-test pre-built Malaysian personas:
                </p>
                <div class="persona-grid">
                    {"".join(persona_links)}
                </div>
            </div>

            <div class="sub-panel" style="margin-top:10px;">
                <p><strong>Current Active Background:</strong> {esc(prof["current_role"])} ({esc(prof["persona_type"])})</p>
                <p><strong>Detected Skills ({len(profile_skills_set)}):</strong> {", ".join([SKILLS_CATALOG[s]["name"] for s in prof.get("skills", []) if s in SKILLS_CATALOG]) or '<span class="tag tag-gap">None detected (Guardrail active)</span>'}</p>
            </div>
        </section>

        <!-- STEP 2: SCENARIO SELECTOR -->
        <section class="card" aria-labelledby="step2-heading" data-testid="scenario-selector-section">
            <div class="section-header">
                <h2 id="step2-heading">2. Future Scenario Selection — Handling Uncertainty (Must-Have #6)</h2>
                <span class="tag tag-amber">{esc(scenario["uncertainty_level"])}</span>
            </div>
            <p class="section-sub">Switch scenarios to observe how different AI disruption speeds and sustainability mandates shift role rankings:</p>
            <div class="scenario-grid">
                {"".join(scenario_links)}
            </div>
            <div class="sub-panel">
                <p><strong>Active Scenario Assumptions:</strong> {esc(scenario["assumptions"])}</p>
            </div>
        </section>

        {scenario_matrix_html}

        <!-- STEP 3: EXPLAINABLE ROLE MATCHING, PATHWAYS & SDG MAP -->
        <section class="card" aria-labelledby="step3-heading" data-testid="ranked-roles-section">
            <div class="section-header">
                <h2 id="step3-heading">3. Explainable Future-Role Rankings, Skill Gaps, Pathways & SDG Links (Must-Haves #3, #4, #5)</h2>
                <span class="tag tag-green">Deterministic & Inspectable Scoring</span>
            </div>
            <p class="section-sub">
                Each role is scored transparently using <code>0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit</code>.
                No black-box LLM scores, unverified courses, or fabricated job statistics are used.
            </p>
            {roles_section_html}
        </section>

        <!-- STEP 4: DATED AI RESEARCH SIGNAL LAYER -->
        <section class="card" aria-labelledby="step4-heading" data-testid="signals-radar-section">
            <div class="section-header">
                <h2 id="step4-heading">4. Future Skills Radar — Dated AI Research Signal Layer (Must-Have #2)</h2>
                <span class="mono">Source Mode: {esc(sig_payload["source_mode"])}</span>
            </div>
            <p class="section-sub">
                Toggle between the dated OpenAlex snapshot, a live OpenAlex fetch (arXiv as backup), or the malformed-signal guardrail test. These are research publications, not job-market or vacancy data:
            </p>
            <div class="mode-bar">
                {"".join(sig_mode_links)}
            </div>
            <div class="table-scroll">
                <table class="data-table" data-testid="signals-table">
                    <thead>
                        <tr>
                            <th>Signal Title & Summary</th>
                            <th>Dates (ISO-8601)</th>
                            <th>Attributed Source</th>
                            <th>Extracted Reviewed Taxonomy Skills</th>
                        </tr>
                    </thead>
                    <tbody>
                        {signals_table_html}
                    </tbody>
                </table>
            </div>
        </section>
    </main>

    <footer>
        <p>
            <strong>AI Skills Compass</strong> · Built for SDC Hackathon 2026 (Domain 1: Aiversecity Future-Ready Workforce) ·
            Context figures quoted from the SDC 2026 Domain 1 brief (not independently re-verified by this team): Hays Asia Salary Guide 2025 (56% use AI at work vs 26% formally trained, Malaysia) & MOSTI (600,000+ workers needing reskilling) ·
            Licensed under Apache License 2.0.
        </p>
    </footer>
</body>
</html>
"""


class CompassRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        # Keep console output clean and structured
        sys.stderr.write(f"[AI-Skills-Compass] {self.address_string()} - {fmt % args}\n")

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if parsed.path == "/api/health":
            self._send_json(200, {"status": "ok", "service": "AI Skills Compass", "domain": "Domain 1"})
            return

        if parsed.path == "/api/signals":
            mode = (query_params.get("signal_mode", ["fallback"])[0] or "fallback").strip()
            payload = fetch_market_signals(mode=mode)
            self._send_json(200, payload)
            return

        if parsed.path == "/api/evaluate":
            state = resolve_request_state(query_params)
            self._send_json(
                200,
                {
                    "profile": state["active_profile"],
                    "evaluation": state["evaluation"],
                },
            )
            return

        if parsed.path in ("/", "/index.html"):
            state = resolve_request_state(query_params)
            body = render_dashboard_html(state).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self._send_json(404, {"error": "Not found"})

    def _send_json(self, status_code: int, data: dict) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_self_check() -> int:
    """Run an end-to-end verification of the full slice and print summary."""
    project_name = os.getenv("PROJECT_NAME", "AI Skills Compass")
    print(format_greeting(project_name))
    state = resolve_request_state(
        {"profile_id": ["aisyah_ops"], "scenario_id": ["moderate_copilot"], "signal_mode": ["fallback"]}
    )
    ev = state["evaluation"]
    scores = [r["total_score"] for r in ev["ranked_roles"]]
    print(f"Result: {summarize(scores)}")
    print(f"Top Role (#1): {ev['ranked_roles'][0]['title']} ({ev['ranked_roles'][0]['total_score']}/100)")
    return 0


def main() -> None:
    if "--self-check" in sys.argv:
        raise SystemExit(run_self_check())

    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "0.0.0.0")
    run_self_check()
    server = ThreadingHTTPServer((host, port), CompassRequestHandler)
    print(f"AI Skills Compass running at http://127.0.0.1:{port} (bound to {host}:{port})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    main()
