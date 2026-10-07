# 01：思維轉變：從傳統 PPT 到 Vibe Coding
> 講授 AI 寫程式，何不直接用 AI 打造專屬的講義網站？打破傳統簡報框架，邁向量身打造的自訂介面。

## 傳統簡報 vs. 個人化講義網站

### 🔧 為什麼不用傳統 PPT？
- 傳統投影片版面受限，無法完美展示長篇程式碼與即時範例
- 網頁講義具備跨裝置瀏覽能力（電腦、平板、手機皆自適應）
- 支援一鍵匯出乾淨的 PDF 列印格式
- 可透過 CSS 與動態元件量身打造日系美感與閱讀體驗

### 🎯 培養多個 AI Agent 交替使用的能力
- 不迷信特定單一模型或工具，因為最強 AI 不斷更迭
- 重點在於解決痛點的系統思維，而非工具本身
- 避免長期綁定高額年約，保持技術棧靈活切換的能力

[tags]
blue: Vibe Coding
purple: 系統思維
orange: 跨裝置體驗
green: 自適應設計
[/tags]

---

# 02：環境準備與 Codex 終端機實戰
> 搭建輕量開發環境，在命令列透過 Prompt 生成第一個網頁原型。

## 開發工具與執行環境

### 📦 安裝 Node.js 與 Codex
- 推薦透過 NVM 管理 Node.js 版本，避免版本衝突
- 使用 npm 全域安裝 OpenAI Codex CLI

```prompt [label="安裝指令"]
npm i -g @openai/codex
codex
```

- 登入方式支援 ChatGPT 帳號、裝置代碼授權或自備 API Key

### 💻 在終端機生成初版講義
- 明確目標：純單一 HTML 檔案，降低部署與分發門檻
- 指定風格：簡約日系質感、側邊欄導覽與發人深省的開場引言
- 階層化架構：卡片、列表、流程圖與社群連結

> **痛點發現：直接生成 HTML 的維護瓶頸**
> 追求細節時，直接修改 AI 產生的巨大 HTML 容易陷入混亂；讓 AI 重寫整頁又可能破壞原有良好設計。解法是將「內容」與「表現」解耦。

---

# 03：系統架構與 Agent Skill 封裝
> 從免洗式生成到工程化複用：將模板與 Markdown 講稿徹底解耦。

## 打造可持續維護的 Skill

### ⚙️ 三層式設計架構

[flow]
1. 內容層（content.md）— 純 Markdown 撰寫講稿與結構化標籤
2. 設定層（config.yaml）— 覆蓋主題、講師資訊與 SEO metadata
3. 渲染層（build.mjs）— 零外部依賴 Node.js 將講稿編譯為單頁 HTML
[/flow]

### 🚀 零依賴 Node.js 建置與熱重載

```prompt [label="建置指令"]
node .agents/skills/course-page-generator/scripts/build.mjs example
node .agents/skills/course-page-generator/scripts/dev.mjs example --port 3000
```

- `dev.mjs` 透過原生 SSE 提供存檔即時熱重載（Live Reload）
- 自動搜尋全域與課程設定（Deep Merge）
- 圖片資源自動嵌入 base64，達成 100% 離線單檔交付

---

# 04：總結
> 將 Vibe Coding 的快速探索與軟體工程的嚴謹度結合，創造長期複用的高價值工具。

## 核心收穫

[summary]
- **擺脫免洗思維**：不只用 AI 生成一次性程式碼，更要思考長期維護架構
- **內容表現分離**：Markdown 專注文本邏輯，HTML/CSS 模板守護版面美感
- **Agent Skill 賦能**：封裝流程後，未來只需提供講稿大綱即可一鍵出稿
[/summary]

[bonus title="🎁 講者幕後心得"]
打造個人化工具最迷人的地方，在於解決自己切身痛點的成就感。
當你把講義網頁做成可複用的 Agent Skill 後，每次備課的時間直接節省 80% 以上！
期待大家也動手打造屬於自己的工作流 Skill！
[/bonus]
