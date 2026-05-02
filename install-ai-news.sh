#!/bin/bash
# AI News Publisher - 一键安装脚本 (Shell 版本)
# 支持任何大模型，通过 OpenClaw Agent 集成

set -e

echo "🚀 AI News Publisher 一键安装"
echo ""

# 配置变量
SKILL_NAME="ai-news-publisher"
REPO_URL="https://github.com/dashwang/ai-news"
BRANCH="kilo-v5-stable"
INSTALL_DIR="${HOME}/.openclaw/workspace/skills/${SKILL_NAME}"

# 1. 检查 OpenClaw
if [ ! -d "${HOME}/.openclaw/workspace" ]; then
  echo "❌ 未找到 OpenClaw workspace"
  echo "   请先安装 OpenClaw: https://docs.openclaw.ai"
  exit 1
fi

echo "✅ OpenClaw workspace 已找到"

# 2. 克隆/更新仓库
if [ -d "${INSTALL_DIR}" ]; then
  echo "📂 Skill 已存在，正在更新..."
  cd "${INSTALL_DIR}"
  git fetch origin "${BRANCH}"
  git reset --hard "origin/${BRANCH}"
  echo "✅ 更新完成"
else
  echo "📦 正在克隆..."
  mkdir -p "${INSTALL_DIR}/../"
  git clone -b "${BRANCH}" --depth 1 "${REPO_URL}" "${INSTALL_DIR}"
  echo "✅ 克隆完成"
fi

# 3. 安装依赖
echo "📦 安装依赖..."
cd "${INSTALL_DIR}"
npm install --silent 2>/dev/null || npm install

# 4. 检查模型配置
echo ""
echo "⚙️  模型配置检测:"
if [ -n "$OPENAI_API_KEY" ]; then
  echo "   ✅ OpenAI API Key 已设置"
else
  echo "   ⚠️  OPENAI_API_KEY 未设置"
fi

if [ -n "$ANTHROPIC_API_KEY" ]; then
  echo "   ✅ Anthropic API Key 已设置"
else
  echo "   ⚠️  ANTHROPIC_API_KEY 未设置"
fi

if [ -n "$STEPFUN_API_KEY" ]; then
  echo "   ✅ StepFun API Key 已设置"
else
  echo "   ⚠️  STEPFUN_API_KEY 未设置"
fi

echo ""
echo "💡 使用 OpenClaw Agent 时，会自动使用 KiloClaw 内置 LLM"
echo "   无需单独配置 API Key"

# 5. WeChat 配置提示
echo ""
if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
  echo "⚠️  WeChat 配置未找到"
  echo "   如需发布到公众号，请设置环境变量:"
  echo "   export WECHAT_APP_ID=你的AppID"
  echo "   export WECHAT_APP_SECRET=你的AppSecret"
  echo "   或编辑 ${INSTALL_DIR}/.env 文件"
else
  echo "✅ WeChat 配置已检测"
fi

# 完成
echo ""
echo "🎉 安装完成！"
echo ""
echo "📖 使用方法:"
echo ""
echo "   方式1: 抓取并翻译今日新闻"
echo "   $ openclaw agent run ai-news-publisher --limit=15"
echo ""
echo "   方式2: 抓取并发布到公众号"
echo "   $ openclaw agent run ai-news-publisher --publish"
echo ""
echo "   方式3: 指定日期"
echo "   $ openclaw agent run ai-news-publisher --date=2026-05-02"
echo ""
echo "📁 安装位置: ${INSTALL_DIR}"
echo "📄 文档: ${INSTALL_DIR}/SKILL.md"
echo ""
