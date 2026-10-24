#!/usr/bin/env python3
"""Resolve named TTE and research skills without machine-specific paths."""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PACKAGE_ROOT / "references" / "skill-registry.json"


@dataclass(frozen=True)
class SkillSpec:
    name: str
    lane: str
    phase: str
    required: bool


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def specs(path: Path = REGISTRY_PATH) -> dict[str, SkillSpec]:
    payload = load_registry(path)
    return {
        item["name"]: SkillSpec(
            name=item["name"],
            lane=item["lane"],
            phase=item["phase"],
            required=bool(item.get("required", False)),
        )
        for item in payload["skills"]
    }


def _split_roots(value: str | None) -> list[Path]:
    if not value:
        return []
    return [Path(part).expanduser() for part in value.split(os.pathsep) if part]


def default_roots(extra: Iterable[str | Path] = ()) -> list[Path]:
    """Return conventional roots while allowing project-specific overrides."""
    roots: list[Path] = []
    # An explicit root belongs to the current run and must take precedence over
    # any globally installed copy with the same skill name.
    roots.extend(Path(item).expanduser() for item in extra)
    for env_name in ("CODEX_SKILLS_ROOT", "DAXUAN_SKILLS_ROOT"):
        roots.extend(_split_roots(os.environ.get(env_name)))
    tte_home = os.environ.get("TTE_CC_HOME")
    if tte_home:
        roots.append(Path(tte_home).expanduser() / ".claude" / "skills")
    roots.append(Path.home() / ".codex" / "skills")
    roots.append(Path.home() / ".tte_cc" / ".claude" / "skills")
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            unique.append(root)
            seen.add(key)
    return unique


def resolve_skill(name: str, roots: Iterable[str | Path] = ()) -> dict[str, object]:
    registry = specs()
    spec = registry.get(name)
    if spec is None:
        return {
            "name": name,
            "status": "unregistered",
            "lane": "unknown",
            "phase": "unknown",
            "required": False,
            "path": None,
            "searched_roots": [str(item) for item in default_roots(roots)],
        }
    searched = default_roots(roots)
    for root in searched:
        candidate = root / name / "SKILL.md"
        if candidate.is_file():
            return {
                "name": name,
                "status": "found",
                "lane": spec.lane,
                "phase": spec.phase,
                "required": spec.required,
                "path": str(candidate.resolve()),
                "searched_roots": [str(item) for item in searched],
            }
    return {
        "name": name,
        "status": "missing",
        "lane": spec.lane,
        "phase": spec.phase,
        "required": spec.required,
        "path": None,
        "searched_roots": [str(item) for item in searched],
    }


def resolve_many(names: Iterable[str], roots: Iterable[str | Path] = ()) -> list[dict[str, object]]:
    return [resolve_skill(name, roots) for name in names]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", dest="skills", default=[])
    parser.add_argument("--skills-root", action="append", default=[])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    names = args.skills or list(specs())
    result = {
        "registry": str(REGISTRY_PATH),
        "skills": resolve_many(names, args.skills_root),
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["skills"]:
            print(f"{item['name']}: {item['status']}" + (f" ({item['path']})" if item["path"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
