# Fictional organization, scope, and control criteria

## Business context

**Harborline Services** is an invented mid-sized services organization. Employees use an internal directory ("Directory") and a CRM platform ("CRM") to access business information. Eight staff departures occurred during October 2026. This engagement is designed to test one termination-related IAM control.

## System and time scope

- **Assessment period:** 2026-10-01 through 2026-10-31, inclusive, based on termination timestamp.
- **Population provided:** Eight employee departures with twelve mapped accounts in Directory and CRM.
- **Snapshot:** 2026-11-05 12:00 UTC; all account status entries refer to that moment.
- **Times:** All timestamps are in **UTC** to avoid daylight-saving ambiguity.
- **Exclusions:** Other SaaS services, service accounts, contractors, accounts without a known employee ID, privileged-access recertification, onboarding and access approval testing.

## Policy excerpt (control owner: Identity Operations)

> **HL-IAM-04 — Access Termination:** All in-scope employee accounts must be disabled no later than 24 elapsed hours after the employee's effective termination timestamp provided by HR. Identity Operations must retain reliable, timestamped evidence demonstrating when disablement occurred.

## Assumed source extracts

| Evidence | Intended purpose | Main limitation |
|---|---|---|
| `hr_terminations.csv` | HR-authoritative list and effective departure times | HR completeness has not been independently demonstrated |
| `account_inventory.csv` | Employee-to-account mapping for two systems | Could omit shadow accounts or other systems |
| `disable_events.csv` | Recorded disable timestamps and change IDs | Some event records are missing; extract completeness not verified |
| `account_state_snapshot.csv` | Current active/disabled status at fixed snapshot | Cannot establish when a disabled account was disabled |

## Assessor questions

1. Are the eight HR terminations the complete relevant population?
2. Does each terminated person have all their in-scope accounts represented?
3. Is a reliable disable event available and within 24 hours?
4. Are any accounts still active at the snapshot?
5. Can observed failures be distinguished from documentation gaps?
6. What remediation and additional evidence would support retesting?
