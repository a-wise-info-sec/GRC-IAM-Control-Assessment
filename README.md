# IAM Control Effectiveness Assessment | Simulated GRC Case

**Independent portfolio project · November 2026 · Synthetic evidence only**

> **Case question:** A fictional organization requires access to be disabled within 24 hours of an employee's departure. Does the available evidence support that the termination control operated effectively during October 2026?

This is a **completed example of a focused GRC control assessment**, not a claim that any real employer was assessed. It demonstrates how to define a control objective, reconcile evidence populations, test execution, distinguish confirmed failures from missing evidence, document findings, and recommend remediation.

## Results at a glance

| Result | Account records | Meaning |
|---|---:|---|
| PASS | 8 | Timely disable event, account disabled at snapshot |
| LATE | 2 | Recorded disable event occurred after 24-hour deadline |
| ACTIVE | 1 | Account still active at the snapshot; no disable event |
| INSUFFICIENT_EVIDENCE | 1 | Account was disabled at snapshot, but no disable event was provided |
| **Total** | **12** | Eight employee terminations, two platforms |

**Assessment conclusion:** The fictional termination control was **not operating effectively for the tested scope and period**. The conclusion is based on observed exceptions, not on the missing-evidence item alone. The incomplete audit trail is reported separately.

## How to explore it

1. Read [`case/organization_and_scope.md`](case/organization_and_scope.md) to learn the business context and the fictional 24-hour requirement.
2. Read [`case/assessment_plan.md`](case/assessment_plan.md) for objectives, evidence, test logic and limitations.
3. Inspect the four files under [`evidence/`](evidence/). They are deliberately imperfect.
4. Reproduce the test using only Python's standard library:

   ```bash
   python src/check_terminations.py
   python -m unittest discover -s tests -v
   ```

5. Compare [`outputs/test_results.csv`](outputs/test_results.csv) and [`outputs/summary.json`](outputs/summary.json) with the narrative [`assessment/working_paper.md`](assessment/working_paper.md).
6. Read the [`assessment/management_summary.md`](assessment/management_summary.md) and [`assessment/remediation_plan.csv`](assessment/remediation_plan.csv).

## Repository guide

```text
case/           Scope, business context, policy excerpt, test plan
 evidence/      Fictional HR, account inventory, event and state extracts
src/            Reproducible account-disable timing check
outputs/        Generated, versioned test results for transparent review
tests/          Unit tests for edge cases
assessment/     Working paper, findings, recommendation, action tracking
```

## Framework relationship

- **NIST SP 800-53 AC-2 (Account Management):** Relevant to lifecycle management and timely account disabling. **NIST does not prescribe this project's 24-hour threshold**; that is a fictional organization-defined policy requirement.
- **NIST SP 800-53A Rev. 5:** Used as general inspiration for evidence-based **examine / test / interview** assessment methods. This is a small educational exercise, **not** an authorized NIST assessment, audit certification, or exhaustive test of AC-2.
- **AC-6 (Least Privilege):** A possible future extension, not an assessed control in this repository.

NIST sources:
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

## Scope and important caveats

- The evidence is fully fabricated. No customer, employee, employer or production records are used.
- The account inventory is assumed to cover two in-scope platforms. There is **no independent proof** of organization-wide account completeness, and no claim of enterprise-wide compliance.
- The script is a **reconciliation aid**, not a substitute for verifying extract completeness, record authenticity, ticket approvals, exceptions, system logs or compensating controls.
- A disabled snapshot **without** a reliable disable event is treated as an evidence gap—not automatically an untimely disable.
- Severity labels in the simulated findings are **illustrative**, pending a real organization's risk-rating method and further investigation.
- This assessment uses an **entire provided population**, not a statistical sample. The population's completeness must be validated before reliance.

## Why this project exists

Just an independent project to show how a documented requirement is connected to actual evidence and how an assessor reaches a defensible conclusion when records are late, missing, or contradictory.
