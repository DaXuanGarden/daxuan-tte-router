#!/usr/bin/env python3
"""Create and maintain a resumable, evidence-gated TTE research run."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from route_tte import route  # type: ignore # noqa: E402
    from skill_registry import resolve_many  # type: ignore # noqa: E402
else:
    from .route_tte import route  # noqa: E402
    from .skill_registry import resolve_many  # noqa: E402


PHASES = (
    "intake",
    "literature",
    "gap_audit",
    "question_refinement",
    "data_support",
    "tte_protocol",
    "pilot",
    "execution",
    "diagnostics",
    "report",
    "feedback",
)
PILOT_DECISIONS = {"proceed", "downgrade", "stop"}
FEEDBACK_CLASSES = {
    "data_failure",
    "design_failure",
    "assumption_violation",
    "null_result",
    "positive_result",
    "pilot_failure",
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _state_path(workdir: Path) -> Path:
    return workdir / "research-state.json"


def _load_state(workdir: Path) -> dict[str, Any]:
    path = _state_path(workdir)
    if not path.is_file():
        raise SystemExit(f"No research-state.json found in {workdir}")
    return _read_json(path)


def _save_state(workdir: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = _now()
    _write_json(_state_path(workdir), state)


def _initial_phase_state() -> dict[str, dict[str, Any]]:
    phases: dict[str, dict[str, Any]] = {}
    for index, name in enumerate(PHASES):
        phases[name] = {
            "status": "ready" if index == 0 else "queued",
            "artifact": None,
            "started_at": None,
            "completed_at": None,
            "notes": [],
        }
    return phases


def _next_action(route_card: dict[str, Any]) -> str:
    if route_card["intent"] == "question_discovery":
        return "Run the evidence tasks, record verified sources, and complete the gap audit before freezing a TTE protocol."
    if route_card["selected"]:
        return f"Read and resolve {route_card['selected'][0]} before advancing to {route_card['next_handoff'] or 'the final report'}."
    return "Clarify the clinical decision, population, treatment contrast, outcome, and horizon."


def _write_templates(workdir: Path, route_card: dict[str, Any]) -> None:
    (workdir / "handoffs").mkdir(exist_ok=True)
    _write_json(workdir / "route-card.json", route_card)
    _write_json(
        workdir / "evidence-map.json",
        {
            "status": "not_started",
            "question": route_card["unmatched"],
            "searches": [],
            "sources": [],
            "direct_examples": [],
            "methods_examples": [],
            "boundary_examples": [],
            "novelty_status": "unverified",
        },
    )
    _write_json(workdir / "design-card.json", route_card["design_card"])
    (workdir / "research-log.md").write_text(
        "# Research log\n\n"
        "This run is a staged record. Each phase must record its artifact and gate decision before the next phase.\n\n"
        f"- Created: {_now()}\n"
        f"- Intent: `{route_card['intent']}`\n"
        f"- Stage: `{route_card['stage']}`\n"
        "- Literature retrieval: not run by the deterministic router\n"
        "- Clinical data analysis: not run\n",
        encoding="utf-8",
    )
    (workdir / "pilot-report.md").write_text(
        "# Pilot report\n\n"
        "Record cohort count, treatment observability, endpoint incidence, time-zero coverage, follow-up, and overlap before a full estimate.\n\n"
        "Decision: pending (`proceed`, `downgrade`, or `stop`).\n",
        encoding="utf-8",
    )
    (workdir / "feedback.md").write_text(
        "# Research feedback\n\n"
        "Record one classification after each pilot or analysis: data_failure, design_failure, assumption_violation, null_result, positive_result, or pilot_failure.\n",
        encoding="utf-8",
    )
    (workdir / "handoffs" / "00-intake.md").write_text(
        "# Intake handoff\n\n"
        f"- Research request: {route_card['unmatched']}\n"
        f"- Current intent: `{route_card['intent']}`\n"
        f"- Current stage: `{route_card['stage']}`\n"
        f"- Next action: {_next_action(route_card)}\n"
        "- Evidence and estimates are intentionally unexecuted at intake.\n",
        encoding="utf-8",
    )


def init_run(text: str, workdir: Path, skills_roots: list[str]) -> dict[str, Any]:
    if workdir.exists() and any(workdir.iterdir()):
        raise SystemExit(f"Workdir is not empty: {workdir}")
    workdir.mkdir(parents=True, exist_ok=True)
    route_card = route(text)
    names = list(route_card["selected"]) + list(route_card["supporting_skills"])
    resolutions = resolve_many(dict.fromkeys(names), skills_roots)
    route_card["skill_resolution"] = resolutions
    missing_required = [item["name"] for item in resolutions if item["required"] and item["status"] != "found"]
    state: dict[str, Any] = {
        "schema_version": "1.0",
        "run_id": workdir.name,
        "created_at": _now(),
        "updated_at": _now(),
        "status": "planned",
        "current_phase": "intake",
        "next_action": _next_action(route_card),
        "route": route_card,
        "skill_resolution": resolutions,
        "missing_required_skills": missing_required,
        "phases": _initial_phase_state(),
        "history": [{"at": _now(), "event": "initialized", "phase": "intake"}],
    }
    _write_templates(workdir, route_card)
    _save_state(workdir, state)
    return state


def record_pilot(workdir: Path, decision: str, notes: str) -> dict[str, Any]:
    if decision not in PILOT_DECISIONS:
        raise SystemExit(f"Pilot decision must be one of: {', '.join(sorted(PILOT_DECISIONS))}")
    state = _load_state(workdir)
    phase = state["phases"]["pilot"]
    phase.update({"status": decision, "completed_at": _now(), "notes": [notes] if notes else []})
    report = workdir / "pilot-report.md"
    report.write_text(
        "# Pilot report\n\n"
        f"Decision: **{decision}**\n\n"
        f"Notes: {notes or 'No notes supplied.'}\n\n"
        "The pilot decision is a gate. It does not constitute a clinical effect estimate.\n",
        encoding="utf-8",
    )
    if decision == "proceed":
        state["current_phase"] = "execution"
        state["status"] = "ready_for_execution"
        state["next_action"] = "Run the prespecified analysis and record its artifact and diagnostics."
    elif decision == "downgrade":
        state["current_phase"] = "tte_protocol"
        state["status"] = "needs_redesign"
        state["next_action"] = "Revise the protocol or estimand in response to pilot limitations before estimating."
    else:
        state["current_phase"] = "pilot"
        state["status"] = "stopped"
        state["next_action"] = "Document why the pilot stopped and define a new research question or data plan."
    state["history"].append({"at": _now(), "event": "pilot_recorded", "decision": decision, "notes": notes})
    _save_state(workdir, state)
    return state


def record_feedback(workdir: Path, classification: str, notes: str, next_action: str) -> dict[str, Any]:
    if classification not in FEEDBACK_CLASSES:
        raise SystemExit(f"Feedback classification must be one of: {', '.join(sorted(FEEDBACK_CLASSES))}")
    state = _load_state(workdir)
    event = {
        "at": _now(),
        "phase": state["current_phase"],
        "classification": classification,
        "notes": notes,
        "next_action": next_action,
    }
    with (workdir / "feedback.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    with (workdir / "feedback.md").open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {event['at']} — {classification}\n\n{notes or 'No notes supplied.'}\n\nNext action: {next_action}\n")
    state["current_phase"] = "feedback"
    state["status"] = "feedback_recorded"
    state["next_action"] = next_action
    state["history"].append({"at": event["at"], "event": "feedback_recorded", "classification": classification})
    _save_state(workdir, state)
    return state


def complete_phase(workdir: Path, phase_name: str, artifact: str, notes: str) -> dict[str, Any]:
    if phase_name not in PHASES:
        raise SystemExit(f"Unknown phase: {phase_name}")
    artifact_path = (workdir / artifact).resolve()
    if not artifact_path.is_file():
        raise SystemExit(f"Artifact does not exist: {artifact}")
    if artifact == "evidence-map.json":
        evidence = _read_json(artifact_path)
        if evidence.get("status") == "not_started":
            raise SystemExit("evidence-map.json is still the initialization template; record verified searches first")
    state = _load_state(workdir)
    if state["current_phase"] != phase_name:
        raise SystemExit(f"Current phase is {state['current_phase']}; complete that phase before {phase_name}")
    phase = state["phases"][phase_name]
    phase.update({"status": "completed", "artifact": artifact, "completed_at": _now()})
    if notes:
        phase["notes"].append(notes)
    index = PHASES.index(phase_name)
    if index + 1 < len(PHASES):
        next_phase = PHASES[index + 1]
        if state["phases"][next_phase]["status"] == "queued":
            state["phases"][next_phase]["status"] = "ready"
        state["current_phase"] = next_phase
        state["next_action"] = f"Complete the `{next_phase}` phase and record its artifact."
    else:
        state["current_phase"] = phase_name
        state["status"] = "complete"
        state["next_action"] = "No further phase is scheduled."
    state["history"].append({"at": _now(), "event": "phase_completed", "phase": phase_name, "artifact": artifact})
    _save_state(workdir, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="initialize a new run without querying data")
    init_parser.add_argument("--text", required=True)
    init_parser.add_argument("--workdir", required=True, type=Path)
    init_parser.add_argument("--skills-root", action="append", default=[])

    status_parser = sub.add_parser("status", help="show a resumable run state")
    status_parser.add_argument("--workdir", required=True, type=Path)

    pilot_parser = sub.add_parser("record-pilot", help="record proceed/downgrade/stop gate")
    pilot_parser.add_argument("--workdir", required=True, type=Path)
    pilot_parser.add_argument("--decision", required=True, choices=sorted(PILOT_DECISIONS))
    pilot_parser.add_argument("--notes", default="")

    feedback_parser = sub.add_parser("feedback", help="record result feedback and next action")
    feedback_parser.add_argument("--workdir", required=True, type=Path)
    feedback_parser.add_argument("--classification", required=True, choices=sorted(FEEDBACK_CLASSES))
    feedback_parser.add_argument("--notes", default="")
    feedback_parser.add_argument("--next-action", required=True)

    complete_parser = sub.add_parser("complete-phase", help="record a phase artifact and advance state")
    complete_parser.add_argument("--workdir", required=True, type=Path)
    complete_parser.add_argument("--phase", required=True, choices=PHASES)
    complete_parser.add_argument("--artifact", required=True)
    complete_parser.add_argument("--notes", default="")

    args = parser.parse_args()
    if args.command == "init":
        result = init_run(args.text, args.workdir, args.skills_root)
    elif args.command == "status":
        result = _load_state(args.workdir)
    elif args.command == "record-pilot":
        result = record_pilot(args.workdir, args.decision, args.notes)
    elif args.command == "feedback":
        result = record_feedback(args.workdir, args.classification, args.notes, args.next_action)
    else:
        result = complete_phase(args.workdir, args.phase, args.artifact, args.notes)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
