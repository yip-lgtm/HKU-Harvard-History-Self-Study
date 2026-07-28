#!/bin/bash
# ============================================
# git-auto.sh
# 一鍵自動化 Git 流程（add → commit → push）
# 使用方式：./git-auto.sh "你的 commit 訊息"
# ============================================

if [ -z "$1" ]; then
  echo "❌ 請輸入 commit 訊息"
  echo ""
  echo "用法："
  echo "  ./git-auto.sh \"完成 GenEd 1017 深度問答\""
  echo "  ./git-auto.sh \"更新 Phase1 總表 $(date +%Y-%m-%d)\""
  exit 1
fi

echo "=== 1. Git Status ==="
git status -sb
echo ""

echo "=== 2. Adding all changes ==="
git add .
echo ""

# 檢查是否有實際變更
if git diff --cached --quiet; then
  echo "⚠️  沒有變更可提交，已取消。"
  exit 0
fi

echo "=== 3. Committing ==="
git commit -m "$1"
echo ""

echo "=== 4. Pushing to origin main ==="
git push origin main

echo ""
echo "✅ 完成！Commit 訊息：$1"
