#!/bin/bash
# 替換成你實際的 GitHub username
USERNAME="tomcheung99"
REPO_NAME="browser-use-api"

# 初始化新的 git repo（清除舊的 .git）
rm -rf .git
git init
git add .
git commit -m "Initial commit: browser-use API with Kimi, OpenAI, Anthropic support"

# 添加遠端
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

# 推送到 main 分支
git branch -M main
git push -u origin main

echo "✅ 推送完成！Repo: https://github.com/$USERNAME/$REPO_NAME"
