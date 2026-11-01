"""What may not reach the public repository.

One definition, used by tools/publish.py and by the CI guard on the public repo.
Returns the name of the rule that excluded a path, so a refusal can say why.
"""
import fnmatch
import re
from pathlib import PurePosixPath

EXCLUDED_PREFIXES = (
    "sources/",
    "source_catalog/",
    "archive/",
    "docs/",
    "slides/quiz/",
    "slides/exam/",
    ".claude/",
    ".agents/",
)

EXCLUDED_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "README_INTERNAL.md",
)
EXCLUDED_CACHE_DIRS = {".pixi", ".pytest_cache", "__pycache__", ".build",
                       ".render", "tmp", "partial_movie_files"}

EXCLUDED_NAMES = (
    "PLAN.md",
    "ISSUES.md",
    "PROVENANCE.json",
    "IDEAS.md",
    "TEACHING_NOTES.md",
)

EXCLUDED_GLOBS = (
    "*.xlsx",
    "0*_*.md",
)

ROOT_FILES = {"README.md", "SOURCES.md", ".gitignore"}
ROOT_DIRS = ("slides_template/", "slides/lecture/", "slides/homework/")
TOOLS_PUBLISHED = ("tools/check_deck.py", "tools/in2ro/")

# A week folder is a whitelist, never a blacklist. Authoring leaves teaching notes,
# provenance updates, scratch source lists and editor backups beside the deck, and no
# list of their names can be kept complete — so name what students may have instead.
WEEK_RE = re.compile(r"^slides/(?P<kind>lecture|homework)/(?P<week>W[0-9][0-9]|Hard_[0-9]+)/(?P<rest>.+)$")
WEEK_DIRS = ("resources/", "input_data/", "fibeamer/", "fonts/")
WEEK_FILES = ("beamerthemefibeamer.sty", "latexmkrc", ".latexmkrc", "biblio.bib")
WEEK_DECK = "In2Ro_*.tex"
# Vector figures the deck includes directly — two_bros_fig.pdf is one. The build
# product In2Ro_*.pdf is git-ignored, so it is never in the index to begin with.
WEEK_FIGURE = "*.pdf"


def is_excluded(path: str) -> str | None:
    path = PurePosixPath(path).as_posix()
    parts = path.split("/")
    if any(part in EXCLUDED_CACHE_DIRS for part in parts[:-1]):
        return "under a generated cache directory"

    for prefix in EXCLUDED_PREFIXES:
        if path.startswith(prefix):
            return f"under {prefix}"
    if "solutions" in parts[:-1]:
        return "under a solutions/ directory"
    if path in EXCLUDED_FILES:
        return f"{path} is instructor-only"
    if parts[-1] in EXCLUDED_NAMES:
        return f"{parts[-1]} is internal"
    for pattern in EXCLUDED_GLOBS:
        if fnmatch.fnmatch(parts[-1], pattern) and len(parts) == 1:
            return f"matches {pattern}"
        if fnmatch.fnmatch(path, pattern):
            return f"matches {pattern}"
    if path.startswith("tools/"):
        if any(path == keep or path.startswith(keep) for keep in TOOLS_PUBLISHED):
            return None
        return "tools/ is internal except check_deck.py and in2ro/"
    match = WEEK_RE.match(path)
    if match:
        rest = match.group("rest")
        if rest.startswith(WEEK_DIRS) or rest in WEEK_FILES:
            return None
        if "/" not in rest and fnmatch.fnmatch(rest, WEEK_DECK):
            return None
        pdf_prefix = "lec" if match.group("kind") == "lecture" else "hw"
        week = match.group("week")
        suffix = "_hard" + week[5:] if week.startswith("Hard_") else week[1:]
        if rest == f"In2Ro_{pdf_prefix}{suffix}.pdf":
            return None
        if "/" not in rest and fnmatch.fnmatch(rest, WEEK_FIGURE) \
                and not rest.startswith("In2Ro_"):
            return None
        return ("a week folder publishes only In2Ro_*.tex, resources/, input_data/ "
                "and the theme")
    if path in ROOT_FILES or path.startswith("slides_template/"):
        return None
    if path in (".github/workflows/build.yml", ".github/workflows/guard.yml"):
        return None
    return "outside the public root whitelist"
