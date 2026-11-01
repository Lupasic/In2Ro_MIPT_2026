"""Repository locations. Every tool resolves paths through this module so that
tests can redirect the whole toolchain with IN2RO_ROOT."""
import os
from pathlib import Path

KINDS = {"lecture": "lec", "homework": "hw", "quiz": "qz"}


def repo_root() -> Path:
    override = os.environ.get("IN2RO_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[2]


def sources_dir() -> Path:
    return repo_root() / "sources"


def sources_md() -> Path:
    return repo_root() / "SOURCES.md"


def slides_dir() -> Path:
    return repo_root() / "slides"


def template_dir() -> Path:
    return repo_root() / "slides_template"


def _check_kind(kind: str) -> str:
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}, expected one of {sorted(KINDS)}")
    return KINDS[kind]


def week_dir(kind: str, week: str) -> Path:
    _check_kind(kind)
    return slides_dir() / kind / week


def week_suffix(week: str) -> str:
    """W09 -> '09' (In2Ro_hw09.tex); Hard_1 -> '_hard1' (In2Ro_hw_hard1.tex)."""
    if week.startswith("Hard_"):
        return "_hard" + week[len("Hard_"):]
    return week[1:]


def deck_path(kind: str, week: str) -> Path:
    short = _check_kind(kind)
    return week_dir(kind, week) / f"In2Ro_{short}{week_suffix(week)}.tex"


def skeleton_path(kind: str) -> Path:
    return template_dir() / f"In2Ro_{_check_kind(kind)}.tex"
