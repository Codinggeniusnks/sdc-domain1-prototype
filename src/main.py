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
from signals import extract_taxonomy_entities, fetch_market_signals
from taxonomy import ROLES_CATALOG, SCENARIOS, SKILLS_CATALOG, SYNTHETIC_PROFILES
from ui_theme import DESIGN_SYSTEM_CSS, icon_svg
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
    view_mode = (query_params.get("view", ["individual"])[0] or "individual").strip()

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
        "view_mode": view_mode,
        "active_profile": active_profile,
        "signals_payload": signals_payload,
        "evaluation": evaluation,
    }


def build_rising_declining_radar_html() -> str:
    """Builds the Rising vs. Declining Skills & Roles Radar (Domain 1 Part 3 #2 & Part 4 #2)."""
    rising_items = [
        ("Agentic Workflow Automation", "High (+40% Signal Surge)", "OpenAlex Live / arXiv", "Multi-step LLM task decomposition, enterprise SOP automation, and tool-use orchestration."),
        ("Human-in-the-Loop QA & Evaluation", "Critical Reliability Bottleneck", "Hays 2025 / OpenAlex", "Auditing hallucination rates, red-teaming, output validation, and factual verification."),
        ("AI Ethics & PDPA Data Governance", "Mandatory Regulatory Push", "MOSTI Guidelines", "Data privacy compliance, bias mitigation, and transparency documentation."),
        ("RAG & Grounded Vector Knowledge Systems", "Standard Enterprise Stack", "OpenAlex Works", "Retrieval-augmented generation, citation grounding, and domain-specific knowledge bases."),
        ("Carbon-Aware Analytics & Green AI", "ESG Compliance Schedule", "Bursa Malaysia / UN SDG", "Energy-efficient compute scheduling, Scope 2/3 IT telemetry, and green software."),
    ]

    declining_items = [
        ("Repetitive Clerical Copy-Pasting & Manual Data Entry", "High Automation Risk", "Displaced by automated API integrations and agentic spreadsheet processing."),
        ("Unverified First-Draft Content Writing", "Vulnerable to Hallucination", "Replaced by structured prompt workflows with human-in-the-loop review."),
        ("Routine Boilerplate Script Translation", "High AI Assistant Saturation", "Automated by IDE coding assistants; durable value shifts to architecture and testing."),
        ("Static Annual Training Schedules", "Declining Relevance", "Shifting to continuous micro-learning and modular competency-based reskilling."),
    ]

    rising_rows = "".join(
        f'<tr><td><strong style="color:var(--status-success-fg);">{esc(item[0])}</strong>'
        f'<div class="sig-summary">{esc(item[3])}</div></td>'
        f'<td><span class="tag tag-green">{esc(item[1])}</span></td>'
        f'<td class="mono">{esc(item[2])}</td></tr>'
        for item in rising_items
    )

    declining_rows = "".join(
        f'<tr><td><strong style="color:var(--status-err-fg);">{esc(item[0])}</strong>'
        f'<div class="sig-summary">{esc(item[2])}</div></td>'
        f'<td><span class="tag tag-gap">{esc(item[1])}</span></td></tr>'
        for item in declining_items
    )

    return f"""
    <div class="grid-2" style="margin-bottom:var(--space-5);" data-testid="rising-declining-radar">
        <div class="radar-panel-rising">
            <h4>{icon_svg("trend_up")} Top Rising Competencies & Emerging Roles (Domain 1 Part 3 #2)</h4>
            <p class="small-note">Backed by dated OpenAlex scholarly publications and industry trend momentum:</p>
            <div class="table-scroll">
                <table class="data-table">
                    <thead><tr><th>Emerging Competency &amp; Focus</th><th>Trend Signal</th><th>Source</th></tr></thead>
                    <tbody>{rising_rows}</tbody>
                </table>
            </div>
        </div>
        <div class="radar-panel-declining">
            <h4>{icon_svg("trend_down")} Declining & Highly Automated Routine Tasks</h4>
            <p class="small-note">Workforce areas facing high displacement without continuous human reskilling:</p>
            <div class="table-scroll">
                <table class="data-table">
                    <thead><tr><th>Routine Vulnerable Task / Practice</th><th>Impact Status</th></tr></thead>
                    <tbody>{declining_rows}</tbody>
                </table>
            </div>
        </div>
    </div>
    """


def build_employer_hr_view_html(active_scenario_id: str, active_signal_mode: str) -> str:
    """Builds the Employer / HR Workforce Skills-Gap Heatmap (Domain 1 Part 5 Good-to-Have #1)."""
    cohort = [
        {"id": "aisyah_ops", "name": "Aisyah Rahman", "dept": "Operations & Logistics", "role": "Junior Operations Coordinator", "skills": ["ai_literacy", "process_mapping", "sql_data_analysis", "stakeholder_communication"]},
        {"id": "wei_jie_qa", "name": "Wei Jie Tan", "dept": "Quality & Software", "role": "Software QA Analyst", "skills": ["python_scripting", "human_in_the_loop_qa", "sql_data_analysis", "api_integration"]},
        {"id": "priya_esg", "name": "Priya Nair", "dept": "Sustainability & Admin", "role": "Sustainability & Admin Officer", "skills": ["esg_sustainability_reporting", "data_visualization", "carbon_footprint_analytics", "stakeholder_communication"]},
    ]

    all_skill_keys = list(SKILLS_CATALOG.keys())
    coverage_counts = {sk: sum(1 for p in cohort if sk in p["skills"]) for sk in all_skill_keys}

    heatmap_rows = []
    for p in cohort:
        cells = []
        for sk in all_skill_keys:
            if sk in p["skills"]:
                cells.append(f'<td style="background:var(--status-success-bg); text-align:center; color:var(--status-success-fg); font-weight:700;" title="{esc(p["name"])}: {esc(SKILLS_CATALOG[sk]["name"])} (Verified)">{icon_svg("check")}</td>')
            else:
                cells.append(f'<td style="background:var(--status-err-bg); text-align:center; color:var(--status-err-fg);" title="{esc(p["name"])}: Missing {esc(SKILLS_CATALOG[sk]["name"])}">—</td>')
        heatmap_rows.append(
            f'<tr><td><strong>{esc(p["name"])}</strong><div class="sig-summary">{esc(p["role"])}</div></td><td>{esc(p["dept"])}</td>'
            + "".join(cells) + "</tr>"
        )

    header_skill_cells = "".join(
        f'<th title="{esc(SKILLS_CATALOG[sk]["name"])}" style="font-size:11px; max-width:90px; white-space:normal; line-height:1.25; vertical-align:bottom;">{esc(SKILLS_CATALOG[sk]["name"].split("&")[0].strip())}</th>'
        for sk in all_skill_keys
    )

    coverage_summary_cells = []
    for sk in all_skill_keys:
        cnt = coverage_counts[sk]
        pct = int(cnt / len(cohort) * 100)
        bg = "var(--status-success-bg)" if pct >= 66 else ("var(--status-warn-bg)" if pct >= 33 else "var(--status-err-bg)")
        fg = "var(--status-success-fg)" if pct >= 66 else ("var(--status-warn-fg)" if pct >= 33 else "var(--status-err-fg)")
        coverage_summary_cells.append(f'<td class="tabular" style="background:{bg}; color:{fg}; font-weight:700; text-align:center; font-size:var(--text-xs);">{pct}%</td>')

    return f"""
    <section class="card" aria-labelledby="hr-view-heading" data-testid="hr-workforce-section">
        <div class="section-header">
            <h2 id="hr-view-heading">{icon_svg("building")} Employer / HR Workforce Skills-Gap Heatmap (Domain 1 Part 5 Feature)</h2>
            <span class="tag tag-blue">Cohort Size: {len(cohort)} Synthetic Employees</span>
        </div>
        <p class="section-sub">
            A company-level workforce diagnostic showing department-wide skill coverage, organizational blind spots, and HRD Corp claimable team reskilling recommendations:
        </p>

        <div class="table-scroll">
            <table class="data-table heatmap-table">
                <thead>
                    <tr>
                        <th>Team Member</th>
                        <th>Department</th>
                        {header_skill_cells}
                    </tr>
                </thead>
                <tbody>
                    {"".join(heatmap_rows)}
                    <tr style="border-top:2px solid var(--border-strong); font-weight:700;">
                        <td colspan="2">Team Capability Coverage (%)</td>
                        {"".join(coverage_summary_cells)}
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="grid-2" style="margin-top:var(--space-5);">
            <div class="structural-pane">
                <h4>{icon_svg("alert")} Immediate Team-Level Reskilling Priorities</h4>
                <ul class="citation-list">
                    <li><strong>Critical Blind Spot (0% Team Coverage):</strong> <em>Prompt Engineering</em>, <em>Workflow Automation (Agentic)</em>, and <em>RAG Knowledge Systems</em>. None of the current team members possess formal production experience in these emerging areas.</li>
                    <li><strong>Governance Vulnerability (0% Coverage):</strong> Zero team members trained in <em>AI Ethics &amp; PDPA Governance</em>, exposing automated processes to regulatory and data-leak risks.</li>
                </ul>
            </div>
            <div class="structural-pane">
                <h4>{icon_svg("book")} Recommended Cohort Learning Program (HRD Corp Claimable)</h4>
                <ul class="citation-list">
                    <li><strong>Cohort 1 (All Staff):</strong> Enroll in <em>Malaysia AI Untuk Rakyat</em> (Citizens &amp; Intel) to establish baseline literacy in 1 week.</li>
                    <li><strong>Cohort 2 (Operations &amp; QA):</strong> <em>HRD Corp e-LATiH Python &amp; Process Automation</em> track (40 hours).</li>
                    <li><strong>Cohort 3 (Legal / HR / Leads):</strong> <em>Malaysia MOSTI AI Governance Guidelines &amp; NIST AI RMF</em> workshop (24 hours).</li>
                </ul>
            </div>
        </div>
    </section>
    """


def build_executive_summary_html(prof: dict, ev: dict, scenario: dict, sig_payload: dict, skill_count: int) -> str:
    """Renders the top Executive Readiness Summary Strip so the user immediately understands state & next action."""
    if ev["status"] == "ok" and ev.get("ranked_roles"):
        top = ev["ranked_roles"][0]
        top_title = esc(top["title"])
        top_score = f"{esc(top['total_score'])} / 100"
        top_score_val = float(top["total_score"])
        pw_hours = f"{esc(top['pathway']['total_estimated_hours'])} hrs (~{esc(top['pathway']['total_estimated_weeks'])} wks)"
        missing_count = len(top["missing_required_skills"])
        gap_summary = f"{missing_count} core skill gap(s) to close" if missing_count > 0 else "All core skills satisfied"
    else:
        top_title = "Guardrail Active — Ranking Halted"
        top_score = "Insufficient Evidence"
        top_score_val = 0.0
        pw_hours = "Select ≥2 skills to compute"
        gap_summary = f"Reason: {esc(ev.get('reason', 'validation_halted'))}"

    return f"""
    <div class="exec-summary-grid" role="region" aria-label="Executive Readiness Summary">
        <div class="exec-cell">
            <span class="exec-label">{icon_svg("user")} Active Learner Profile</span>
            <div class="exec-value">{esc(prof["name"])}</div>
            <span class="exec-sub">{skill_count} of {len(SKILLS_CATALOG)} taxonomy skills detected</span>
        </div>
        <div class="exec-cell">
            <span class="exec-label">{icon_svg("compass")} #1 Recommended Role Match</span>
            <div class="exec-value">{top_title}</div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="exec-sub tabular" style="font-weight:700; color:var(--primary);">{top_score}</span>
                <div class="meter-bar" aria-hidden="true"><div class="meter-fill" style="width:{min(max(top_score_val, 0), 100)}%;"></div></div>
            </div>
        </div>
        <div class="exec-cell">
            <span class="exec-label">{icon_svg("layers")} Active Future Scenario</span>
            <div class="exec-value" style="font-size:var(--text-base);">{esc(scenario["name"])}</div>
            <span class="exec-sub">Uncertainty Band: {esc(scenario["uncertainty_level"])}</span>
        </div>
        <div class="exec-cell">
            <span class="exec-label">{icon_svg("book")} Primary Reskilling Horizon</span>
            <div class="exec-value">{pw_hours}</div>
            <span class="exec-sub">{gap_summary} · <a href="#step3-heading">View roadmap</a></span>
        </div>
    </div>
    """


def render_dashboard_html(state: dict) -> str:
    prof = state["active_profile"]
    is_employer_hr = state.get("view_mode") == "employer_hr"
    base_qs = f"profile_id={urllib.parse.quote(state['profile_id'])}&scenario_id={urllib.parse.quote(state['scenario_id'])}&signal_mode={urllib.parse.quote(state['signal_mode'])}"

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

    # Scenario buttons (inline badge header instead of stacked eyebrow kicker)
    scenario_links = []
    for sc_id, sc_info in SCENARIOS.items():
        is_active = "active-scenario" if state["scenario_id"] == sc_id else ""
        href = f"/?profile_id={urllib.parse.quote(state['profile_id'])}&scenario_id={urllib.parse.quote(sc_id)}&signal_mode={urllib.parse.quote(state['signal_mode'])}"
        scenario_links.append(
            f'<a href="{href}" class="scenario-tab {is_active}" data-testid="scenario-{esc(sc_id)}">'
            f'<div class="scenario-tab-header"><strong>{esc(sc_info["name"])}</strong><span class="tag tag-amber">{esc(sc_info["badge"])}</span></div>'
            f'<small>Sensitivity: {esc(sc_info["uncertainty_level"])}</small></a>'
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
            f'<a href="{href}" class="mode-btn {is_active}" data-testid="sigmode-{esc(m_id)}">{icon_svg("radio")} {esc(m_label)}</a>'
        )

    # Skill checkboxes for custom/interactive refinement
    skill_checkboxes = []
    for sk_id, sk_info in SKILLS_CATALOG.items():
        checked = "checked" if sk_id in profile_skills_set else ""
        skill_checkboxes.append(
            f'<label class="skill-check"><input type="checkbox" name="skills" value="{esc(sk_id)}" {checked} onchange="updateSkillCount()">'
            f'<span><strong>{esc(sk_info["name"])}</strong><small>{esc(sk_info["category"])}</small></span></label>'
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
            f'<td><div style="margin-bottom:4px;">{fb_tag}</div><strong>{esc(sig["title"])}</strong><div class="sig-summary">{esc(sig.get("summary", ""))}</div></td>'
            f'<td class="mono">Pub: {esc(sig["published_date"])}<br>Ret: {esc(sig["retrieved_date"])}</td>'
            f'<td><a href="{esc(sig["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(sig["source_name"])} {icon_svg("external")}</a></td>'
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
            <h3>{icon_svg("alert")} Insufficient Evidence — Honest Guardrail Triggered</h3>
            <p><strong>Reason Code:</strong> <code class="mono">{esc(ev["reason"])}</code></p>
            <p class="prose-measure">{esc(ev["message"])}</p>
            {f'<ul>{warnings_list}</ul>' if warnings_list else ''}
            <p class="small-note" style="margin-top:var(--space-2);">
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
                f'<td><strong>{esc(comp["scenario_name"])}</strong><div class="sig-summary">{esc(comp["assumptions"])}</div></td>'
                f'<td><span class="tag tag-amber">{esc(comp["uncertainty_level"])}</span></td>'
                f'<td class="tabular"><strong>#1 {esc(comp["top_role"])}</strong> ({esc(comp["top_role_score"])}/100)</td>'
                f'<td class="tabular">#2 {esc(comp["runner_up_role"])} ({esc(comp["runner_up_score"])}/100)</td>'
                f'</tr>'
            )
        scenario_matrix_html = f"""
        <section class="card" aria-labelledby="scenario-matrix-heading" data-testid="scenario-comparison-section">
            <div class="section-header">
                <h2 id="scenario-matrix-heading">{icon_svg("layers")} Multi-Scenario Uncertainty Comparison (Must-Have #6)</h2>
                <span class="tag tag-blue">Estimates, Not Single-Point Predictions</span>
            </div>
            <p class="section-sub">
                AI adoption speed and policy enforcement are uncertain. Compare how your top role rankings shift across three explicit future scenarios:
            </p>
            <div class="table-scroll">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Future Scenario &amp; Explicit Assumptions</th>
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
                "".join(f'<span class="tag tag-green">{icon_svg("check")} {esc(s["name"])}</span>' for s in role["matched_required_skills"])
                or '<span class="small-note">None matched yet</span>'
            )
            missing_req_html = (
                "".join(f'<span class="tag tag-gap">{icon_svg("plus")} {esc(s["name"])}</span>' for s in role["missing_required_skills"])
                or f'<span class="tag tag-green">{icon_svg("check")} All core required skills matched!</span>'
            )
            matched_sup_html = (
                "".join(f'<span class="tag tag-blue">{icon_svg("check")} {esc(s["name"])}</span>' for s in role["matched_supporting_skills"])
                or '<span class="small-note">None matched yet</span>'
            )
            missing_sup_html = (
                "".join(f'<span class="tag tag-muted">{icon_svg("plus")} {esc(s["name"])}</span>' for s in role["missing_supporting_skills"])
                or '<span class="small-note">None</span>'
            )

            sig_citations = []
            for cs in role["supporting_signals"]:
                mode_tag = "[Snapshot Fallback]" if cs.get("is_fallback") else "[Live Feed]"
                sig_citations.append(
                    f'<li><a href="{esc(cs["source_url"])}" target="_blank" rel="noopener noreferrer">{esc(cs["title"])} {icon_svg("external")}</a> '
                    f'<span class="mono">({esc(cs["source_name"])}, Published {esc(cs["published_date"])}, Retrieved {esc(cs["retrieved_date"])} {mode_tag})</span> '
                    f'— Matched: <em>{esc(", ".join(cs["matched_skills"]))}</em></li>'
                )
            sig_citations_html = (
                f'<ul class="citation-list">{"".join(sig_citations)}</ul>'
                if sig_citations
                else '<p class="small-note">Insufficient role-specific signals in current window (score penalized).</p>'
            )

            pathway_steps = []
            for st in role["pathway"]["steps"]:
                sdg_badges = "".join(f'<span class="tag tag-sdg">{esc(t)}</span>' for t in st["sdg_tags"])
                pathway_steps.append(
                    f'<div class="pathway-step">'
                    f'<div class="step-index-circle">{esc(st["step_number"])}</div>'
                    f'<div>'
                    f'<div class="pathway-step-header">'
                    f'<h4>{esc(st["skill_name"])}</h4>'
                    f'<div class="tag-wrap"><span class="tag tag-muted">Stage {esc(st["stage"])} · {esc(st["priority"])}</span>'
                    f'<span class="tag tag-green mono">{esc(st["estimated_hours"])} hrs (~{esc(st["estimated_weeks"])} wk)</span></div>'
                    f'</div>'
                    f'<p class="prose-measure" style="margin:4px 0;"><strong>Learning Objective:</strong> {esc(st["objective"])}</p>'
                    f'<p style="margin:4px 0;"><strong>Verified Resource:</strong> <a href="{esc(st["resource_url"])}" target="_blank" rel="noopener noreferrer">{esc(st["resource_title"])} {icon_svg("external")}</a> '
                    f'<span class="tag tag-green">{esc(st["cost_tier"])}</span></p>'
                    f'<div class="verify-note"><span>Provenance: {esc(st["verification_status"])}</span> {sdg_badges}</div>'
                    f'</div>'
                    f'</div>'
                )
            pathway_html = (
                f'<div class="pathway-list">{"".join(pathway_steps)}</div>'
                if pathway_steps
                else f'<p class="tag tag-green">{icon_svg("check")} Your profile already satisfies all required and supporting skills for this role.</p>'
            )

            sdg_cards = []
            for sl in role["sdg_links"]:
                sdg_cards.append(
                    f'<div class="sdg-item">'
                    f'<strong>{esc(sl["sdg"])} ({esc(sl["target"])})</strong>'
                    f'<p class="prose-measure">{esc(sl["explanation"])}</p>'
                    f'</div>'
                )

            # Progressive disclosure: Top 2 roles open by default; ranks 3-6 collapsible for clean scanning
            is_open_attr = "open" if int(role["rank"]) <= 2 else ""
            top_rank_class = "top-rank-role" if int(role["rank"]) == 1 else ""

            role_cards.append(
                f"""
                <article class="role-card {top_rank_class}" data-testid="role-card-{esc(role['rank'])}">
                    <details class="role-disclosure" {is_open_attr}>
                        <summary>
                            <div class="role-title-group">
                                <div class="role-badges-row">
                                    <span class="rank-badge">Rank #{esc(role["rank"])}</span>
                                    <span class="tag tag-blue">{esc(role["category"])}</span>
                                    <span class="tag tag-muted">{len(role["matched_required_skills"])}/{len(role["matched_required_skills"]) + len(role["missing_required_skills"])} Core Skills Matched</span>
                                    <span class="tag tag-green mono">{esc(role["pathway"]["total_estimated_hours"])} hrs pathway</span>
                                </div>
                                <h3>{esc(role["title"])}</h3>
                                <p class="role-summary">{esc(role["summary"])}</p>
                            </div>
                            <div class="role-score-cluster">
                                <div class="score-box">
                                    <div class="score-num" data-testid="role-score-{esc(role['rank'])}">{esc(role["total_score"])}<span>/100</span></div>
                                    <div class="score-label">Estimated Match</div>
                                </div>
                                {icon_svg("chevron")}
                            </div>
                        </summary>

                        <div class="role-body">
                            <div class="explain-box">
                                <strong>Why This Role Ranks #{esc(role["rank"])}:</strong> {esc(role["why_ranked_here"])}
                                <div class="formula-breakdown mono">
                                    <span>Formula ({esc(bd["formula"])})</span>
                                    <span>Readiness: <strong>{esc(bd["skill_readiness_score"])}%</strong></span>
                                    <span>Signal Coverage: <strong>{esc(bd["signal_momentum_score"])}%</strong></span>
                                    <span>Scenario Fit: <strong>{esc(bd["scenario_fit_score"])}%</strong></span>
                                </div>
                            </div>

                            <div class="grid-2">
                                <div class="structural-pane">
                                    <h4>{icon_svg("check")} Matched Profile Skills</h4>
                                    <div class="skill-group-label">Required Core Matched:</div>
                                    <div class="tag-wrap">{matched_req_html}</div>
                                    <div class="skill-group-label">Supporting Matched:</div>
                                    <div class="tag-wrap">{matched_sup_html}</div>
                                </div>
                                <div class="structural-pane">
                                    <h4>{icon_svg("plus")} Identified Skill Gaps (To Reskill)</h4>
                                    <div class="skill-group-label">Missing Required Skills:</div>
                                    <div class="tag-wrap">{missing_req_html}</div>
                                    <div class="skill-group-label">Missing Supporting Skills:</div>
                                    <div class="tag-wrap">{missing_sup_html}</div>
                                </div>
                            </div>

                            <div class="structural-pane" data-testid="pathway-section-{esc(role['rank'])}">
                                <div class="panel-title-row">
                                    <h4>{icon_svg("book")} Ordered Low-Cost / Free Reskilling Pathway (Must-Have #4)</h4>
                                    <span class="mono badge-time">Total Est: {esc(role["pathway"]["total_estimated_hours"])} hrs (~{esc(role["pathway"]["total_estimated_weeks"])} weeks)</span>
                                </div>
                                <p class="small-note">{esc(role["pathway"]["disclaimer"])}</p>
                                {pathway_html}
                            </div>

                            <div class="structural-pane">
                                <h4>{icon_svg("radio")} Dated Research Signals (Scholarly Publications) Mentioning This Role's Skills</h4>
                                {sig_citations_html}
                            </div>

                            <div class="grid-2">
                                <div class="structural-pane" data-testid="sdg-section-{esc(role['rank'])}">
                                    <h4>{icon_svg("globe")} UN SDG Alignment &amp; Contribution (Must-Have #5)</h4>
                                    <div class="sdg-list">{"".join(sdg_cards)}</div>
                                </div>
                                <div class="uncertainty-panel" data-testid="uncertainty-section-{esc(role['rank'])}">
                                    <h4>{icon_svg("shield")} Uncertainty, Limitations &amp; Human-in-Charge Notice</h4>
                                    <p class="prose-measure"><strong>Role Limitation:</strong> {esc(role["uncertainty_note"])}</p>
                                    <p class="prose-measure"><strong>Active Scenario Assumption ({esc(scenario["name"])}):</strong> {esc(scenario["assumptions"])}</p>
                                    <p class="prose-measure"><strong>Epistemic Boundary:</strong> Signals are dated scholarly AI publications (OpenAlex). They show research activity around a skill, NOT job postings, vacancy counts, hiring demand, or salaries in Malaysia. Final career decisions remain with the human learner.</p>
                                </div>
                            </div>
                        </div>
                    </details>
                </article>
                """
            )
        roles_section_html = f'<div class="roles-stack">{"".join(role_cards)}</div>'

    exec_summary_html = build_executive_summary_html(prof, ev, scenario, sig_payload, len(profile_skills_set))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Skills Compass — SDC Hackathon 2026 Domain 1 Prototype</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Fira+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>{DESIGN_SYSTEM_CSS}</style>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <header class="app-header">
        <div class="header-inner">
            <div class="brand-group">
                <div class="brand-mark">{icon_svg("compass")}</div>
                <div class="header-title">
                    <h1>AI Skills Compass</h1>
                    <p>SDC Hackathon 2026 · Domain 1 (The Aiversecity Future-Ready Workforce Domain)</p>
                </div>
            </div>
            <div class="header-badges">
                <span class="tag tag-blue">{icon_svg("globe")} SDG 4 (4.3, 4.4) &amp; SDG 8 (8.2, 8.5)</span>
                <span class="tag tag-green">{icon_svg("shield")} Human-in-Charge Advisory</span>
                <span class="tag tag-amber">Synthetic &amp; Public Data Only</span>
            </div>
        </div>
    </header>

    <nav class="workspace-nav-bar" aria-label="Workspace View and Section Navigation">
        <div class="workspace-nav-inner">
            <div class="view-tabs" data-testid="view-switcher">
                <a href="/?{base_qs}&view=individual" class="view-tab {"active-mode" if not is_employer_hr else ""}" data-testid="view-individual">{icon_svg("user")} Learner View (Individual Path)</a>
                <a href="/?{base_qs}&view=employer_hr" class="view-tab {"active-mode" if is_employer_hr else ""}" data-testid="view-hr">{icon_svg("building")} Employer / HR Workforce Cohort View</a>
            </div>
            <div class="step-jump-nav">
                <a href="#step1-heading" class="step-jump-link"><span class="step-num-pill">1</span> Profile Intake</a>
                <a href="#step2-heading" class="step-jump-link"><span class="step-num-pill">2</span> Future Scenarios</a>
                <a href="#step3-heading" class="step-jump-link"><span class="step-num-pill">3</span> Roles &amp; Pathways</a>
                <a href="#step4-heading" class="step-jump-link"><span class="step-num-pill">4</span> Signal Radar</a>
            </div>
        </div>
    </nav>

    <main id="main-content" class="container">
        <div class="status-strip">
            <div class="top-banner {banner_class}" role="status" data-testid="signal-status-banner">
                <div>
                    <strong>[{esc(badge_text)}]</strong> {esc(sig_payload.get("banner_label", ""))}
                </div>
                <div class="mono">Valid Signals: {len(sig_payload.get("signals", []))}</div>
            </div>

            <div class="synthetic-guardrail" data-testid="synthetic-data-notice">
                <span class="guardrail-icon">{icon_svg("shield")}</span>
                <div class="prose-measure" style="max-width:105ch;">
                    <strong>Data &amp; Privacy Guardrail (Domain 1 Rule §6):</strong> This prototype uses <strong>synthetic personas and public dated research-publication signals only</strong>. Do not enter real personal identifiers or upload real CVs. Every recommendation cites its dated signal source and never fabricates courses, job statistics, or hiring guarantees.
                </div>
            </div>
        </div>

        {exec_summary_html}

        {build_employer_hr_view_html(state['scenario_id'], state['signal_mode']) if is_employer_hr else ''}

        {top_guardrail_banner}

        <!-- STEP 1: PROFILE INTAKE -->
        <section class="card" aria-labelledby="step1-heading" data-testid="profile-intake-section">
            <div class="section-header">
                <h2 id="step1-heading">{icon_svg("user")} 1. Skills Profile Intake — "Tell Us About Yourself" (Must-Have #1)</h2>
                <span class="tag tag-blue">Active Profile: {esc(prof["name"])}</span>
            </div>
            <p class="section-sub">
                Select a pre-built synthetic Malaysian worker persona for instant evaluation, or enter custom skills and sample experience text below:
            </p>

            <div style="margin-bottom:var(--space-5);">
                <div class="skill-group-label" style="margin-bottom:var(--space-2);">Quick-Select Synthetic Malaysian Personas:</div>
                <div class="persona-grid">
                    {"".join(persona_links)}
                </div>
            </div>

            <!-- INTERACTIVE QUESTIONNAIRE & CV PASTE FORM -->
            <form method="GET" action="/" class="intake-form" data-testid="interactive-intake-form" onsubmit="const b=this.querySelector('[data-testid=apply-skills-btn]'); if(b){{b.textContent='Analyzing Profile & Matching Roles...'; b.style.opacity='0.85';}}">
                <input type="hidden" name="profile_id" value="custom">
                <input type="hidden" name="scenario_id" value="{esc(state['scenario_id'])}">
                <input type="hidden" name="signal_mode" value="{esc(state['signal_mode'])}">

                <div class="form-grid-3">
                    <div class="form-field">
                        <label for="input-custom-name">Your Name / Identifier (Synthetic Only)</label>
                        <input type="text" id="input-custom-name" name="custom_name" class="form-control" value="{esc(prof.get('name', 'Custom Learner'))}" placeholder="e.g. Farhan Tan / Fresh Grad">
                    </div>
                    <div class="form-field">
                        <label for="input-exp-level">Experience Level</label>
                        <select id="input-exp-level" name="experience_level" class="form-control">
                            <option value="entry" {"selected" if prof.get("experience_level") == "entry" else ""}>Fresh Graduate / Career Switcher (&lt; 2 yrs)</option>
                            <option value="mid" {"selected" if prof.get("experience_level") in ("mid", None) else ""}>Mid-Level Practitioner (2–6 yrs)</option>
                            <option value="senior" {"selected" if prof.get("experience_level") == "senior" else ""}>Senior Specialist / Lead (&gt; 6 yrs)</option>
                        </select>
                    </div>
                    <div class="form-field">
                        <label for="input-interest-track">Career Interest Track</label>
                        <select id="input-interest-track" name="target_interest" class="form-control">
                            <option value="">Explore All Emerging AI Tracks</option>
                            <option value="operations" {"selected" if prof.get("target_interest") == "operations" else ""}>Operations &amp; Process Optimization</option>
                            <option value="quality assurance" {"selected" if prof.get("target_interest") == "quality assurance" else ""}>Quality Assurance &amp; LLM Evaluation</option>
                            <option value="governance" {"selected" if prof.get("target_interest") == "governance" else ""}>AI Ethics, PDPA &amp; Governance</option>
                            <option value="engineering" {"selected" if prof.get("target_interest") == "engineering" else ""}>RAG &amp; Knowledge Engineering</option>
                            <option value="sustainability" {"selected" if prof.get("target_interest") == "sustainability" else ""}>Green Tech &amp; ESG Analytics</option>
                        </select>
                    </div>
                </div>

                <div class="form-field" style="margin-bottom:var(--space-4);">
                    <label for="cv-bio-textarea">Paste Sample CV / Experience Bio / Skill Summary (Domain 1 Item #1)</label>
                    <textarea name="cv_bio_text" id="cv-bio-textarea" rows="3" class="form-control" placeholder="Paste your background, e.g.: 'Operations analyst with 3 years experience. Skilled in workflow automation, process mapping, and basic SQL data analysis. Interested in prompt engineering and human-in-the-loop quality evaluation.'">{esc(prof.get("cv_bio_text", ""))}</textarea>
                    <div class="file-upload-bar">
                        <span>{icon_svg("upload")} <strong>Load sample text file</strong> (.txt, .md, .csv — processed locally in browser):</span>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <input type="file" id="cv-file-picker" accept=".txt,.md,.json,.csv" style="font-size:var(--text-xs);" onchange="
                                const file = this.files[0];
                                if (file) {{
                                    const reader = new FileReader();
                                    reader.onload = function(e) {{
                                        document.getElementById('cv-bio-textarea').value = e.target.result;
                                        const st = document.getElementById('file-upload-status');
                                        if (st) {{ st.textContent = 'Loaded: ' + file.name + ' (' + e.target.result.length + ' chars)'; st.style.display = 'inline-flex'; }}
                                    }};
                                    reader.readAsText(file);
                                }}
                            ">
                            <span id="file-upload-status" class="tag tag-green" style="display:none;"></span>
                        </div>
                    </div>
                    <small class="form-helper">
                        Whole-word regex parser automatically detects and matches your skills against the 16 reviewed taxonomy competencies without sending text to any third-party server.
                    </small>
                </div>

                <details class="skill-drawer">
                    <summary>
                        Fine-Tune Skill Checkboxes Manually (<span id="selected-skill-counter" class="tabular">{len(profile_skills_set)}</span> of {len(SKILLS_CATALOG)} selected)
                    </summary>
                    <div class="skills-grid">
                        {"".join(skill_checkboxes)}
                    </div>
                </details>

                <div class="form-actions-row">
                    <button type="submit" class="btn-primary" data-testid="apply-skills-btn">
                        {icon_svg("search")} Analyze Profile &amp; Match Future Roles
                    </button>
                    <span class="small-note">Deterministic calculation · Zero external LLM latency</span>
                </div>
            </form>

            <div class="profile-summary-bar">
                <div><strong>Current Active Background:</strong> {esc(prof["current_role"])} <span class="tag tag-muted">{esc(prof["persona_type"])}</span></div>
                <div><strong>Detected Skills ({len(profile_skills_set)}):</strong> {", ".join([SKILLS_CATALOG[s]["name"] for s in prof.get("skills", []) if s in SKILLS_CATALOG]) or '<span class="tag tag-gap">None detected (Guardrail active)</span>'}</div>
            </div>
        </section>

        <!-- STEP 2: SCENARIO SELECTOR -->
        <section class="card" aria-labelledby="step2-heading" data-testid="scenario-selector-section">
            <div class="section-header">
                <h2 id="step2-heading">{icon_svg("layers")} 2. Future Scenario Selection — Handling Uncertainty (Must-Have #6)</h2>
                <span class="tag tag-amber">Sensitivity: {esc(scenario["uncertainty_level"])}</span>
            </div>
            <p class="section-sub">Switch scenarios to observe how different AI disruption speeds and sustainability mandates shift role rankings:</p>
            <div class="scenario-grid">
                {"".join(scenario_links)}
            </div>
            <div class="explain-box">
                <strong>Active Scenario Assumptions ({esc(scenario["name"])}):</strong> {esc(scenario["assumptions"])}
            </div>
        </section>

        {scenario_matrix_html}

        <!-- STEP 3: EXPLAINABLE ROLE MATCHING, PATHWAYS & SDG MAP -->
        <section class="card" aria-labelledby="step3-heading" data-testid="ranked-roles-section">
            <div class="section-header">
                <h2 id="step3-heading">{icon_svg("compass")} 3. Explainable Future-Role Rankings, Skill Gaps, Pathways &amp; SDG Links (Must-Haves #3, #4, #5)</h2>
                <div style="display:flex; align-items:center; gap:var(--space-2);">
                    <span class="tag tag-green">Deterministic &amp; Inspectable Scoring</span>
                    <button type="button" class="btn-secondary" onclick="toggleAllRoles(this)">Expand All 6 Roles</button>
                </div>
            </div>
            <p class="section-sub">
                Each role is scored transparently using <code class="mono">0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit</code>.
                Top 2 matches are expanded by default; click any role header below to inspect its full pathway and SDG mapping.
            </p>
            {roles_section_html}
        </section>

        <!-- STEP 4: DATED AI RESEARCH SIGNAL LAYER -->
        <section class="card" aria-labelledby="step4-heading" data-testid="signals-radar-section">
            <div class="section-header">
                <h2 id="step4-heading">{icon_svg("radio")} 4. Future Skills Radar — Dated AI Research Signal Layer (Must-Have #2)</h2>
                <span class="tag tag-muted mono">Source Mode: {esc(sig_payload["source_mode"])}</span>
            </div>
            <p class="section-sub">
                Toggle between the dated OpenAlex snapshot, a live OpenAlex fetch (arXiv as backup), or the malformed-signal guardrail test. These are research publications, not job-market or vacancy data:
            </p>
            <div class="mode-bar">
                {"".join(sig_mode_links)}
            </div>

            {build_rising_declining_radar_html()}
            <div class="table-scroll">
                <table class="data-table" data-testid="signals-table">
                    <thead>
                        <tr>
                            <th>Signal Title &amp; Summary</th>
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
        <p class="prose-measure" style="margin:0 auto;">
            <strong>AI Skills Compass</strong> · Built for SDC Hackathon 2026 (Domain 1: Aiversecity Future-Ready Workforce) ·
            Context figures quoted from the SDC 2026 Domain 1 brief (not independently re-verified by this team): Hays Asia Salary Guide 2025 (56% use AI at work vs 26% formally trained, Malaysia) &amp; MOSTI (600,000+ workers needing reskilling) ·
            Licensed under Apache License 2.0.
        </p>
    </footer>

    <script>
        function updateSkillCount() {{
            const checked = document.querySelectorAll('input[name="skills"]:checked').length;
            const el = document.getElementById('selected-skill-counter');
            if (el) el.textContent = checked;
        }}
        function toggleAllRoles(btn) {{
            const disclosures = document.querySelectorAll('.role-disclosure');
            const anyClosed = Array.from(disclosures).some(d => !d.open);
            disclosures.forEach((d, idx) => {{
                d.open = anyClosed ? true : (idx < 2);
            }});
            btn.textContent = anyClosed ? 'Collapse Roles #3–#6' : 'Expand All 6 Roles';
        }}
    </script>
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
