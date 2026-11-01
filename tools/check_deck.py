"""The QA gate. Every deck must pass before it is committed.

    python tools/check_deck.py --kind lecture --week W02
    python tools/check_deck.py --kind lecture --week W02 --no-compile
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from in2ro import paths, texutil as T

MAX_ASSET = 5 * 1024 * 1024
WARN_ASSET = 800 * 1024
PAGE_NUMBER_RE = re.compile(r"\b(?:p\.?|pp\.?|page|pages|slide|slides)\s*\d", re.I)
HANDLE_RE = re.compile(r"\b((?:DL|KL|SB|SW|AH|OB)_[0-9A-Za-z_]+)\b")
FRAME_BLOCK_RE = re.compile(
    r"\\begin\{frame\}(?:\[[^\]]*\])?\{([^{}\n]*)\}(.*?)\\end\{frame\}", re.S)
QUIZ_QUESTION_LABEL_RE = re.compile(r"\\textbf\{Question\s+(\d+)\}")


class Report:
    def __init__(self):
        self.failures, self.warnings = [], []

    def fail(self, message):
        self.failures.append(message)

    def warn(self, message):
        self.warnings.append(message)


def compile_deck(folder, deck, report):
    build = folder / ".build" / "qa"
    build.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["latexmk", "-xelatex", "-interaction=nonstopmode", f"-outdir={build}", deck.name],
        cwd=folder, capture_output=True, text=True)
    log = build / (deck.stem + ".log")
    if proc.returncode != 0:
        tail = log.read_text(encoding="utf-8", errors="replace")[-2000:] if log.exists() else proc.stdout[-2000:]
        report.fail(f"latexmk exited {proc.returncode}\n{tail}")
        return
    if log.exists():
        overfull = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines()
                    if l.startswith(("Overfull \\hbox", "Overfull \\vbox"))]
        if overfull:
            report.warn(f"{len(overfull)} overfull horizontal/vertical boxes in {log.name}")
    compiled = build / (deck.stem + ".pdf")
    if not compiled.is_file():
        report.fail(f"latexmk did not create {compiled.name}")
        return
    shutil.copyfile(compiled, deck.with_suffix(".pdf"))


def check_structure(text, skeleton, kind, report):
    for problem in T.head_differences(text, skeleton):
        report.fail(problem)
    for problem in T.subtitle_problems(text, kind):
        report.fail(problem)
    try:
        _, tail = T.split_tail(text)
    except ValueError:
        report.fail(f"missing frozen tail: {T.TAIL_START} and \\frame[plain]{{}}")
    else:
        if "\\frame[plain]{}" not in tail:
            report.fail(f"missing frozen tail: {T.TAIL_START} and \\frame[plain]{{}}")
    for number, line in T.body_comment_lines(text):
        report.fail(f"comment below the frozen head at line {number}: {line}")
    for number, line in T.speaker_notes(text):
        report.fail(f"speaker note below the frozen head at line {number}: {line}")


def check_assets(folder, text, report):
    for number, target in T.graphics_paths(text):
        candidates = [folder / target, folder / "resources" / target]
        found = next((p for p in candidates if p.exists()), None)
        if found is None:
            report.fail(f"line {number}: \\includegraphics points at {target}, which does not exist")
            continue
        size = found.stat().st_size
        if size > MAX_ASSET:
            report.fail(f"{found.name} is {size / 1024 / 1024:.1f} MB, above the 5 MB ceiling")
        elif size > WARN_ASSET:
            report.warn(f"{found.name} is {size / 1024:.0f} KB, above 800 KB")


def check_counts(folder, text, kind, report):
    frames = T.frame_count(text)
    plan = folder / "PLAN.md"
    ideas = folder / "IDEAS.md"
    if kind == "quiz" and not ideas.exists():
        report.fail("a quiz week needs IDEAS.md with its approved questions")
        return
    if kind == "lecture":
        # The Reference Materials frame is generated from the plan, not listed in it.
        content = frames - 1 if T.has_reference_frame(text) else frames
        if not plan.exists():
            if os.environ.get("IN2RO_PUBLIC") == "1":
                return      # PLAN.md is internal; CI on the public repo never sees one
            report.fail("a lecture week needs a PLAN.md")
            return
        planned = len(re.findall(r"^### F\d+", plan.read_text(encoding="utf-8"), re.M))
        if planned and planned != content:
            report.fail(f"content frame count {content} does not match PLAN.md's {planned}")
    elif ideas.exists():
        ideas_text = ideas.read_text(encoding="utf-8")
        approved_numbers = [int(number) for number in re.findall(
            r"^### (?:Task|Question) (\d+)", ideas_text, re.M)]
        approved = len(approved_numbers)
        if kind == "quiz" and approved:
            titles = T.frame_titles(text)
            expected_title = f"Quiz {int(folder.name[1:])}"
            if not titles or titles[0] != expected_title:
                report.fail(f"{expected_title} must be the first content frame after the title")
            if any(title not in ("Answers", "Answer", "Solutions", "Solution")
                   for title in titles[1:]):
                report.fail("only answer or solution frames may follow the Quiz frame")
            quiz_frames = [body for title, body in FRAME_BLOCK_RE.findall(T.body_code_only(text))
                           if title.strip() == expected_title]
            if len(quiz_frames) != 1:
                report.fail(f"quiz questions must appear together on exactly one Quiz frame; "
                            f"found {len(quiz_frames)}")
                return
            labels = [int(number) for number in QUIZ_QUESTION_LABEL_RE.findall(quiz_frames[0])]
            if labels != approved_numbers:
                report.fail(f"the Quiz frame labels questions {labels}, but IDEAS.md approves "
                            f"{approved_numbers}; write each as \\textbf{{Question N}}")

        elif approved and frames < approved:
            report.fail(f"frame count {frames} is below IDEAS.md's {approved} approved tasks")


def check_references(folder, text, kind, report):
    if kind != "lecture":
        return
    items = T.reference_items(text)
    if not items:
        report.fail("a lecture deck needs a non-empty Reference Materials frame")
        return
    for item in items:
        if PAGE_NUMBER_RE.search(item):
            report.fail(f"page or slide number in the Reference Materials frame: {item}")
    for item in items:
        if HANDLE_RE.fullmatch(item.strip()):
            report.fail(f"the Reference Materials frame lists the bare handle {item.strip()}; "
                        f"an item carries the source's citation — author and topic")
    plan = folder / "PLAN.md"
    if not plan.exists():
        return
    from in2ro import sources as S, plan as P
    try:
        parsed = P.parse(plan.read_text(encoding="utf-8"))
    except ValueError as exc:
        report.fail(str(exc))
        return
    used = set(parsed["handles"])
    index = S.read_sources_md()
    for handle in sorted(used):
        source = index.get(handle)
        if source is None:
            continue  # SOURCES.md has no entry for it; nothing to cross-check yet
        if not any(source.citation == item.strip() for item in items):
            report.fail(f"{handle} is used in PLAN.md but no \\item covers it")
    citations = {index[h].citation for h in used if h in index}
    citations.update(parsed.get("external_references", []))
    for citation in parsed.get("external_references", []):
        if citation not in items:
            report.fail(f"external reference {citation!r} is missing from Reference Materials")
    for item in items:
        if citations and item not in citations:
            report.fail(f"the Reference Materials frame lists {item!r}, "
                        f"which no source in PLAN.md accounts for")


def check_scaffolding(folder, report):
    if (folder / "blocks").exists():
        report.fail("leftover blocks/ — assembly did not finish")
    if (folder / ".build").exists() and any((folder / ".build").glob("[!q]*")):
        report.fail("leftover .build/ from block compilation")
    for stray in folder.glob("_preview_*.tex"):
        report.fail(f"leftover {stray.name}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind", required=True, choices=sorted(paths.KINDS))
    parser.add_argument("--week", required=True)
    parser.add_argument("--no-compile", action="store_true", help="skip latexmk (structure only)")
    args = parser.parse_args(argv)

    folder = paths.week_dir(args.kind, args.week)
    deck = paths.deck_path(args.kind, args.week)
    if not deck.exists():
        print(f"FAIL {deck} does not exist", file=sys.stderr)
        return 1

    text = deck.read_text(encoding="utf-8")
    skeleton = paths.skeleton_path(args.kind).read_text(encoding="utf-8")
    report = Report()

    check_structure(text, skeleton, args.kind, report)
    check_assets(folder, text, report)
    check_counts(folder, text, args.kind, report)
    check_references(folder, text, args.kind, report)
    check_scaffolding(folder, report)
    if not args.no_compile and not report.failures:
        compile_deck(folder, deck, report)

    for warning in report.warnings:
        print(f"WARN {warning}")
    for failure in report.failures:
        print(f"FAIL {failure}")

    if report.failures:
        print(f"\n{deck.name}: {len(report.failures)} failure(s), {len(report.warnings)} warning(s)")
        return 1
    print(f"OK {deck.name}: {T.frame_count(text)} frames, "
          f"{len(report.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
