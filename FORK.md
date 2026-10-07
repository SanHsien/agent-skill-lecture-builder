# Fork 維護說明

本 repo fork 自 [`deancourse/agent-skill-lecture-builder`](https://github.com/deancourse/agent-skill-lecture-builder)，
沿用 ISC License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留原作者持續更新的 Markdown 講稿轉 HTML 課程網頁生成器與 Agent Skill。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口維持繁體中文為主，英文鏡像放 `README.en.md`。
- 建立可重現的 Windows 開發 gate、Windows CI job，以及逐筆審查的上游追蹤（涵蓋 commit、PR 與 issue 水位）。
- 產品執行路徑以上游為準；零外部依賴 Node.js 建置機制完全保留。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**
回貢前必須在當次對話取得維護者明確同意；「fork」「建開發環境」「開 PR」都不是同意。

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；加入 fork 維護資訊與快速入口 |
| `README.en.md` | 英文鏡像；加入 fork 維護資訊 |
| `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | 本 fork 的 AI 維護單一真相源 |
| `NOTICE.md` / `FORK.md` / `LICENSE` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate（維護工具語法、單元測試、相對連結檢查） |
| `tools/bootstrap_dev.ps1` | Windows 本機一鍵初始化與驗收環境 |
| `tools/test_product.ps1` | Windows 原生產品測試執行腳本（驗證語法檢查、example 課程頁建置與產出完整度） |
| `requirements-dev.txt` | Python 維護依賴清單（pytest、ruff） |
| `.github/workflows/ci.yml` | 純 Windows 原生 CI (windows-latest)：Node 腳本檢查 / Python 3.10–3.14 維護測試 / 連結檢查 / 產品實測 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit、PR、issue 水位檢查 |
| `.github/workflows/dependency-freshness.yml` | 每月依賴新鮮度檢查 |
| `.github/workflows/codeql.yml` | CodeQL 安全掃描工作流程 |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |
| `REVIEW.md` | 全庫風險快照 |

核心腳本在 `.agents/skills/course-page-generator/scripts/`、模板在 `reference/`，以上游為準。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常修改在本機跑 gate 後直接推 `origin/main`。
- `upstream/main`：deancourse 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/agent-skill-lecture-builder.git
cd agent-skill-lecture-builder
# 若尚未設定 upstream remote：
# git remote add upstream https://github.com/deancourse/agent-skill-lecture-builder.git
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

要實際使用課程頁建置工具與 Agent Skill，見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。
