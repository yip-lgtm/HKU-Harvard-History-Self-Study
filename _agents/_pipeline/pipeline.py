#!/usr/bin/env python3
"""Multi-agent pipeline for course content generation.

For each course, runs:
1. Researcher — web search + fetch
2. Data Extractor — structure facts
3. Analyst — 5MM/3DG/10Q specific
4. Diagram — 5 real Mermaid diagrams
5. Professor Supervisor — review and approve/reject

Output: Final markdown file in 袁騰飛 format.
"""
import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime
import subprocess


AGENT_DIR = Path(__file__).parent.parent  # /workspace/agents
PIPELINE_DIR = Path(__file__).parent

# System prompts for each agent
RESEARCHER_SYS = (AGENT_DIR / "researcher" / "SYSTEM.md").read_text(encoding="utf-8")
DATA_SYS = (AGENT_DIR / "data_extractor" / "SYSTEM.md").read_text(encoding="utf-8")
ANALYST_SYS = (AGENT_DIR / "analyst" / "SYSTEM.md").read_text(encoding="utf-8")
DIAGRAM_SYS = (AGENT_DIR / "diagram" / "SYSTEM.md").read_text(encoding="utf-8")
PROFESSOR_SYS = (AGENT_DIR / "professor_supervisor" / "SYSTEM.md").read_text(encoding="utf-8")


def run_agent(agent_name: str, system_prompt: str, user_prompt: str, model: str = "sonnet") -> str:
    """Run a single agent via claude CLI.

    Falls back to manual prompt construction if no CLI available.
    """
    # Use the Mavis agent system via subprocess
    # Each agent has a system prompt + the user prompt
    pass


def build_researcher_prompt(course_code: str, course_name: str, institution: str) -> str:
    """Build the user prompt for the researcher agent."""
    return f"""請用以下步驟研究呢個 course:

**Course code**: {course_code}
**Course name**: {course_name}
**Institution**: {institution}

## 任務

1. 用 `web_search` 揾 "{course_code} {course_name} {institution}" 嘅 syllabus
2. 用 `web_fetch` 去官方頁面拎:
   - 真正嘅 course description
   - 真正嘅 reading list (學者 + 著作 + 年份)
   - 真正嘅 weekly topics
3. 揾呢個 course 嘅 5-10 個核心學者(中英對照)
4. 揾 5-10 個關鍵 primary sources(條約、演講、報紙、檔案)
5. 揾 10-15 個關鍵歷史事件(具體年月日)
6. 揾 5-10 個具體數字(人口、傷亡、面積等)
7. 揾 3-5 個關鍵爭論 + 兩邊學者

## 輸出 JSON

按 SYSTEM.md 嘅 schema 輸出,要有真 URL、真名、真日期。

## 重要

**唔好做 template-driven research**。例如「香港現代史」要搵到 Ming Chan, David Faure, John Carroll, 等等,而唔係 generic 「香港歷史學者」。

開始啦。"""


def build_data_prompt(course_code: str, researcher_json: str) -> str:
    return f"""從以下 researcher output 抽取結構化數據:

```json
{researcher_json}
```

按 SYSTEM.md schema 輸出 JSON:
- timeline: 至少 10 個事件,每個有準確年月日
- people: 5-10 個重要人物
- key_numbers: 5-10 個具體數字
- places: 5-10 個地方
- primary_sources_list: 5-10 個原始史料
- key_quotes: 3-5 個關鍵 quote (中英對照)

每個項目都要有 source URL。"""


def build_analyst_prompt(course_code: str, course_name_zh: str, course_name_en: str,
                          researcher_json: str, data_json: str) -> str:
    return f"""基於以下 researcher + data output,真正分析呢個 course:

**Course**: {course_code} - {course_name_zh} / {course_name_en}

**Researcher output**:
```json
{researcher_json}
```

**Data output**:
```json
{data_json}
```

## 任務:輸出 5 個 SPECIFIC 心智模型 + 3 個 SPECIFIC 根本分歧 + 10 個 PROBING 深度問題

**重要規則**:
- 唔可以用「現代性」、「權力」、「全球化」呢啲 generic 字
- 每個心智模型要有具體學者 + 具體事件
- 每個分歧要引用真實學者 + 真實著作 + 年份
- 每個問題要 probe 真實理解,唔可以係背書題

## 範例(好嘅分析,適用於 HIST1017)

### 心智模型 1:「自由港殖民地」嘅低稅收+低福利模式
- 1841 Pottinger 嘅 laissez-faire 政策 → 商業利益優先
- 1967 暴動後民政主任制度 → 維持低度管治
- 學者:Ming Chan (1991) Hong Kong: An Inexpensive Place at Any Price

### 分歧 1:1997 平穩過渡 — 成功典範 vs 畸形妥協
- A: Norman Miners (1987) — 平穩
- B: Lo Shiu-hing (2008) — 妥協

### 問題 1:
如果 Pottinger 1841 揀 Kowloon 而非 Hong Kong Island,後續發展會點?要答呢個問題要諗(1) 海軍戰略(2) 地質(3) 1841 清廷內部政治

## 你嘅輸出:

5 個 SPECIFIC 心智模型 + 3 個 SPECIFIC 根本分歧 + 10 個 PROBING 深度問題

用 Markdown 格式。"""


def build_diagram_prompt(course_code: str, course_name_zh: str,
                          researcher_json: str, data_json: str, analyst_md: str) -> str:
    return f"""基於以下 output 設計 5 個 Mermaid 圖:

**Course**: {course_code} - {course_name_zh}

**Analyst output**:
```
{analyst_md}
```

**Data output**:
```json
{data_json}
```

## 任務:5 個 Mermaid 圖,每個 SPECIFIC 到呢個 course

### 圖 1:Timeline — 真實時間線,至少 8 個事件,有準確年份
### 圖 2:Causal Chain — A → B → C 真實因果,每個箭頭有具體邏輯
### 圖 3:Network — 真實人物/組織網絡
### 圖 4:Decision Flow — 真實歷史轉折嘅 if-then
### 圖 5:Comparison — 對比 2-3 個時代/人物/概念,有具體 metric

## 規則
- 每個節點都要有真實內容(年份、人物、事件)
- 唔可以係 "A → B" 嘅 generic
- Mermaid 語法要 verify
- 用 Mermaid timeline, graph TD, flowchart, sequenceDiagram, mindmap 等

## 輸出
5 個獨立嘅 ```mermaid code blocks```,每個有 title。"""


def build_professor_prompt(course_code: str, course_name_zh: str,
                            final_md: str) -> str:
    return f"""扮演袁騰飛式嚴格歷史教授,審閱呢份 {course_code} 嘅 course file:

**Course**: {course_code} - {course_name_zh}

**File**:
```
{final_md}
```

## 審稿 checklist (按 SYSTEM.md)

### 1. 真實性 — 日期、人名、source URL 都真?
### 2. 深度 — 5MM/3DG/10Q 係 SPECIFIC 而非 generic?
### 3. 中英對照 — 真翻譯,非 copy?
### 4. 袁騰飛式 — 犀利有觀點?
### 5. 圖解 — 真實內容?
### 6. 結構 — 5MM/3DG/10Q/5DD/10SL/5MR/Closing 完整?

## 決策
- APPROVED:全部 pass
- REVISE:具體指出要改咩
- REJECT:要求重做

## 輸出 JSON
按 SYSTEM.md 嘅 schema 輸出 decision, score, issues, strengths, overall_comment。

如果係 REVISE 或 REJECT,必須指出**具體嘅修改方案**,唔可以係「再深入啲」嘅空泛 comment。"""


# === Orchestration ===

class CoursePipeline:
    """5-agent pipeline for one course."""

    def __init__(self, course_code: str, course_name_zh: str, course_name_en: str,
                 institution: str, output_path: Path):
        self.course_code = course_code
        self.course_name_zh = course_name_zh
        self.course_name_en = course_name_en
        self.institution = institution
        self.output_path = output_path
        self.researcher_output = None
        self.data_output = None
        self.analyst_output = None
        self.diagram_output = None
        self.professor_output = None
        self.final_md = None

    def run(self, max_rounds: int = 2) -> dict:
        """Run the full pipeline."""
        print(f"\n=== Processing {self.course_code} - {self.course_name_zh} ===\n")

        # Round 1: Run all 4 producer agents
        self.researcher_output = self._run_researcher()
        print(f"  [1/5] Researcher done: {len(self.researcher_output)} chars")

        self.data_output = self._run_data_extractor()
        print(f"  [2/5] Data Extractor done: {len(self.data_output)} chars")

        self.analyst_output = self._run_analyst()
        print(f"  [3/5] Analyst done: {len(self.analyst_output)} chars")

        self.diagram_output = self._run_diagram()
        print(f"  [4/5] Diagram done: {len(self.diagram_output)} chars")

        # Assemble final markdown
        self.final_md = self._assemble_markdown()
        print(f"  [5/5] Final markdown assembled: {len(self.final_md)} chars")

        # Round 2: Professor review
        for round_n in range(max_rounds):
            print(f"\n  --- Professor Review Round {round_n + 1} ---")
            self.professor_output = self._run_professor()
            decision = self._parse_decision()
            print(f"  Decision: {decision.get('decision', 'UNKNOWN')}")
            print(f"  Score: {json.dumps(decision.get('score', {}), ensure_ascii=False)}")

            if decision.get("decision") == "APPROVED":
                print(f"  ✅ APPROVED in round {round_n + 1}")
                break
            else:
                issues = decision.get("issues", [])
                print(f"  ⚠️  {len(issues)} issues found")
                if round_n < max_rounds - 1:
                    print(f"  Re-running producer agents with feedback...")
                    # In real implementation, would pass feedback to agents
                    # For now, we stop after one revise
                    break

        # Save final
        self._save()
        return {
            "course_code": self.course_code,
            "decision": decision.get("decision"),
            "final_md": self.final_md,
            "professor_review": decision,
        }

    def _run_researcher(self) -> str:
        # In real implementation, would call out to LLM via spawn or team
        # Here, we use the model itself with detailed prompt
        # For now, this is a placeholder that returns a JSON template
        # The actual agent invocation happens via mavis spawn or team tool
        return "{}"

    def _run_data_extractor(self) -> str:
        return "{}"

    def _run_analyst(self) -> str:
        return ""

    def _run_diagram(self) -> str:
        return ""

    def _run_professor(self) -> str:
        return "{}"

    def _parse_decision(self) -> dict:
        try:
            return json.loads(self.professor_output)
        except (json.JSONDecodeError, TypeError):
            return {"decision": "UNKNOWN", "score": {}}

    def _assemble_markdown(self) -> str:
        return ""

    def _save(self):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self.final_md or "", encoding="utf-8")


def demo_run():
    """Demo: Run pipeline on HIST1017 Modern Hong Kong."""
    course = CoursePipeline(
        course_code="HIST1017",
        course_name_zh="現代香港",
        course_name_en="Modern Hong Kong",
        institution="HKU",
        output_path=Path("/workspace/HKU-Harvard-History-Self-Study/01_HKU_Courses/HIST1017_Modern_Hong_Kong.md"),
    )
    result = course.run()
    print(f"\n=== Demo result: {result['decision']} ===")


if __name__ == "__main__":
    demo_run()
