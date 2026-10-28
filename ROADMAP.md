# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `a6dc5c079c00` 查的快照，開工前先重查 GitHub。

## 現況

這是 deancourse/agent-skill-lecture-builder（由 Markdown 講稿生成單頁 HTML 課程的 Agent Skill）的 Windows 原生維護 fork。維護面健康：`main` 上 CI、CodeQL、Dependency freshness、Upstream check 最近一次皆 success，open PR 0 筆、Dependabot 與 Code scanning 告警 0 筆；issue 功能已停用，issue 數「未查到」不是 0；遠端只剩 `main` 一條分支（2026-10-29 `gh api repos/SanHsien/agent-skill-lecture-builder/branches` 查詢）。上游最後 push 2026-04-12，水位 `reviewed_through` 為 `43642998afe9` 即上游最新 commit（`tools/upstream_baseline.json`），無待審項目。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 移除或改寫已過時的 `HANDOFF.md` | 它寫於 2026-09-27，仍把 PR #5 的 CodeQL TOCTOU 列為「待處理」並記著舊本機路徑；PR #5 已合併、CodeQL 現為 success，留著會誤導接手者 | `HANDOFF.md` 刪除（歷史在 git log），或只留指向本檔的一行；`rg "HANDOFF" -g "*.md"` 無懸空連結；`tools\dev_check.ps1` 綠（含連結檢查） | Claude Haiku | `HANDOFF.md`；`REVIEW.md` R-10；2026-10-29 `gh` 查詢：CodeQL success |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 審上游新 commit／PR／issue 並推進水位 | `Upstream check` workflow 轉 failure，或上游 `main` 出現 `43642998afe9` 之後的 commit | 結論記入 `docs/DECISIONS.md`；`tools/upstream_baseline.json` 水位推進；`python tools/check_upstream_updates.py --strict` exit 0；`tools\dev_check.ps1` 與 `tools\test_product.ps1` 綠 | Claude Sonnet | `tools/upstream_baseline.json`；`docs/UPSTREAM.md:46-52` |
| 審上游 `develop` 分支內容 | 上游把 `develop` 合進 `main`（屆時隨 `main` 審查）；baseline 只追 `main` | 合併後的 commit 依上一列流程審完 | Claude Sonnet | `docs/DECISIONS.md:37`；`docs/UPSTREAM.md:51` |
| 取消 ruff 延後、提高下限 | ruff 出現高於延後清單 `deferredLatest` 的新版（延後自動失效）或 CI 開始執行 ruff 規則之外的 lint | `.github/dependency-deferrals.json` ruff 條目移除或更新；`check_dependency_freshness.py --strict` exit 0；CI 綠 | Codex | `.github/dependency-deferrals.json`；`requirements-dev.txt` |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 改動上游的 `build.mjs` 等產品程式（除已記錄的路徑正規化與 YouTube lookahead 修正） | 以上游為準，fork 只加最小修正（`REVIEW.md` R-09、R-10） | 上游停止維護且維護者決定接手產品 |
| 讓 `[t](my file.md)` 這類無角括號含空白的連結通過連結檢查 | CommonMark 不視為連結，檢查器不處理是正確行為 | CommonMark 規範改變 |
| 對上游開 PR／回貢 | 依 fork 維護政策只打 `SanHsien/` 名下（`REVIEW.md`「尚未宣稱範圍」） | 維護者在新的對話中明確要求回貢 |

## 維護方式

fork：以 `Upstream check` workflow 為訊號（failure＝上游有未審項目），上游目前很安靜（最後 push 2026-04-12），審完在 `docs/DECISIONS.md` 記採用與否並推進水位。Dependabot 只開 PR，CI 綠且讀完 diff 才合併；puppeteer 等 npm 依賴由 Dependabot 驅動。
