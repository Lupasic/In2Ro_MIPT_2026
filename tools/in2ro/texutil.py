"""Structure of a deck: the frozen head, the frozen tail, and what may sit between."""
import re

HEAD_END = "\\fbckg{fibeamer/figs/common.png}"
TAIL_START = "\\fbckg{fibeamer/figs/last_page.png}"
BODY_MARKER = "%%BODY%%"
REF_FRAME_OPEN = "\\begin{frame}[t]{Reference Materials}"

TITLE_RE = re.compile(r"^\\title(\[.*?\])?\{")
SUBTITLE_OPEN_RE = re.compile(r"^\\subtitle\{")
FRAME_OPEN_RE = re.compile(r"\\begin\{frame\}(?:\[[^\]]*\])?(?:\{(.*)\})?")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", re.S)
ITEM_RE = re.compile(r"^\s*\\item\s+(.*?)\s*$")
VERBATIM_OPEN_RE = re.compile(r"\\begin\{(lstlisting|verbatim|minted)\}")
VERBATIM_CLOSE_RE = re.compile(r"\\end\{(lstlisting|verbatim|minted)\}")
NOTE_RE = re.compile(r"\\note\b\s*(?:<[^>]*>)?\s*[\{\[]")


def _lines(text):
    return text.splitlines(keepends=True)


def _head_index(text) -> int:
    for i, line in enumerate(_lines(text)):
        if line.rstrip("\r\n") == HEAD_END:
            return i
    raise ValueError(f"no frozen head: the deck has no line {HEAD_END!r}")


def split_head(text) -> tuple[str, str]:
    lines = _lines(text)
    i = _head_index(text)
    return "".join(lines[: i + 1]), "".join(lines[i + 1:])


def split_tail(text) -> tuple[str, str]:
    lines = _lines(text)
    for i, line in enumerate(lines):
        if line.rstrip("\r\n") == TAIL_START:
            return "".join(lines[:i]), "".join(lines[i:])
    raise ValueError(f"no frozen tail: the deck has no line {TAIL_START!r}")


def _variable_head_lines(head_lines) -> set[int]:
    """Indices of the \\title line and the lines of the \\subtitle block."""
    variable = set()
    for i, line in enumerate(head_lines):
        if TITLE_RE.match(line):
            variable.add(i)
        if SUBTITLE_OPEN_RE.match(line):
            j = i
            while j < len(head_lines):
                variable.add(j)
                if "}" in head_lines[j].split("%%")[0]:
                    break
                j += 1
    return variable


def head_differences(deck_text, skeleton_text) -> list[str]:
    deck_head = _lines(split_head(deck_text)[0])
    skel_head = _lines(split_head(skeleton_text)[0])
    if len(deck_head) != len(skel_head):
        return [f"frozen head is {len(deck_head)} lines, the skeleton's is {len(skel_head)}"]
    variable = _variable_head_lines(skel_head) | _variable_head_lines(deck_head)
    problems = []
    for i, (got, want) in enumerate(zip(deck_head, skel_head)):
        if i in variable or got == want:
            continue
        problems.append(f"frozen head differs on line {i + 1}: {got.rstrip()!r} "
                        f"but the skeleton has {want.rstrip()!r}")
    return problems


def subtitle_of(text) -> str | None:
    lines = _lines(split_head(text)[0])
    for i, line in enumerate(lines):
        if SUBTITLE_OPEN_RE.match(line):
            collected = []
            for j in range(i, len(lines)):
                collected.append(lines[j])
                if "}" in lines[j].split("%%")[0]:
                    break
            return "".join(collected)
    return None


def subtitle_problems(text, kind) -> list[str]:
    raw = subtitle_of(text)
    if raw is None:
        return ["no \\subtitle in the frozen head"]
    inner = raw.split("{", 1)[1].rsplit("}", 1)[0] if "{" in raw else ""
    parts = inner.split("\\\\")
    problems = []
    if len(parts) != 3:
        problems.append(f"the subtitle must have exactly three lines separated by two "
                        f"'\\\\\\\\', found {len(parts)}")
        return problems
    for n, part in enumerate(parts, start=1):
        if part.strip(" ") == "":
            if kind == "lecture":
                if part == "":
                    problems.append(f"subtitle line {n} is empty; an empty line must be a space")
            else:
                problems.append(f"subtitle line {n} is empty or only spaces; a quiz or homework "
                                f"subtitle writes an empty line as an escaped space")
    if kind == "lecture" and not parts[2].endswith("  "):
        problems.append("a lecture subtitle ends with two spaces before the closing brace")
    return problems


def body_outside_verbatim(text) -> str:
    """The body below the frozen head, with every line of a verbatim-like block replaced by
    an empty line. Line numbering is preserved so callers can still report line numbers."""
    body = split_head(text)[1]
    out = []
    in_verbatim = False
    for raw in _lines(body):
        line = raw.rstrip("\r\n")
        newline = raw[len(line):]
        if VERBATIM_OPEN_RE.search(line):
            in_verbatim = True
        if VERBATIM_CLOSE_RE.search(line):
            in_verbatim = False
            out.append(newline)
            continue
        if in_verbatim:
            out.append(newline)
            continue
        out.append(raw)
    return "".join(out)


def body_code_only(text) -> str:
    """The body below the frozen head with verbatim blocks blanked and every line truncated at
    its first real comment character. Line numbering is preserved, so callers can still report
    line numbers."""
    out = []
    for raw in _lines(body_outside_verbatim(text)):
        line = raw.rstrip("\r\n")
        newline = raw[len(line):]
        position = first_comment_char(line)
        if position is not None:
            line = line[:position]
        out.append(line + newline)
    return "".join(out)


def body_comment_lines(text) -> list[tuple[int, str]]:
    """1-based line numbers of comments below the frozen head."""
    start = _head_index(text) + 1
    found = []
    for offset, raw in enumerate(_lines(body_outside_verbatim(text)), start=start):
        line = raw.rstrip("\r\n")
        position = first_comment_char(line)
        if position is None:
            continue
        if line[position:].strip() == "%":       # a bare % suppresses a space
            continue
        found.append((offset + 1, line.strip()))
    return found


def speaker_notes(text) -> list[tuple[int, str]]:
    """1-based line numbers of speaker-note macros below the frozen head, verbatim blocks ignored."""
    start = _head_index(text) + 1
    found = []
    for offset, raw in enumerate(_lines(body_code_only(text)), start=start):
        line = raw.rstrip("\r\n")
        if NOTE_RE.search(line):
            found.append((offset + 1, line.strip()))
    return found


def first_comment_char(line) -> int | None:
    i = 0
    while i < len(line):
        char = line[i]
        if char == "\\":
            i += 2
            continue
        if char == "%":
            return i
        i += 1
    return None


_first_comment_char = first_comment_char


def frame_count(text) -> int:
    return len(FRAME_OPEN_RE.findall(body_code_only(text)))


def frame_titles(text) -> list[str]:
    return [(m or "").strip() for m in FRAME_OPEN_RE.findall(body_code_only(text))]


def graphics_paths(text) -> list[tuple[int, str]]:
    offset = len(_lines(split_head(text)[0]))
    body = body_code_only(text)
    found = []
    for m in GRAPHICS_RE.finditer(body):
        number = offset + 1 + body.count("\n", 0, m.start())
        found.append((number, m.group(1).strip()))
    return found


def has_reference_frame(text) -> bool:
    return REF_FRAME_OPEN in body_code_only(text)


def reference_items(text) -> list[str]:
    body = body_code_only(text)
    if REF_FRAME_OPEN not in body:
        return []
    block = body.split(REF_FRAME_OPEN, 1)[1].split("\\end{frame}", 1)[0]
    return [m.group(1) for m in (ITEM_RE.match(line) for line in block.splitlines()) if m]
