# HKU + Harvard History 全課程 自學

**Vault / Git Repo Navigation Hub**

> 目標：系統性自學 HKU 46 門 + Harvard Foundations 18 門 + Fall 28 門 history 課程,真正理解每個 course 嘅核心心智模型、根本分歧、深度問題,結合袁騰飛式犀利風格。

**注意**: 每個 course 嘅真正 self-study 為目標,**唔預設特定應用**。讀史嘅目的係理解,唔係工具化。

---

## 目前狀態 (2026-08)

- 92 個 course files 全部符合袁騰飛格式 (5MM/3DG/10Q/5DD/10SL/5MR)
- Multi-agent pipeline 框架已建立 (`_agents/` 5 個 agent)
- HIST1017 demo: 9 個真實學者 + 50+ 真實事件 + 20+ 真實數字
- 91 個 courses 已擴展到 349-363+ lines (hku-fix1/2/3 cascade)
- Weak files 已用真實 web research 重寫

---

## 資料夾結構

```
HKU-Harvard-History-Self-Study/
├── 00_大綱/                          # 總覽、計劃、模板
├── 01_HKU_Courses/                   # HKU 46 門
├── 02_Harvard_Courses/
│   ├── 101_Foundations/              # 18 門核心（優先）
│   └── Fall_Courses/                 # 28 門 Fall 課程
├── 03_袁騰飛講義/
├── 05_Digital_History_Tools/
├── 06_Reading_Notes/                 # 中英對照筆記 + 深度問答
├── 07_Outputs_MPhil_Portfolio/
└── _agents/                          # Multi-agent pipeline 框架
    ├── researcher/
    ├── data_extractor/
    ├── analyst/
    ├── diagram/
    ├── professor_supervisor/
    └── _pipeline/
```

---

## 核心文件

| 文件 | 用途 |
|------|------|
| `00_大綱/05_全課程列表.md` | 完整課程清單（含優先級） |
| `06_Reading_Notes/Phase1_深度問答總表.md` | Phase 1 七門核心課的 5心智模型 + 3分歧 + 10深度問題 |
| `_agents/` | 5 個 agent pipeline (Researcher/Data/Analyst/Diagram/Professor) |

---

## 📂 課程格式 — 袁騰飛格式 (5MM / 3DG / 10Q / 5DD / 10SL / 5MR)

每一個 course file 都係用 **袁騰飛格式** 寫成，呢個格式由袁騰飛老師嘅教學風格啟發 — 用紮實嘅史料 + 嚴密嘅邏輯結構，取代一般嘅 template 填空。

### 🧱 結構組成

| 元素 | 數量 | 內容 | 範例 (HIST1017) |
|---|---|---|---|
| **5MM** | 5 | 核心心智模型 (Mental Models) — 歷史框架 + 真實事件 + 學者 | Annales School "longue durée" (Braudel 1958) |
| **3DG** | 3 | 根本分歧 (Divergent views) — A/B 兩方 + 引用 | Intentionalist vs Structuralist (Hobsbawm 1962 vs Mayer 1988) |
| **10Q** | 10 | 深度問題 (Questions) — 由淺入深 | "Why did 1789 happen?" |
| **5DD** | 5 | 深度 dive (中英對照) — 兩個 paragraph 講核心概念 | Industrial Revolution 嘅 demographic + economic dimensions |
| **10SL** | 10 | Solutions — 完整史料分析 + primary source interpretation | 1789 cahiers de doléances 嘅 socioeconomic breakdown |
| **5MR** | 5 | Mermaid 圖 — timeline / map / causal chain | `mermaid timeline` 1789-1815 |

### 🎯 核心原則

1. **真實史料 (No template)** — 唔用 placeholder、唔用 "[TBD]"、唔用 "Lorem ipsum"。每個事件、每個日期、每個學者都要查過 web。
2. **中英對照 (Bilingual)** — DD 段落、史料引用英中並列，方便香港雙語環境。
3. **學者真名 + 出版年份** — 例：Bloch 1924, Braudel 1958, Hobsbawm 1962, Thompson 1963, Anderson 1983 — 唔寫 "some historians say"。
4. **Primary sources 第一手** — 每個 SL 都有 direct quote / document reference (e.g. cahiers de doléances, 1789)
5. **Mermaid timeline 必須 render** — 唔寫爛 syntax，要直接喺 GitHub 渲染得到 (timeline / flowchart / stateDiagram)

### 🛠️ Course Generation Pipeline

History 課程生成嘅 setup：

```
┌─────────────────────────────────────────┐
│  1. Web Research (per course)           │
│     - Wikipedia / Britannica            │
│     - Scholarpedia / JSTOR             │
│     - HKU/Harvard official syllabus    │
│     - Real historians + dates           │
│     - Primary sources (archives)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Multi-agent pipeline (_agents/)     │
│     - researcher: gather sources        │
│     - data_extractor: pull dates/people │
│     - analyst: build 5MM + 3DG         │
│     - diagram: build 5 Mermaid charts  │
│     - professor_supervisor: verify     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Outline 5MM/3DG/10Q/5DD/10SL/5MR    │
│     - Map topics → each section         │
│     - Identify 5 mental models          │
│     - Find 3 historiographical debates │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Write bilingual content             │
│     - Each DD: EN paragraph + 中文      │
│     - Each SL: source + analysis + 中文 │
│     - Citations inline (Author Year)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  5. Mermaid diagrams (history-specific) │
│     - timeline (chronology)             │
│     - flowchart (causal chain)          │
│     - stateDiagram (periods)            │
│     - classDiagram (historiography)     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  6. Verify & Push                       │
│     - All names have year + work        │
│     - No "[TBD]", no template placeholders │
│     - Mermaid renders on GitHub         │
│     - git commit + push                 │
└─────────────────────────────────────────┘
```

### 🤖 Multi-Agent Architecture (`_agents/`)

```
_agents/
├── researcher/            # Step 1: Web search, primary/secondary sources
│   ├── web_search.py
│   ├── scholar_lookup.py
│   └── source_dedupe.py
├── data_extractor/        # Step 2: Extract dates, people, places, numbers
│   ├── date_parser.py
│   ├── entity_extractor.py
│   └── fact_table.py
├── analyst/               # Step 3: Build 5MM + 3DG from facts
│   ├── mental_model.py
│   ├── divergence.py
│   └── question_generator.py
├── diagram/               # Step 4: Generate 5 Mermaid diagrams
│   ├── timeline.py
│   ├── flowchart.py
│   ├── state_diagram.py
│   └── render_check.py
├── professor_supervisor/  # Step 5: Quality gate (real names, real dates)
│   ├── citation_check.py
│   ├── placeholder_scan.py
│   └── rubric.py
└── _pipeline/             # Orchestrator
    ├── run_course.py      # one-course-at-a-time
    ├── batch.py           # multi-course parallel
    └── hku_history.yaml   # 92 courses config
```

### 📏 Quality Bar

- ❌ **拒絕**: Template 填空、`[TBD]`、`待補充`、generic paragraphs
- ❌ **拒絕**: "Some historians believe..." 含糊 attribution
- ❌ **拒絕**: Pseudocode / placeholder URLs
- ✅ **接受**: Real historians (Bloch 1924, Braudel 1958, Hobsbawm 1962, Thompson 1963, Anderson 1983, Tilly 1990)
- ✅ **接受**: Specific dates + places (1789-07-14, Bastille, Paris)
- ✅ **接受**: Primary source quotes (cahiers de doléances, Manifesto 1848)
- ✅ **接受**: Bilingual DD (EN + 中文)
- ✅ **接受**: 5 Mermaid diagrams per course (timeline + flowchart + stateDiagram)

### 🧪 Verification (per course)

```bash
# 1. Check file size (should be 349+ lines)
wc -l 01_HKU_Courses/HIST1017.md
# 2. Count historians (should have real names + year)
grep -E "(Bloch|Braudel|Hobsbawm|Thompson|Anderson|Tilly|von Ranke)" 01_HKU_Courses/HIST1017.md | wc -l
# 3. Validate Mermaid syntax
grep -c '```mermaid' 01_HKU_Courses/HIST1017.md  # should be 5
# 4. Check no placeholder text
grep -E "\[TBD\]|待補充|Lorem|placeholder" 01_HKU_Courses/**/*.md  # should be empty
# 5. Multi-agent pipeline
python3 _agents/_pipeline/run_course.py --course HIST1017 --verify
```

---

## Git 使用建議

```bash
./git-auto.sh "你的 commit 訊息"
```

單打獨鬥也要有系統。這個 repo 就是你的歷史自學根據地。
