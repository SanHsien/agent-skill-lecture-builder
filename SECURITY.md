# 安全政策

## 支援範圍

安全修正以本 fork 的最新 `main` 為主；上游版本的問題也會視需要回報原作者。

## 私下回報

若發現針對本 fork 維護骨架或衍生程式的安全漏洞，請使用 GitHub Security Advisories 的 **Report a vulnerability** 私下回報：
<https://github.com/SanHsien/agent-skill-lecture-builder/security/advisories/new>。
若該入口不可用，請透過 GitHub 個人檔案聯絡維護者，不要先建立公開 Issue。

若問題屬於上游核心邏輯，亦可向原作者 deancourse 通報。

回報請包含影響範圍、重現步驟、受影響版本與最小必要證據。請勿在回報中附上真實 API key、token、個人機密文件或帳密。

## 特別注意

- **路徑防護**：`build.mjs` 與 `dev.mjs` 會根據使用者輸入之路徑讀取與寫入檔案。請防範路徑遍歷與非預期目錄覆寫。
- **HTML 跳脫防護**：Markdown 轉 HTML 過程中，應對不信任字串與 YAML 欄位進行 `html.escape`，避免潛在 XSS 漏洞。
- **本專案範圍**：不要將真實個人資料、含憑證的設定檔或 API key 提交進 repository。
