# 維護決策

## 2026-09-12：建立 Windows-first 維護型 fork

**決定**：fork `deancourse/agent-skill-lecture-builder`，保留 ISC License 與完整歷史。本線預設分支用 `main`。本線聚焦繁中文件、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：`agent-skill-lecture-builder` 是一套優質的講稿轉單頁 HTML 課程網頁工具與 Agent Skill。本 fork 補足 Windows 11 原生開發／驗收骨架、繁體中文維護入口，以及可審計的上游追蹤機制。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者 Dean Lin 與官方連結。
- 不發佈第三方套件取代官方管道。
- 維護 gate 不預設安裝重型套件。
- 上游更新必須逐筆審查。

## 2026-09-12：依賴新鮮度追蹤

**決定**：`tools/check_dependency_freshness.py` 納管 `requirements-dev.txt` 與相關依賴。

**理由**：維護依賴（`pytest`, `ruff`）與產品可選套件納入每月新鮮度檢查以確保相容性。

## 2026-09-12：上游檢查涵蓋 Commit、PR 與 Issue 三面向

**決定**：`check_upstream_updates.py` 以 `--state all` 收集上游 PR 與 Issue，並追蹤 Commit SHA。`gh` 失敗時 fail closed（exit 2）。

**理由**：未合併即關閉的 PR 與待處理的 Issue 同樣可能揭露重要缺陷或需求。排程報告必須確保「未檢查」與「沒有新變更」截然分明。

## 2026-09-12：日常直接推 main

**決定**：日常維護修改在本機跑 `tools\dev_check.ps1` 後直接推 `origin/main`。Dependabot 與外部貢獻仍走 PR，合併前讀 diff。

**理由**：對齊 SanHsien 體系其他維護 fork 的治理規範。

## 2026-09-12：上游分支、PR 與 Issue 首次盤點結論

**決定**：
1. **上游分支**：上游有 `main` 與 `develop`，但 `develop` 僅包含相同的提交內容與 lock 檔，本 fork 唯一長期跟隨分支為 `upstream/main`，清理 origin 上的 `develop` 暫存分支。
2. **上游 PR 與 Issue**：當前上游無任何歷史 PR 與 Issue。
3. **水位鎖定**：`tools/upstream_baseline.json` 鎖定 Commit `43642998afe9291098b0e3ad3a309499bb82f60e`、PR 水位 `0`、Issue 水位 `0`。

**理由**：
- 確立乾淨的審查基準線，增量檢查未來僅需處理大於 `#0` 的新項目或 `4364299` 之後的新 Commit。

## 2026-09-12：Windows 路徑與 URL 標準化硬化

**決定**：在 `build.mjs` 中的 `coursePath` 計算加入正斜線替換 `.replace(/\\/g, '/')`，確保在 Windows 環境下產出的 SEO 網址（如 `https://user.github.io/repo/example/`）不會帶有反斜線。

**理由**：Windows 的 `path.relative` 會產生帶有反斜線的路徑，直接拼入 URL 會破壞 Open Graph 與 SEO meta tag 標準。

## 2026-09-12：健全範例目錄 `example/`

**決定**：在 `example/` 補齊 `content.md` 與 `config.yaml`，保留原始 `README.md`。

**理由**：上游在 `package.json` 中配置了 `"build:example": "node .agents/skills/course-page-generator/scripts/build.mjs example"`，但目錄下缺少 `content.md`，導致開箱直接報錯。補齊後讓使用者與本機門禁能直接一鍵驗收產品生成能力。
