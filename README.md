# HKU + Harvard History 全課程 自學

**Vault / Git Repo Navigation Hub**

> 目標：系統性自學 HKU 46 門 + Harvard Foundations 18 門 + Fall 28 門 history 課程,真正理解每個 course 嘅核心心智模型、根本分歧、深度問題,結合袁騰飛式犀利風格。

**注意**: 每個 course 嘅真正 self-study 為目標,**唔預設特定應用**。讀史嘅目的係理解,唔係工具化。

---

## 目前狀態 (2026-08)

- 92 個 course files 全部符合袁騰飛格式 (5MM/3DG/10Q/5DD/10SL/5MR)
- Multi-agent pipeline 框架已建立 (`_agents/` 5 個 agent)
- HIST1017 demo: 9 個真實學者 + 50+ 真實事件 + 20+ 真實數字
- 其他 91 個 courses 仲係 template-driven,等逐個 course 真正 research 重寫

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

## 每門課統一產出格式（袁騰飛風格）

1. **5個核心心智模型**（What are the 5 core mental models every expert shares?）
2. **3個根本分歧點**（3 places experts fundamentally disagree + strongest arguments）
3. **10個深度理解問題**（Generate 10 questions that expose deep understanding vs memorization）

---

## Git 使用建議

```bash
./git-auto.sh "你的 commit 訊息"
```

單打獨鬥也要有系統。這個 repo 就是你的歷史自學根據地。
