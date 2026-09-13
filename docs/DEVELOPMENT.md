# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
.agents/
  └── skills/
      └── course-page-generator/
          ├── scripts/
          │   ├── build.mjs             純 Node.js ESM 課程頁建置器（零外部依賴）
          │   ├── dev.mjs               本機預覽伺服器與 SSE 熱重載
          │   └── generate-og.mjs       OG 縮圖產出器（依賴 Puppeteer）
          └── reference/
              ├── base.html             單頁課程 HTML 模板
              ├── components.md         組件與 Markdown 語法規範
              ├── config-example.yaml   課程設定範例
              └── content-example.md    課程講稿範例
config/
  ├── global.yaml                       全域設定（講者、社群、頁尾）
  └── assets/                           共用圖片資源
example/                                範例課程目錄
  ├── config.yaml                       課程專屬設定
  ├── content.md                        結構化講稿
  ├── README.md                         原始課程筆記
  └── index.html                        建置產出之單頁課程網頁
tools/                                  fork 維護工具（Windows gate、上游檢查、相對連結檢查、依賴新鮮度）
  └── tests/                            維護契約測試
docs/                                   fork 維護與治理文件
```

## 本機開發（Windows 11 原生）

### 維護骨架（必跑）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

等價一鍵指令：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

### 執行產品測試

本 repo 提供專用 Windows 原生產品測試腳本 `tools/test_product.ps1`：

```powershell
pwsh -NoProfile -File tools\test_product.ps1
```

腳本會：
1. 以 `node --check` 驗證所有 `.mjs` 腳本語法正確。
2. 執行 `node .agents/skills/course-page-generator/scripts/build.mjs example` 建置課程頁。
3. 驗證產出之 `example/index.html` 存在且非空，並包含預期 HTML 結構標籤。

## Canonical Gate

`tools\dev_check.ps1` 會依序執行：

1. `python -m compileall`（`tools`）
2. `ruff check`（E9 + F，僅檢查 `tools`）
3. `pytest tools/tests`（使用獨立的 `tools/pytest.ini`）
4. `python tools/check_links.py`（驗證所有維護文件相對連結）

CI 專注於 Windows 原生環境，在 `windows-latest` 執行 Python 3.10–3.14 矩陣並跑過 gate 與產品測試。推至 `main` 前請務必在本機跑過 gate。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 納管依賴清單。

紅燈只有兩條誠實的出口：

| 出口 | 寫在哪 | 什麼時候用 |
| --- | --- | --- |
| `# freshness-hold: <理由>` | `requirements-dev.txt` 行末 | 這個下限就是我們要的 |
| `.github/dependency-deferrals.json` 的 `deferredLatest` + `reason` | 獨立檔案 | 已看過、這個月不升；超過該版本會恢復提醒 |

不要用調高下限讓報告變綠。

## 不要做的事

- 不要提交含有個人憑證、API key 或敏感資訊的檔案。
- 不要把 PR 指向上游 `deancourse/agent-skill-lecture-builder`。
