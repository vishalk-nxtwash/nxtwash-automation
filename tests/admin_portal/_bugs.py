"""Expose the ``docs/bug_reports.md`` sections as strings for Allure.

Tests attach these as ``@allure.description(...)`` so the bug write-up renders
inside the Allure report (test detail) instead of living only in a markdown file.
Single-sourced from the doc so the two never drift.
"""
import os

_DOC = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "bug_reports.md"
)


def _section(title_contains):
    """Return the '## ...' section of bug_reports.md whose heading matches."""
    try:
        with open(os.path.abspath(_DOC), encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return "See docs/bug_reports.md (%s)" % title_contains

    sections = text.split("\n## ")
    for section in sections[1:]:
        if title_contains.lower() in section.splitlines()[0].lower():
            return "## " + section.strip()
    return "See docs/bug_reports.md (%s)" % title_contains


BUG1 = _section("BUG 1")
BUG2 = _section("BUG 2")
