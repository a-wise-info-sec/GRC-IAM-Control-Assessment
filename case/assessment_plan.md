# Control assessment plan

| Field | Defined approach |
|---|---|
| Assessment ID | HL-AC2-2026-10 |
| Control owner | Fictional Identity Operations |
| Control tested | Termination-related account disablement and supporting evidence retention |
| NIST mapping | AC-2 Account Management (related control context) |
| Design criterion | Policy HL-IAM-04 specifies in-scope accounts, a 24-hour deadline and record retention |
| Operating period | October 2026 departures |
| Population | Eight terminated employees and twelve mapped Directory / CRM accounts |
| Test type | Full supplied-population reconciliation; quantitative timing check and documentary review |
| Methods | Examine HR, identity inventory, event and status exports; test timestamps; interview owners if evidence is missing (simulated follow-up only) |

## Procedure

1. Obtain HR departure extract. Validate period, effective timestamps and unique employee identifiers.
2. Obtain an independently sourced account inventory, reconcile identifiers, confirm both platforms are in scope and assess completeness.
3. Obtain disablement-event export and account-state snapshot. Confirm system clocks, timezone, time windows and extract origin.
4. For every expected account, calculate `disabled_at - termination_at` in elapsed hours.
5. Classify the results using the rules below. Document unsupported conclusions.
6. Investigate exceptions, request tickets/logs, assess root causes and compensating controls, and report findings.
7. Obtain remediation evidence and retest.

## Evaluation rules

| Result | Evidence condition |
|---|---|
| `PASS` | Disable timestamp within 24 hours of termination and snapshot status disabled |
| `LATE` | Disable timestamp more than 24 hours after termination, snapshot disabled |
| `ACTIVE` | No disable timestamp and snapshot active |
| `INSUFFICIENT_EVIDENCE` | Snapshot disabled but no disable timestamp available |
| `CONFLICTING_EVIDENCE` | Disable event exists but snapshot still active |
| `REVIEW_REQUIRED` | Inconsistent/malformed record, pre-termination disablement, or other unexpected state |

**Important:** `LATE` is not inferred from a missing event. A snapshot showing `disabled` does not demonstrate 24-hour timeliness. No synthetic documented exception waivers or compensating controls are provided for this controlled dataset.

## Conclusion rubric

- **Operating effectively for assessed population:** All account records passed, with adequate evidence and validated population completeness.
- **Not operating effectively for assessed population:** Confirmed late disablement or active post-termination account(s) identified.
- **Undetermined:** Reliable evidence cannot establish the outcomes or material population gaps remain.
