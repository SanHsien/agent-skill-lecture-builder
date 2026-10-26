from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_links


@pytest.fixture()
def docs(tmp_path, monkeypatch):
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("x", encoding="utf-8")

    def check(markdown: str) -> list[str]:
        page = tmp_path / "page.md"
        page.write_text(markdown, encoding="utf-8")
        return check_links.check_document(page)

    return check


def test_link_title_is_not_part_of_the_path(docs) -> None:
    assert docs('[t](a.md "Title")') == []
    assert docs("[t](a.md 'Title')") == []


def test_query_string_is_not_part_of_the_path(docs) -> None:
    assert docs("[t](a.md?plain=1)") == []
    assert docs("[t](a.md?plain=1#frag)") == []


def test_missing_target_with_title_is_still_reported(docs) -> None:
    assert len(docs('[t](nope.md "Title")')) == 1


def test_longer_fence_is_not_closed_by_a_shorter_one(docs) -> None:
    text = "````\n```\n[x](nope.md)\n```\n````\n[ok](a.md)\n"
    assert docs(text) == []


def test_broken_image_is_reported_once(docs) -> None:
    assert len(docs("![i](missing.png)")) == 1
