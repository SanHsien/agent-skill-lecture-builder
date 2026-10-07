# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/agent-skill-lecture-builder.git`（預設分支 `main`）
- 原作者：`upstream` → `https://github.com/deancourse/agent-skill-lecture-builder.git`（預設分支 `main`）
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交、PR 與 Issues。
有新變更或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確亮紅燈提醒。

CI 沒有 `upstream` remote，所以 baseline 的 `repo` 寫完整 clone URL，不要寫遠端短名。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題結案）。
2. 判斷是否與繁中 README、Windows gate、發佈閘門或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 `docs/DECISIONS.md` 記錄採用／略過理由。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA 與更新 PR/Issue 水位。

Baseline 代表「已審查」，不代表「全部已合併」。

## 2026-09-12：fork 起點

本 fork 自上游 `main` `43642998afe9291098b0e3ad3a309499bb82f60e`
（`docs: expand README.md with practical insights on Vibe Coding and a structured course outline`）建立。
此 SHA 設為第一個 `reviewed_through`（短 SHA 為 `4364299`）。
之後的上游 commit 才需要進入審查清冊。

---

## 2026-09-12：上游 PR、Issue、分支全面盤點

2026-09-12 對 [`deancourse/agent-skill-lecture-builder`](https://github.com/deancourse/agent-skill-lecture-builder) 進行完整盤點：
**2 個分支（main、develop）、0 個 PR、0 個 Issue**。
評估結論如下，記錄於本檔與 [`docs/DECISIONS.md`](DECISIONS.md)，避免未來重複評估。

### 一、上游分支盤點

上游包含 `main` 與 `develop`，但 `develop` 僅包含相同的提交內容與 lock 檔。
本 fork **唯一長期跟隨分支為 `upstream/main`**，本 fork 的 `origin` 刪除 `develop` 分支以維持單一分支簡潔。

### 二、上游 PR 與 Issue 盤點

當前無任何待處理之 Open 或 Closed PR / Issue。

### 三、防重複評估機制（Watermark 機制）

為避免每次巡檢重複評估既有項目，本專案實施嚴格的水位線（Watermark）機制：

1. **基準水位鎖定**：
   - Commit 水位：`43642998afe9291098b0e3ad3a309499bb82f60e`（短 SHA `4364299`）
   - PR 水位：`0`
   - Issue 水位：`0`
   - 記錄於 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。

2. **增量巡檢機制**：
   - 每次執行 `tools/check_upstream_updates.py` 或 GitHub Actions 每週排程時，檢查器會自動過濾 `number <= watermark` 的項目。
   - 只有編號大於 **#0** 的新開 PR / Issue，或 `main` 上高於 `4364299` 的新 Commit，才會出現在待審報告中。
   - 當新項目被審查完畢並於 `docs/DECISIONS.md` 記錄結論後，再遞增更新 baseline 水位。
