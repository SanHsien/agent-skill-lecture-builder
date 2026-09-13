# Repository review（Windows-only）

- Review date: 2026-09-12
- Review baseline: `43642998afe9291098b0e3ad3a309499bb82f60e`
- Remediation: 同日 fork-local overlay（不回貢）
- Upstream reviewed through: `43642998afe9291098b0e3ad3a309499bb82f60e`
- Primary environment: Windows 11、PowerShell、Node.js v26.7.0、Python 3.14.7（本機 gate）
- Status: 維護骨架與產品相依環境全面可用。已完成建立 Windows 原生門禁與驗收。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 Lecture Builder 線。產品行為跟隨 `deancourse/agent-skill-lecture-builder` `4364299`，再加上本線維護骨架：繁體中文維護文件、Windows 原生 1-click gate、純 Windows 原生維護 CI、每週上游水位追蹤（commit、PR、issue）以及每月依賴新鮮度檢查。

本 repo 的維護依賴（`pytest`, `ruff`）與 Node.js 執行環境皆已完整梳理並通過 Windows 原生環境驗證。在 Windows 環境下執行腳本時，門禁與工具腳本全面注入 `$env:PYTHONUTF8 = "1"`，避免預設 ANSI/CP950 編碼解碼 UTF-8 文件失敗。

## 本輪實證

### 審查當下（`4364299`）

```text
git rev-parse HEAD
→ 43642998afe9291098b0e3ad3a309499bb82f60e

gh repo set-default --view
→ SanHsien/agent-skill-lecture-builder
```

實查結果：
- 上游 repository 為 `deancourse/agent-skill-lecture-builder`，採 ISC License。
- 上游 PR 水位為 `#0`，Issue 水位為 `#0`。
- 上游未配置 GitHub Actions workflows，本 fork 建立了純 Windows 原生 CI 工作流程。
- 維護工具無 `os.system`／`shell=True`／`eval(`／`exec(`。

## 已修 findings

| ID | 嚴重度 | 做了什麼 |
|---|---|---|
| R-01 | P2 | `.gitignore` 加入 `.env`、`.venv`、`upstream-review-report.md`、`dependency-freshness-report.md`、`.ruff_cache/`、`.pytest_cache/` |
| R-02 | P2 | 建立獨立維護測試目錄 `tools/tests/` 與獨立 `tools/pytest.ini`，隔離維護測試 |
| R-03 | P2 | 建立 `FORK.md`、`NOTICE.md`、`LICENSE`、`SECURITY.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`，寫明對外邊界與安全性 |
| R-04 | P3 | `README.md`（繁體中文）與 `README.en.md`（英文鏡像）雙向互指，並標明 upstream 與 ISC 條款 |
| R-05 | P2 | 建立 `tools/dev_check.ps1` 與 `tools/bootstrap_dev.ps1`，規範 Windows 11 原生 PowerShell 驗收門禁 |
| R-06 | P2 | 建立 `tools/test_product.ps1` 驗證腳本語法檢驗與課程頁實際建置完整度 |
| R-07 | P2 | 建立純 Windows 原生 CI（`ci.yml`、`codeql.yml`、`upstream-check.yml`、`dependency-freshness.yml`） |
| R-08 | P2 | 健全範例課程目錄 `example/`：補齊 `content.md` 與 `config.yaml`，解決 `npm run build:example` 開箱缺少 `content.md` 報錯缺陷 |
| R-09 | P2 | Windows 路徑 URL 相容性硬化：在 `build.mjs` 中對 `coursePath` 加入反斜線正規化，避免 Windows 路徑反斜線破壞 SEO/OG 網址 |

## 接受、不改契約

| ID | 嚴重度 | 處理 |
|---|---|---|
| - | - | （無。所有已識別項目皆已妥善處理完畢） |

## 尚未宣稱範圍

- **不宣稱** 已將任何修改提交回原作者上游（依 fork 維護政策，所有 PR/commit 僅限於 `SanHsien/agent-skill-lecture-builder`）。
