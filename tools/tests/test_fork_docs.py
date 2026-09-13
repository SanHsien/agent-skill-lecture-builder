from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_links
import check_upstream_updates as checker

ROOT = Path(__file__).resolve().parents[2]


def test_maintainer_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_required_overlay_files_exist() -> None:
    required = (
        "README.md",
        "README.en.md",
        "FORK.md",
        "NOTICE.md",
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "REVIEW.md",
        "docs/DEVELOPMENT.md",
        "docs/DECISIONS.md",
        "docs/UPSTREAM.md",
        "tools/dev_check.ps1",
        "tools/bootstrap_dev.ps1",
        "tools/test_product.ps1",
        "requirements-dev.txt",
        "package.json",
        "LICENSE",
    )
    missing = [name for name in required if not (ROOT / name).is_file()]
    assert missing == []


def test_readme_pair_cross_links_and_names_the_fork() -> None:
    zh = (ROOT / "README.md").read_text(encoding="utf-8")
    en = (ROOT / "README.en.md").read_text(encoding="utf-8")
    assert "README.en.md" in zh
    assert "README.md" in en
    assert "deancourse/agent-skill-lecture-builder" in zh
    assert "deancourse/agent-skill-lecture-builder" in en
    assert "FORK.md" in zh
    assert "ISC" in zh
    assert "tools\\bootstrap_dev.ps1" in zh or "tools/bootstrap_dev.ps1" in zh


def test_gitignore_covers_user_data_and_reports() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in text
    assert ".venv" in text
    assert "upstream-review-report.md" in text
    assert "dependency-freshness-report.md" in text


def test_review_snapshot_has_required_sections() -> None:
    text = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    assert "## 結論" in text
    assert "## 已修 findings" in text
    assert "## 接受、不改契約" in text
    assert "## 尚未宣稱範圍" in text


def test_ci_covers_windows() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert '"3.14"' in workflow
    assert "windows / py" in workflow
    assert "tools/dev_check.ps1" in workflow or "tools\\dev_check.ps1" in workflow
    assert "ubuntu" not in workflow


def test_baseline_file_is_valid_and_complete() -> None:
    baseline = checker.load_baseline()
    assert baseline["repo"] == "https://github.com/deancourse/agent-skill-lecture-builder.git"
    assert baseline["branch"] == "main"
    assert len(baseline["reviewed_through"]) == 40
    assert baseline["reviewed_through"] == "43642998afe9291098b0e3ad3a309499bb82f60e"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", baseline["reviewed_date"])
    assert isinstance(baseline["reviewed_pr_through"], int)
    assert isinstance(baseline["reviewed_issue_through"], int)


def test_workflow_is_scheduled_and_fails_on_unreviewed_commits() -> None:
    workflow = (ROOT / ".github" / "workflows" / "upstream-check.yml").read_text(
        encoding="utf-8"
    )
    assert "cron:" in workflow
    assert "--strict" in workflow
