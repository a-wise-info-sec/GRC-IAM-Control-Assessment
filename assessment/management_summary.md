# Management summary — fictional IAM termination assessment

**Overall:** The access termination control did **not** operate as required across the **supplied October 2026 test population**. Of 12 mapped accounts, eight had evidence of timely disablement, two CRM accounts were disabled after the 24-hour policy deadline, one CRM account remained active at the November 5 snapshot, and one Directory account lacked sufficient timestamp evidence to determine timeliness.

**Priority action:** Verify and restrict the still-active CRM account promptly. The inventory flags this account as privileged; that classification and any actual post-termination activity require independent confirmation.

**Systemic improvement:** Reconcile HR terminations to account inventories for each in-scope platform; standardize ownership, ticket handoffs, timing checkpoints and escalation for overdue CRM disablements.

**Evidence quality:** Recover the missing disablement log or ticket for the Directory account. A disabled status at a later snapshot is not proof that the account was disabled within the required timeframe.

**Assurance limitation:** This is a synthetic exercise. Source completeness, log integrity, other SaaS platforms and remediation have not been validated. Findings and preliminary severity are illustrative, not a formal audit opinion.

**Recommended decision:** Treat confirmed failures as control deficiencies within this defined scope; assign owners and dates, document evidence requests, and schedule a retest after corrective actions.
