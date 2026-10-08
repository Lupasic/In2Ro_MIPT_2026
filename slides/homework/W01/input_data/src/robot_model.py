"""Loads ``ar601m.yaml`` into a plain Python dict.

This is a hand-written reader for the one small, flat YAML shape
``ar601m.yaml`` actually uses: a few top-level scalars, then two lists
(``links:`` and ``joints:``) whose entries are each a single-line flow
mapping, e.g. ``{name: l1, length: 0.40, axis: [0, 0, 1], mass: null,
inertia: null, stiffness: null}``.

It is deliberately not a general YAML parser and does not try to become
one -- adding a PyYAML dependency to this skeleton was declined on
purpose (see ``README.md``), so parsing the handful of lines this one
file contains is cheaper and clearer than depending on a library for it.
If you change the shape of ``ar601m.yaml`` beyond this file's format,
extend this reader or swap in a real YAML library in your own copy.

Usage::

    import robot_model
    robot = robot_model.load()
    robot["arm"]                  # "right" or "left"
    robot["shoulder_offset_deg"]  # float
    robot["links"]                # list of dicts: name, length, axis, ...
    robot["joints"]               # list of dicts: name, type, axis, ...
"""
import os
import re

_FLOW_ITEM_RE = re.compile(r"^\s*-\s*\{(.*)\}\s*$")

_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "ar601m.yaml")


def _parse_scalar(text):
    """Parse one YAML scalar: null, a bracketed list, a number, or a bare string."""
    text = text.strip()
    if text == "null":
        return None
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(v) for v in inner.split(",")]
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text.strip('"').strip("'")


def _split_top_level(text):
    """Split a flow mapping's body on commas that are not inside ``[ ]``."""
    parts = []
    depth = 0
    start = 0
    for i, ch in enumerate(text):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(text[start:i])
            start = i + 1
    parts.append(text[start:])
    return parts


def _parse_flow_mapping(body):
    entry = {}
    for part in _split_top_level(body):
        if not part.strip():
            continue
        key, _, value = part.partition(":")
        entry[key.strip()] = _parse_scalar(value)
    return entry


def load(path=None):
    """Parse ``ar601m.yaml`` (or ``path``) into a robot dict.

    Returns a dict with keys ``arm``, ``shoulder_offset_deg``, ``links``
    (a list of 4 link dicts) and ``joints`` (a list of 6 joint dicts, in
    chain order t1..t6).
    """
    if path is None:
        path = _DEFAULT_PATH
    robot = {"links": [], "joints": []}
    section = None
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.split("#", 1)[0].rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("links:"):
                section = "links"
                continue
            if line.startswith("joints:"):
                section = "joints"
                continue
            match = _FLOW_ITEM_RE.match(line)
            if match and section in ("links", "joints"):
                robot[section].append(_parse_flow_mapping(match.group(1)))
                continue
            if section is None and ":" in line:
                key, _, value = line.partition(":")
                robot[key.strip()] = _parse_scalar(value)
    return robot


if __name__ == "__main__":
    import pprint

    pprint.pprint(load())
