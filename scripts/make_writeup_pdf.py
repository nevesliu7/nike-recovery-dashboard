from __future__ import annotations

import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).resolve().parents[1]
WRITEUP_MD = ROOT / "writeup.md"
WRITEUP_PDF = ROOT / "writeup.pdf"


def strip_md(line: str) -> str:
    line = re.sub(r"^#+\s*", "", line)
    line = line.replace("**", "")
    return line.strip()


def parse_sections(markdown: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title = "Nike Global Brand Recovery Dashboard"
    current_lines: list[str] = []
    for raw in markdown.splitlines():
        if raw.startswith("# "):
            current_title = strip_md(raw)
            continue
        if raw.startswith("## "):
            if current_lines:
                sections.append((current_title, current_lines))
            current_title = strip_md(raw)
            current_lines = []
            continue
        if raw.strip():
            current_lines.append(strip_md(raw))
    if current_lines:
        sections.append((current_title, current_lines))
    return sections


def draw_page(pdf: PdfPages, title: str, sections: list[tuple[str, list[str]]], page_num: int) -> None:
    fig = plt.figure(figsize=(8.5, 11))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    fig.patch.set_facecolor("#fbfbf7")

    ax.add_patch(plt.Rectangle((0.0, 0.0), 0.045, 1.0, transform=ax.transAxes, color="#111111"))
    ax.add_patch(plt.Rectangle((0.045, 0.945), 0.955, 0.018, transform=ax.transAxes, color="#c8ff00"))
    ax.text(0.08, 0.92, title, fontsize=18, weight="bold", color="#111111", va="top")

    y = 0.86
    for heading, paragraphs in sections:
        ax.text(0.08, y, heading, fontsize=11.5, weight="bold", color="#111111", va="top")
        y -= 0.028
        for paragraph in paragraphs:
            wrapped = textwrap.wrap(paragraph, width=92)
            for line in wrapped:
                ax.text(0.08, y, line, fontsize=9.2, color="#222222", va="top")
                y -= 0.019
            y -= 0.012
        y -= 0.006

    ax.text(0.93, 0.035, f"Page {page_num}", fontsize=8.5, color="#555555", ha="right")
    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    sections = parse_sections(WRITEUP_MD.read_text())
    title = "Nike Global Brand Recovery Dashboard"

    page_sections = [
        [
            sections[0],
            sections[1],
            sections[2],
        ],
        [
            sections[3],
            sections[4],
        ],
        [
            sections[5],
            sections[6],
        ],
    ]

    with PdfPages(WRITEUP_PDF) as pdf:
        for idx, page in enumerate(page_sections, start=1):
            draw_page(pdf, title, page, idx)

    print(f"Wrote {WRITEUP_PDF}")


if __name__ == "__main__":
    main()
