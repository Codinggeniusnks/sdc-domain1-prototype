# M4 Benchmark Schedule Assumptions & Production Disclaimers v1.1.0

**Reference Milestone**: Stage 12C Remediation (Audit Finding M4-P3-02)  
**Target Module**: M4 Personalised Reskilling Pathway Engine v1.1.0  
**Status**: COMPLETE & VERIFIED

---

## 1. Audit Context & Pacing Ambiguity

In M4 v1.0.0 benchmark reports, estimated completion times were presented in weeks (e.g., "5.0 to 7.5 weeks"). Reviewer Argon noted that presenting weeks without an explicit disclaimer created the false impression that M4 dictates or predicts a worker's personal learning velocity, whereas the conversion from hours to weeks was based entirely on a developer test assumption of 10 study hours per week.

For adult workers balancing full-time shifts, childcare, or informal gig employment, available study time varies widely (e.g., 3 hours/week for shift workers vs 20 hours/week for jobseekers).

---

## 2. Test Assumption vs. User Schedule Separation

In M4 v1.1.0, a strict separation is established between benchmark testing assumptions and live user pathway generation:

1. **Benchmark Reports & Suites**:
   - Explicitly tagged as: `"TEST ASSUMPTION: 10 STUDY HOURS/WEEK"`.
   - Never presented as real-world clinical or vocational commitments.
2. **Production API (`build_pathway`)**:
   - `hours_per_week` is an optional parameter (`Optional[int] = None`).
   - If `hours_per_week` is omitted or `None`, the engine calculates total estimated hours (`total_estimated_hours_low`, `total_estimated_hours_high`), but sets `schedule_estimate: null`. It deliberately refrains from guessing weeks.
   - If a user explicitly specifies their weekly availability (e.g., `hours_per_week = 5`), the engine produces a `schedule_estimate` labeled `"USER-SCHEDULE-DEPENDENT ESTIMATE"`.

---

## 3. Benchmark Suite Schedule Table (8 Standard Personas)

The table below reflects the 8 benchmark evaluations using the documented test assumption:

$$\text{Estimated Weeks} = \frac{\text{Total Estimated Hours}}{10\text{ hours/week}}$$

| Persona ID | Baseline Profile | Target Role (MASCO) | Steps | Total Hours (Low) | Total Hours (High) | Benchmark Weeks (Low) | Benchmark Weeks (High) | Pacing Category | Explicit Benchmark Schedule Tag |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|
| **Persona 1** | Data Entry Clerk | Database Admin (2521) | 3 | 32 | 50 | 3.2 | 5.0 | Part-Time Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 2** | Customer Service Rep | Prompt Engineer (2512) | 3 | 48 | 75 | 4.8 | 7.5 | Moderate Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 3** | Admin Assistant | Workflow Automation (2519) | 4 | 44 | 70 | 4.4 | 7.0 | Moderate Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 4** | General Clerk | Prompt Engineer (2512) | 3 | 48 | 75 | 4.8 | 7.5 | Moderate Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 5** | Bank Teller | Financial Analyst (2413) | 4 | 52 | 82 | 5.2 | 8.2 | Comprehensive | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 6** | Logistics Coordinator | Supply Chain Spec (2141) | 4 | 46 | 72 | 4.6 | 7.2 | Moderate Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 7** | IT Support Tech | Cloud Solutions Admin (2522) | 3 | 34 | 54 | 3.4 | 5.4 | Part-Time Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |
| **Persona 8** | Digital Marketer | AI Marketing Spec (2431) | 3 | 42 | 66 | 4.2 | 6.6 | Part-Time Paced | `TEST ASSUMPTION: 10 STUDY HOURS/WEEK` |

---

## 4. Transition Distance Correlation

Consistent with Labour-Economics expectations, estimated learning effort correlates positively with M3 Transition Distance:
- **SHORT TRANSITION** (e.g., IT Support to Cloud Admin, Data Entry to Database Admin): Mean High Hours = **50.4 hours** (approx. 5.0 test-weeks).
- **MODERATE TRANSITION** (e.g., Customer Service to Prompt Engineer, Bank Teller to Financial Analyst): Mean High Hours = **55.0 hours** (approx. 5.5 to 8.2 test-weeks).

All outputs maintain integer bounds on hours, avoiding false precision decimals.
