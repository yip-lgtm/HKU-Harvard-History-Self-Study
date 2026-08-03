# Multi-Agent Pipeline for Course Content Generation

## 5 Agents
1. **Researcher** — Web search + fetch 找真學者、史料、events
2. **Data Extractor** — 抽取 timeline, people, numbers, places, sources, quotes
3. **Analyst** — 從 data 真正做 5 個 SPECIFIC 心智模型 + 3 SPECIFIC 根本分歧 + 10 PROBING 問題
4. **Diagram** — 5 個 Mermaid 圖,每個 SPECIFIC 到呢個 course
5. **Professor Supervisor** — 審稿 APPROVED/REVISE/REJECT

## Pipeline
`pipeline.py` 係 orchestrator,按順序 call 各 agent 處理 1 個 course。

## Demo
HIST1017 (Modern Hong Kong) 已用呢個 pipeline 重新生成,質素由 template-driven 變成 research-based:
- 9 個真實學者 (Ming K. Chan, John M. Carroll, Steve Tsang, etc.)
- 真實 events (1841.1.26, 1967 暴動, 1984.12.19, 1997.7.1, 2020.6.30, 2024.3.19)
- 真實 numbers (7,450 居民、51 死、832 傷、4,979 逮捕、156 年)
- 真實 books (Edge of Empires 2005, Pacific Crossing 2013, Democracy Shelved 2024)
