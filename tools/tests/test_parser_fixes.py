import subprocess
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_SCRIPT = REPO_ROOT / ".agents" / "skills" / "course-page-generator" / "scripts" / "build.mjs"
BASE_CONFIG = REPO_ROOT / "config" / "global.yaml"


def run_build(course_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["node", str(BUILD_SCRIPT), str(course_dir)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_youtube_block_and_single_line_parsing():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        content_md = """# 單元測試：YouTube 語法驗證
> 測試各種 YouTube 標籤解析

## 第一節：影片測試

[youtube id="single_vid" title="單行標題影片"]

[youtube id="block_vid"]
這是區塊形式的多行
詳細說明文字。
[/youtube]

[youtube id="inline_vid"]單行閉合說明[/youtube]

[/youtube]
"""
        (tmp_path / "content.md").write_text(content_md, encoding="utf-8")
        (tmp_path / "config.yaml").write_text(
            "page:\n  title: 'YouTube Test Page'\n",
            encoding="utf-8",
        )

        res = run_build(tmp_path)
        assert res.returncode == 0, f"build failed: {res.stderr}\n{res.stdout}"

        out_html = (tmp_path / "index.html").read_text(encoding="utf-8")

        # 1. Single-line embed verification
        assert 'src="https://www.youtube.com/embed/single_vid"' in out_html
        assert "單行標題影片" in out_html

        # 2. Block-form embed verification
        assert 'src="https://www.youtube.com/embed/block_vid"' in out_html
        assert "這是區塊形式的多行 詳細說明文字。" in out_html

        # 3. Inline closed form verification
        assert 'src="https://www.youtube.com/embed/inline_vid"' in out_html
        assert "單行閉合說明" in out_html

        # 4. Critical check: [/youtube] must NEVER leak into rendered HTML
        assert "[/youtube]" not in out_html
        assert "<p>[/youtube]</p>" not in out_html


def test_defensive_block_boundaries_on_unclosed_tags():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        content_md = """# 單元測試：邊界防禦
> 測試未閉合區塊不跨越章節

## 第一節：未閉合流程

[flow]
1. 步驟一 — 建立專案
2. 步驟二 — 撰寫測試

## 第二節：第二章節正常呈現

### 測試卡片
- 卡片項目一
- 卡片項目二
"""
        (tmp_path / "content.md").write_text(content_md, encoding="utf-8")
        (tmp_path / "config.yaml").write_text(
            "page:\n  title: 'Boundary Test Page'\n",
            encoding="utf-8",
        )

        res = run_build(tmp_path)
        assert res.returncode == 0, f"build failed: {res.stderr}\n{res.stdout}"

        out_html = (tmp_path / "index.html").read_text(encoding="utf-8")

        # Section 2 must be rendered and not swallowed
        assert "第二節：第二章節正常呈現" in out_html
        assert "測試卡片" in out_html
        assert "卡片項目一" in out_html
