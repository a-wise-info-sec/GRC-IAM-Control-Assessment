# Working paper: HL-AC2-2026-10

**Client:** Harborline Services (**fictional**)  
**Period:** October 2026  
**Control:** HL-IAM-04 — disable each in-scope employee account within 24 elapsed hours of HR's effective termination timestamp  
**NIST context:** AC-2 (Account Management)  
**Assessor:** Independent simulated case study; no real audit engagement

## 1. Objective and population

Determine whether the in-scope Directory and CRM account termination control operated as required for departures during the period, and whether available records support the conclusion. Eight HR termination records map to twelve system accounts. All twelve provided records were tested. **Completeness of the source population was not independently established.**

## 2. Procedure and evidence

Reconcile `hr_terminations.csv` to `account_inventory.csv`, then join `disable_events.csv` and `account_state_snapshot.csv` by account ID. Calculate elapsed hours in UTC and compare to the fictional 24-hour requirement. A disabled snapshot is insufficient to establish timing without an event timestamp. The script provides repeatable arithmetic; a real assessor would verify data provenance and obtain supporting tickets/logs.

## 3. Test results

| Classification | Count | Account(s) |
|---|---:|---|
| Pass | 8 | A101-DIR, A101-CRM, A102-DIR, A103-DIR, A104-DIR, A105-DIR, A107-DIR, A108-DIR |
| Late | 2 | A102-CRM (42 hours), A104-CRM (25 hours) |
| Active | 1 | A103-CRM (privileged according to inventory) |
| Insufficient evidence | 1 | A106-DIR (disabled at snapshot; no disabling event) |
| **Total** | **12** | |

**Evidence-supported on-time results:** 8 of 12 account records. Do **not** describe this ratio as a statistically representative enterprise compliance rate. It measures the supplied records only and includes one inconclusive record.

## 4. Findings

### HL-F01 — Terminated employee CRM account remains active

- **Observed condition:** `EMP-103` terminated on 2026-10-07 at 10:15 UTC; `A103-CRM` had no disable event in the supplied extract and remained `ACTIVE` in the November 5 snapshot.
- **Inventory context:** Account marked `privileged=Yes`, which increases potential exposure; **validate privilege with the CRM control owner** before final rating.
- **Criterion:** HL-IAM-04 requires disablement within 24 hours.
- **Risk:** A former worker's account could permit access to customer or business records; privileged status may increase impact.
- **Preliminary severity:** High, subject to validation of actual access, privilege and compensating controls.
- **Immediate next step:** Escalate for prompt access restriction; obtain verified current account state and activity logs; determine root cause and other affected terminations.

### HL-F02 — Two CRM accounts disabled after policy deadline

- **Observed condition:** `A102-CRM` disabled 42 hours after departure; `A104-CRM` disabled 25 hours after departure.
- **Criterion:** No later than 24 elapsed hours after HR's effective departure timestamp.
- **Risk:** Residual access beyond policy deadline, indicating unreliable offboarding handoffs or platform-specific procedures.
- **Preliminary severity:** Medium, pending evidence of actual activity and organizational risk method.
- **Next step:** Reconcile HR notifications to CRM disable tickets; inspect queue timing, escalation and automated provisioning dependencies; validate remediation in subsequent departures.

### HL-O01 — Missing disablement event / evidence gap

- **Observed condition:** `A106-DIR` was `DISABLED` at November 5 snapshot, but no disable timestamp was present in supplied log.
- **Assessment:** **Inconclusive**, not a confirmed late disablement. We cannot establish whether the 24-hour requirement was satisfied.
- **Next step:** Obtain a corroborating immutable event record or ticket history and determine whether the log export was complete.

## 5. Operating effectiveness conclusion

**Not effective for the tested population and period**, based on two evidenced late disabling events and one account still active at the assessment snapshot. The missing disable event is separately an **evidence sufficiency issue**; it is not used as proof of an additional failure.

This conclusion is limited to the two named platforms and the supplied inventory, subject to verification of evidence integrity and population completeness. No claim is made about all accounts, every system, the organization overall, or a certified audit opinion.

## 6. Work not completed / follow-up

- Validate source-system coverage, HR roster completeness, and snapshot/event export generation.
- Request supporting identity platform logs, ticket approvals and role ownership for exceptions.
- Check login activity after departure, reset sessions, and review token/API access as appropriate.
- Determine root cause and risk ratings under an approved organizational methodology.
- Obtain remediation proof and retest future departures. **No remediation verification is claimed in this simulation.**
