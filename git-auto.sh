#!/bin/bash
# 使用方式：./git-auto.sh "你的 commit 訊息"

if [ -z "$1" ]; then
  echo "請輸入 commit 訊息"
  echo "用法：./git-auto.sh \"完成某某課程深度問答\""
  exit 1
fi

echo "=== Git Status ==="
git status -sb

echo ""
echo "=== Adding all changes ==="
git add .

echo ""
echo "=== Committing ==="
git commit -m "$1"

echo ""
echo "=== Pushing to origin main ==="
git push origin main

echo ""
echo "完成！"
