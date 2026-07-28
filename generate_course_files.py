#!/usr/bin/env python3
"""
自動化課程檔案生成腳本
用途：為 HKU + Harvard History 自學專案批次產生標準深度問答模板
"""

import os
from pathlib import Path

# ==================== 課程清單 ====================
# 格式：(檔案路徑, 課程代碼, 課程名稱, 優先級, 備註)

COURSES = [
    # Harvard Foundations
    ("02_Harvard_Courses/101_Foundations", "GenEd1017", "Forced to Be Free: Americans as Occupiers and Nation-Builders", "★★★★★", "美國在亞洲的軍事佔領與 nation-building"),
    ("02_Harvard_Courses/101_Foundations", "GenEd1068", "The United States and China", "★★★★★", "中美關係與軍事對抗"),
    ("02_Harvard_Courses/101_Foundations", "Hist47", "The Cold War", "★★★★★", "冷戰亞洲熱戰與基地"),
    ("02_Harvard_Courses/101_Foundations", "Hist38", "Modern China: 1894–Present", "★★★★★", "中國近代被武器重塑的軌跡"),
    ("02_Harvard_Courses/101_Foundations", "Hist14", "The First World War", "★★★★☆", "現代武器時代開端"),
    ("02_Harvard_Courses/101_Foundations", "Hist68", "The 20th-Century United States", "★★★★☆", "美國成為全球軍事霸權"),
    ("02_Harvard_Courses/101_Foundations", "GenEd1206", "Asian Americans as an American Paradox", "★★★★", "亞裔與美國對亞政策的互動"),
    ("02_Harvard_Courses/101_Foundations", "Hist66", "The Coming of the Civil War", "★★★", "美國早期帝國擴張根源"),
    ("02_Harvard_Courses/101_Foundations", "GenEd1159", "American Capitalism", "★★★", "資本主義與軍事-工業複合體背景"),

    # HKU 高優先級
    ("01_HKU_Courses", "HIST1023", "Modern East Asia", "★★★★★", "現代東亞史"),
    ("01_HKU_Courses", "HIST1025", "Introduction to the United States, 1607 to today", "★★★★★", "美國從大陸擴張到全球投射"),
    ("01_HKU_Courses", "HIST2118", "Chinese and Americans: A cultural and international history", "★★★★★", "中美文化與國際關係史"),
    ("01_HKU_Courses", "HIST2127", "Qing China in the World, 1644-1912", "★★★★", "清代中國與世界"),
    ("01_HKU_Courses", "HIST2193", "A history of energy and humankind", "★★★★", "武器工業的能量基礎"),

    # Harvard Fall 高優先級
    ("02_Harvard_Courses/Fall_Courses", "Hist76", "The History of Energy", "★★★★", "能量與現代戰爭"),
    ("02_Harvard_Courses/Fall_Courses", "Hist1942", "The Second World War", "★★★★★", "二戰與美國全球軍事存在"),
    ("02_Harvard_Courses/Fall_Courses", "Hist137", "A History of Love: Modern South and Southeast Asia", "★★★★", "東南亞史"),
    ("02_Harvard_Courses/Fall_Courses", "GENED1136", "Power and Civilization: China", "★★★★", "中國權力與文明"),
]

# ==================== 模板 ====================

TEMPLATE = """# {code}
**{title}**

優先級：{priority}

> {note}

### 1. 5個核心心智模型 / 5 Core Mental Models

- （待填寫）

### 2. 3個根本分歧點 / 3 Fundamental Disagreements

- （待填寫）

### 3. 10個深度理解問題 / 10 Deep Understanding Questions

1. （待填寫）
2. （待填寫）
3. （待填寫）
4. （待填寫）
5. （待填寫）
6. （待填寫）
7. （待填寫）
8. （待填寫）
9. （待填寫）
10. （待填寫）
"""

def sanitize_filename(code: str, title: str) -> str:
    """產生乾淨的檔名"""
    safe_title = title.replace(":", "").replace("/", "-").replace("?", "").replace("*", "")
    safe_title = safe_title.replace(" ", "_")[:60]
    return f"{code}_{safe_title}.md"

def generate_files(overwrite: bool = False):
    created = 0
    skipped = 0

    for folder, code, title, priority, note in COURSES:
        Path(folder).mkdir(parents=True, exist_ok=True)
        filename = sanitize_filename(code, title)
        filepath = Path(folder) / filename

        if filepath.exists() and not overwrite:
            print(f"⏭  已存在，跳過：{filepath}")
            skipped += 1
            continue

        content = TEMPLATE.format(
            code=code,
            title=title,
            priority=priority,
            note=note
        )

        filepath.write_text(content, encoding="utf-8")
        print(f"✅ 已建立：{filepath}")
        created += 1

    print("\n========== 完成 ==========")
    print(f"新建立：{created} 個檔案")
    print(f"已跳過：{skipped} 個檔案")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="自動化生成課程深度問答模板")
    parser.add_argument("--overwrite", action="store_true", help="覆蓋已存在的檔案")
    args = parser.parse_args()

    generate_files(overwrite=args.overwrite)
