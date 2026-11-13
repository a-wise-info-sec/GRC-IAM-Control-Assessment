"""Reconcile synthetic termination evidence. Standard library only.

This is a decision-support exercise, not a certified control testing engine.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUTPUTS = ROOT / "outputs"
DEADLINE_HOURS = 24  # Harborline's *fictional* policy, not a NIST deadline


def read_csv(name: str) -> list[dict[str, str]]:
    with (EVIDENCE / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError(f"Expected UTC ISO timestamp: {value}")
    return parsed.astimezone(timezone.utc)


def index_unique(rows: list[dict[str, str]], field: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if not key or key in result:
            raise ValueError(f"Missing/duplicate {field} in {label}: {key!r}")
        result[key] = row
    return result


def classify(terminated: datetime, disabled: datetime | None, status: str) -> tuple[str, str]:
    """Classify account using supplied event and snapshot evidence.

    Deliberately do not interpret absent logs as evidence of timeliness.
    """
    status = status.strip().upper()
    if status not in {"ACTIVE", "DISABLED"}:
        return "REVIEW_REQUIRED", "Unrecognized or missing snapshot status"
    if disabled is None:
        if status == "ACTIVE":
            return "ACTIVE", "No disable event; account active at snapshot"
        return "INSUFFICIENT_EVIDENCE", "Account disabled at snapshot; no disable timestamp"
    if disabled < terminated:
        return "REVIEW_REQUIRED", "Disable event precedes HR termination; validate effective timing"
    if status == "ACTIVE":
        return "CONFLICTING_EVIDENCE", "Disable event exists, but snapshot shows active"
    hours = (disabled - terminated).total_seconds() / 3600
    if hours > DEADLINE_HOURS:
        return "LATE", f"Disable event {hours:.2f} hours after departure"
    return "PASS", f"Disable event {hours:.2f} hours after departure"


def assess() -> list[dict[str, str]]:
    hr = index_unique(read_csv("hr_terminations.csv"), "employee_id", "HR termination roster")
    inventory = read_csv("account_inventory.csv")
    events = index_unique(read_csv("disable_events.csv"), "account_id", "disable events")
    snapshots = index_unique(read_csv("account_state_snapshot.csv"), "account_id", "snapshot")
    _ = index_unique(inventory, "account_id", "account inventory")
    if not inventory:
        raise ValueError("No accounts in population")
    results = []
    for account in sorted(inventory, key=lambda r: r["account_id"]):
        employee_id = account["employee_id"]
        account_id = account["account_id"]
        if employee_id not in hr:
            raise ValueError(f"Account not linked to termination roster: {account_id}")
        if account_id not in snapshots:
            raise ValueError(f"Account missing snapshot: {account_id}")
        terminated = parse_utc(hr[employee_id]["terminated_at_utc"])
        event = events.get(account_id)
        disabled = parse_utc(event["disabled_at_utc"]) if event else None
        snapshot = snapshots[account_id]
        snapshot_at = parse_utc(snapshot["snapshot_at_utc"])
        if snapshot_at < terminated:
            raise ValueError(f"Snapshot predates termination: {account_id}")
        status = snapshot["status"]
        result, rationale = classify(terminated, disabled, status)
        elapsed = f"{(disabled - terminated).total_seconds() / 3600:.2f}" if disabled else ""
        results.append({
            "employee_id": employee_id,
            "account_id": account_id,
            "platform": account["platform"],
            "privileged": account["privileged"],
            "terminated_at_utc": hr[employee_id]["terminated_at_utc"],
            "disabled_at_utc": event["disabled_at_utc"] if event else "",
            "hours_elapsed": elapsed,
            "snapshot_status": status,
            "result": result,
            "rationale": rationale,
            "change_ticket_id": event["change_ticket_id"] if event else "",
        })
    # Warn only by rejecting unlinked events and snapshots, not silently discarding them.
    inventory_ids = {a["account_id"] for a in inventory}
    extra_events = sorted(set(events) - inventory_ids)
    extra_snapshots = sorted(set(snapshots) - inventory_ids)
    if extra_events or extra_snapshots:
        raise ValueError(f"Unreconciled source records: events={extra_events}, snapshots={extra_snapshots}")
    return results


def main() -> None:
    results = assess()
    OUTPUTS.mkdir(exist_ok=True)
    file = OUTPUTS / "test_results.csv"
    with file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    counts = Counter(r["result"] for r in results)
    summary = {
        "scenario": "Harborline Services — synthetic October 2026 terminations",
        "policy_deadline_hours": DEADLINE_HOURS,
        "employee_count": len({r["employee_id"] for r in results}),
        "account_count": len(results),
        "counts": {name: counts[name] for name in [
            "PASS", "LATE", "ACTIVE", "INSUFFICIENT_EVIDENCE", "CONFLICTING_EVIDENCE", "REVIEW_REQUIRED"
        ]},
        "assessment_conclusion": "NOT_EFFECTIVE_FOR_TESTED_SCOPE" if any(
            r["result"] in ("LATE", "ACTIVE", "CONFLICTING_EVIDENCE") for r in results
        ) else "FURTHER_REVIEW_REQUIRED",
        "limitation": "Provided population and event logs have not been independently validated for completeness.",
    }
    (OUTPUTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {file.relative_to(ROOT)} and outputs/summary.json")
    print(json.dumps(summary["counts"], indent=2))


if __name__ == "__main__":
    main()
