"""Poppler wrappers. No image library is installed."""
import struct
import subprocess
from collections import Counter
from pathlib import Path


class PopplerError(RuntimeError):
    pass


def run(cmd) -> tuple[str, str]:
    """Run a poppler command. Returns (stdout, stderr).

    stderr is returned, never interpreted: this poppler build prints
    'No display font for Symbol' on every file and still exits 0.
    """
    proc = subprocess.run([str(part) for part in cmd], capture_output=True, text=True)
    if proc.returncode != 0:
        raise PopplerError(f"{cmd[0]} failed ({proc.returncode}): {proc.stderr.strip()}")
    return proc.stdout, proc.stderr


def page_count(pdf: Path) -> int:
    out, _ = run(["pdfinfo", pdf])
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1])
    raise PopplerError(f"pdfinfo reported no page count for {pdf}")


PREVIEW_W, PREVIEW_H = 1400, 1050


def png_size(png: Path) -> tuple[int, int]:
    header = Path(png).open("rb").read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{png} is not a PNG")
    return struct.unpack(">II", header[16:24])


def _sole_output(out_prefix: Path, page: int) -> Path:
    """pdftoppm pads the page number to the width of the document's page count, so
    the produced name is not predictable. Each call therefore needs a clean prefix."""
    prefix = Path(out_prefix)
    produced = sorted(prefix.parent.glob(prefix.name + "-*.png"))
    if len(produced) != 1:
        raise PopplerError(
            f"expected one PNG for page {page} under {prefix}, "
            f"found {[p.name for p in produced]}; use an empty directory per render"
        )
    return produced[0]


def render_page(pdf: Path, page: int, out_prefix: Path, k: int = 1) -> tuple[Path, str]:
    _, stderr = run([
        "pdftoppm", "-f", page, "-l", page, "-png",
        "-scale-to-x", PREVIEW_W * k, "-scale-to-y", PREVIEW_H * k,
        pdf, out_prefix,
    ])
    return _sole_output(out_prefix, page), stderr


def render_crop(pdf: Path, page: int, box: tuple[int, int, int, int], out_prefix: Path,
                 k: int = 1) -> tuple[Path, str]:
    """box is (x, y, w, h) in the 1400x1050 preview space and scales linearly with k."""
    x, y, w, h = box
    if w <= 0 or h <= 0:
        raise ValueError(f"crop box must have positive width and height, got {box}")
    if x < 0 or y < 0 or x + w > PREVIEW_W or y + h > PREVIEW_H:
        raise ValueError(
            f"crop box {box} leaves the {PREVIEW_W} x {PREVIEW_H} preview space")
    _, stderr = run([
        "pdftoppm", "-f", page, "-l", page, "-png",
        "-scale-to-x", PREVIEW_W * k, "-scale-to-y", PREVIEW_H * k,
        "-x", x * k, "-y", y * k, "-W", w * k, "-H", h * k,
        pdf, out_prefix,
    ])
    return _sole_output(out_prefix, page), stderr


def list_images(pdf: Path, page: int) -> list[dict]:
    """One entry per row of `pdfimages -list`, in `num` order.

    `pdfimages -png` writes one file per row, including `smask` rows, so `num` is
    also the index of the produced file.
    """
    out, _ = run(["pdfimages", "-list", "-f", page, "-l", page, pdf])
    rows = []
    for line in out.splitlines()[2:]:
        fields = line.split()
        if len(fields) < 11 or not fields[0].isdigit():
            continue
        rows.append({
            "page": int(fields[0]),
            "num": int(fields[1]),
            "type": fields[2],
            "width": int(fields[3]),
            "height": int(fields[4]),
            "object_id": int(fields[10]),
        })
    return rows


def content_object_ids(pdf: Path, furniture_ratio: float = 0.25) -> set[int]:
    """Object IDs that are not slide furniture.

    A PowerPoint export repeats the master's background and logo on every page. An
    object appearing on more than `furniture_ratio` of the pages is furniture.
    """
    total = page_count(pdf)
    seen = Counter()
    for page in range(1, total + 1):
        for row in list_images(pdf, page):
            seen[row["object_id"]] += 1
    limit = max(1, total * furniture_ratio)
    return {object_id for object_id, count in seen.items() if count <= limit}


def extract_image(pdf: Path, page: int, index: int, out_prefix: Path) -> tuple[Path, str]:
    """Native extraction of one embedded raster, addressed by its `num` on the page."""
    _, stderr = run(["pdfimages", "-f", page, "-l", page, "-png", pdf, out_prefix])
    prefix = Path(out_prefix)
    produced = sorted(prefix.parent.glob(prefix.name + "-*.png"))
    if index < 0 or index >= len(produced):
        raise PopplerError(
            f"page {page} holds {len(produced)} images, asked for index {index}"
        )
    return produced[index], stderr


def parse_pages(tokens: list[str]) -> list[int]:
    """'3' '7-8' '11,13' -> [3, 7, 8, 11, 13], sorted and de-duplicated."""
    pages: list[int] = []
    for token in tokens:
        for part in str(token).split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                first, last = part.split("-", 1)
                first, last = int(first), int(last)
                if last < first:
                    raise ValueError(f"backwards page range: {part}")
                pages.extend(range(first, last + 1))
            else:
                pages.append(int(part))
    return sorted(dict.fromkeys(pages))
