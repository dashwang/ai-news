#!/usr/bin/env node
/**
 * AI News Publisher - Universal Installer
 * 一键安装 AI News Publisher Skill 到 OpenClaw
 * 支持所有大模型提供商（OpenAI、Anthropic、StepFun、KiloClaw 等）
 *
 * 用法:
 *   node install.js [options]
 *
 * 选项:
 *   --provider <name>    模型提供商: openai|anthropic|stepfun|kilo|custom
 *   --model <name>       模型名称 (默认: gpt-4o)
 *   --target <path>      OpenClaw workspace 路径 (默认: ~/.openclaw/workspace)
 *   --no-wechat          跳过 WeChat 配置检查
 *   --force             强制重新安装
 *
 * 示例:
 *   node install.js --provider stepfun --model step-1.5-flash
 *   node install.js --provider kilo  # 使用 KiloClaw 内置 LLM
 *   node install.js --provider openai --model gpt-4o
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// 解析参数
const args = {};
for (let i = 2; i < process.argv.length; i++) {
  const arg = process.argv[i];
  if (arg.startsWith('--') && i + 1 < process.argv.length && !process.argv[i + 1].startsWith('--')) {
    const key = arg.slice(2);
    args[key] = process.argv[++i];
  } else if (arg.startsWith('--')) {
    args[arg.slice(2)] = true;
  }
}

const provider = args.provider || 'kilo';
const model = args.model || (provider === 'openai' ? 'gpt-4o' : provider === 'anthropic' ? 'claude-sonnet-4' : provider === 'stepfun' ? 'step-1.5-flash' : 'default');
const targetDir = args.target || `${process.env.HOME || process.env.USERPROFILE}/.openclaw/workspace`;
const force = args.force || false;
const skipWechat = args['no-wechat'] || false;

console.log(`🚀 AI News Publisher Universal Installer`);
console.log(`   Provider: ${provider}`);
console.log(`   Model: ${model}`);
console.log(`   Target: ${targetDir}`);
console.log('');

// 步骤1: 检查 OpenClaw
if (!existsSync(join(targetDir, 'AGENTS.md'))) {
  console.error('❌ 错误: 未找到 OpenClaw workspace');
  console.error(`   请确认路径: ${targetDir}`);
  console.error('   或使用 --target 指定正确路径');
  process.exit(1);
}

// 步骤2: 安装 Skill
const skillDir = join(targetDir, 'skills', 'ai-news-publisher');
if (existsSync(skillDir) && !force) {
  console.log(`📂 Skill 已存在，跳过安装`);
  console.log(`   使用 --force 强制重新安装`);
} else {
  if (existsSync(skillDir)) {
    console.log(`🧹 清理旧版本...`);
    execSync(`rm -rf "${skillDir}"`, { stdio: 'pipe' });
  }

  console.log(`📦 安装 Skill...`);
  mkdirSync(dirname(skillDir), { recursive: true });
  execSync(
    `git clone -b kilo-v5-stable --depth 1 https://github.com/dashwang/ai-news.git "${skillDir}"`,
    { stdio: 'pipe', env: { ...process.env, GIT_TERMINAL_PROMPT: '0' } }
  );
  console.log(`✅ Skill 已安装到 ${skillDir}`);
}

// 步骤3: 安装依赖
console.log('📦 安装 Node.js 依赖...');
execSync('npm install', { cwd: skillDir, stdio: 'pipe' });

// 步骤4: 配置模型提供商
console.log('⚙️  配置模型提供商...');
const configPath = join(skillDir, '.env');
const envConfig = [];

if (provider === 'openai') {
  if (!process.env.OPENAI_API_KEY) {
    console.log('⚠️  OPENAI_API_KEY 未设置，请手动配置 .env 文件');
  } else {
    envConfig.push(`OPENAI_API_KEY=${process.env.OPENAI_API_KEY}`);
  }
  envConfig.push(`LLM_PROVIDER=openai`);
  envConfig.push(`LLM_MODEL=${model}`);
}
else if (provider === 'anthropic') {
  if (!process.env.ANTHROPIC_API_KEY) {
    console.log('⚠️  ANTHROPIC_API_KEY 未设置，请手动配置 .env 文件');
  } else {
    envConfig.push(`ANTHROPIC_API_KEY=${process.env.ANTHROPIC_API_KEY}`);
  }
  envConfig.push(`LLM_PROVIDER=anthropic`);
  envConfig.push(`LLM_MODEL=${model}`);
}
else if (provider === 'stepfun') {
  if (!process.env.STEPFUN_API_KEY) {
    console.log('⚠️  STEPFUN_API_KEY 未设置，请手动配置 .env 文件');
  } else {
    envConfig.push(`STEPFUN_API_KEY=${process.env.STEPFUN_API_KEY}`);
  }
  envConfig.push(`LLM_PROVIDER=stepfun`);
  envConfig.push(`LLM_MODEL=${model}`);
}
else if (provider === 'kilo') {
  envConfig.push(`LLM_PROVIDER=kilo`);
  envConfig.push(`LLM_MODEL=kilo-claude`);
}
else if (provider === 'custom') {
  console.log('🔧 自定义提供商模式');
  console.log(`   请手动编辑 ${configPath} 配置 LLM 参数`);
}

// 写入 .env
if (envConfig.length > 0) {
  require('fs').writeFileSync(configPath, envConfig.join('\n') + '\n');
  console.log(`✅ 模型配置已写入: ${configPath}`);
}

// 步骤5: WeChat 配置
if (!skipWechat) {
  if (!process.env.WECHAT_APP_ID || !process.env.WECHAT_APP_SECRET) {
    console.log('');
    console.log('⚠️  WeChat 配置未找到');
    console.log(`   请设置环境变量或在 ${configPath} 中添加:`);
    console.log('   WECHAT_APP_ID=你的AppID');
    console.log('   WECHAT_APP_SECRET=你的AppSecret');
    console.log('');
    console.log('   获取地址: https://mp.weixin.qq.com');
  } else {
    console.log('✅ WeChat 配置已检测');
  }
}

// 步骤6: 生成使用说明
console.log('');
console.log('🎉 安装完成！');
console.log('');
console.log('📖 使用命令:');
console.log('');
console.log('   # 运行新闻抓取+翻译（使用 OpenClaw Agent 自动调用 LLM）');
console.log(`   $ openclaw agent run ai-news-publisher --date=$(date +%Y-%m-%d) --limit=15`);
console.log('');
console.log('   # 发布到微信草稿箱');
console.log(`   $ openclaw agent run ai-news-publisher --publish`);
console.log('');
console.log('   # 本地直接运行（使用配置的 LLM）');
console.log(`   $ node ${skillDir}/agent-proper.js --limit=15`);
console.log('');
console.log('📁 安装位置: ' + skillDir);
console.log('📄 配置文件: ' + configPath);
console.log('');
console.log('💡 提示: 如果 openclaw agent 命令报错，尝试:');
console.log('   $ openclaw gateway restart');
