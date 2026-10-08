"""PLAN.md is a specification, not LaTeX. One '### FNN - title' entry per frame."""
import re

HANDLE_RE = re.compile(r"\b((?:DL|KL|SB|SW|AH)_[0-9A-Za-z_]+)\b")
FRAME_RE = re.compile(r"^###\s+(F\d+)\s*[-\u2013\u2014]+\s*(.*?)\s*$")


def parse(text) -> dict:
    frames, handles, external = [], [], []
    current = None
    for line in text.splitlines():
        if line.strip().startswith("external_reference:"):
            parts = [part.strip() for part in line.split(":", 1)[1].split("|")]
            if len(parts) != 2 or not all(parts):
                raise ValueError("external_reference needs author | topic")
            escapes = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
                       "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
                       "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
            citation = " --- ".join("".join(escapes.get(c, c) for c in part) for part in parts)
            if citation not in external:
                external.append(citation)
            continue
        match = FRAME_RE.match(line)
        if match:
            current = {"id": match.group(1), "title": match.group(2), "sources": []}
            frames.append(current)
            continue
        for handle in HANDLE_RE.findall(line):
            if current is not None and handle not in current["sources"]:
                current["sources"].append(handle)
            if handle not in handles:
                handles.append(handle)
    parsed = {"frames": frames, "handles": handles}
    if external:
        parsed["external_references"] = external
    return parsed


def reference_frame(handles, index, external=()) -> str:
    items = []
    for handle in handles:
        source = index.get(handle)
        if source is None:
            raise ValueError(f"{handle} is used in PLAN.md but SOURCES.md has no entry for it, "
                             f"so it cannot be cited")
        items.append(f"        \\item {source.citation}")
    items.extend(f"        \\item {citation}" for citation in external
                 if f"        \\item {citation}" not in items)
    return (
        "\\begin{frame}[t]{Reference Materials}\n"
        "    \\begin{itemize}\n"
        + "\n".join(items) + "\n"
        "    \\end{itemize}\n"
        "\\end{frame}\n"
    )
