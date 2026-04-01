---
name: poe
description: 调用 Poe API 使用各种大模型（GPT, Claude, Gemini, Kling等）进行翻译、创作等任务
triggers:
  - 命令: poe chat
  - 命令: poe 翻译
  - 命令: poe 创作

# 环境配置
ENV:
  POE_API_KEY: "你的 Poe API key"
  # 可选: 代理配置
  # HTTP_PROXY: "http://127.0.0.1:7890"

# 可用模型 (已验证)
MODELS:
  # Kling 视频生成 (必须用流式 API)
  - name: kling-2.6-pro
    full_name: "Kling 2.6 Pro"
    provider: Kling
    status: ⚠️ 视频生成模型，必须用 stream=True
    max_duration: 240秒

  # Flux 图像生成 (推荐)
  - name: flux-pro
    full_name: "Flux Pro"
    provider: BlackForestLabs
    status: ✅ 可用
    
  - name: flux-dev
    full_name: "Flux Dev"
    provider: BlackForestLabs

  # OpenAI (可用)
  - name: gpt-4o
    full_name: "GPT-4o"
    provider: OpenAI
    status: ✅ 可用
    
  - name: gpt-4o-mini
    full_name: "GPT-4o Mini"
    provider: OpenAI
    status: ✅ 可用 (免费)

# 默认配置
DEFAULT_MODEL: "flux-pro"  # 图像生成推荐
DEFAULT_MODEL_TEXT: "gpt-4o"  # 文本对话
DEFAULT_TEMPERATURE: 0.7
MAX_TOKENS: 4096

---

# Poe API Skill (OpenAI 兼容方式)

## 功能

1. **单轮对话** - 发送消息获取回复
2. **流式输出** - 实时显示生成内容
3. **多模型切换** - 支持 15+ 模型
4. **翻译** - 中英互译
5. **创作** - 短视频脚本、文案等

## 安装依赖

```bash
pip install openai
```

## 基础使用

### 1. 初始化客户端

```python
import openai
import os

client = openai.OpenAI(
    api_key=os.environ.get("POE_API_KEY"),
    base_url="https://api.poe.com/v1",
)
```

### 2. 发送消息

```python
response = client.chat.completions.create(
    model="kling-2.6-pro",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### 3. 流式输出

```python
stream = client.chat.completions.create(
    model="kling-2.6-pro",
    messages=[{"role": "user", "content": "写一首诗"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## 快捷函数

### 对话
```python
def chat(prompt, model="kling-2.6-pro", temperature=0.7):
    import openai
    import os
    client = openai.OpenAI(
        api_key=os.environ.get("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content
```

### 翻译成中文
```python
def translate_to_chinese(text, model="gpt-4o"):
    return chat(f"翻译成中文:\n\n{text}", model=model)
```

### 翻译成英文
```python
def translate_to_english(text, model="gpt-4o"):
    return chat(f"Translate to English:\n\n{text}", model=model)
```

### 图像生成 (推荐)
```python
def generate_image(prompt, model="flux-pro"):
    import openai
    import os
    client = openai.OpenAI(
        api_key=os.environ.get("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    # 返回 Markdown 图片链接
    return content
```

### 创作短视频脚本
```python
def create_video_script(topic, duration=60, model="gpt-4o"):
    prompt = f"""为以下主题创作一个{duration}秒的短视频脚本:
主题: {topic}

要求:
- 开场hook (3秒)
- 内容主体
- 结尾CTA

返回JSON格式:
{{"hook": "...", "content": "...", "cta": "..."}}"""
    return chat(prompt, model=model)
```

### 图像生成提示词
```python
def generate_image_prompt(description, model="flux-pro"):
    prompt = f"""根据描述生成详细的图像提示词:
描述: {description}

返回英文提示词，包含:
- 主体描述
- 背景
- 风格
- 光线
- 色调"""
    return chat(prompt, model=model)
```

### 视频生成 (Kling)
```python
def generate_video(prompt_text, model="kling-2.6-pro"):
    import openai
    import os
    client = openai.OpenAI(
        api_key=os.environ.get("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )
    # 必须用流式 API
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}],
        stream=True
    )
    
    video_url = None
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            # 检测到 URL 即为生成完成
            if "http" in content and "pfst" in content:
                video_url = content.split()[-1]
    return video_url
```

### 多模型对比
```python
def compare_models(prompt, models=None):
    import openai
    import os
    if models is None:
        models = ["flux-pro", "gpt-4o"]
    
    client = openai.OpenAI(
        api_key=os.environ.get("POE_API_KEY"),
        base_url="https://api.poe.com/v1",
    )
    results = {}
    for model in models:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        results[model] = response.choices[0].message.content
    return results
```

## 使用示例

### 命令行对话
```bash
export POE_API_KEY="你的key"

python3 -c "
import openai, os
client = openai.OpenAI(api_key=os.environ['POE_API_KEY'], base_url='https://api.poe.com/v1')
print(client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': '你好'}]
).choices[0].message.content)
"
```

### 翻译新闻
```bash
python3 -c "
import openai, json, os
client = openai.OpenAI(api_key=os.environ['POE_API_KEY'], base_url='https://api.poe.com/v1')
result = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': '翻译成中文: Claude Code source code leak reveals architecture secrets'}]
)
print(result.choices[0].message.content)
"
```

### 生成图像
```bash
python3 -c "
import openai, os
client = openai.OpenAI(api_key=os.environ['POE_API_KEY'], base_url='https://api.poe.com/v1')
result = client.chat.completions.create(
    model='flux-pro',
    messages=[{'role': 'user', 'content': 'A cute robot reading news in a futuristic studio'}]
)
print(result.choices[0].message.content)
"
```

## 检查清单

- [ ] 设置 POE_API_KEY 环境变量
- [ ] 测试连接
- [ ] 选择模型并发送第一条消息
- [ ] 验证翻译/创作结果

## 错误处理

```python
import openai
from openai import APIError, RateLimitError

try:
    response = client.chat.completions.create(model="gpt-4o", messages=[...])
except RateLimitError:
    print("请求过于频繁")
except APIError as e:
    print(f"API错误: {e}")
except Exception as e:
    print(f"错误: {e}")
```

## 注意事项

1. **API Key 安全**: 不要提交到 git
2. **频率限制**: 遵守 Poe API 限制
3. **模型选择**:
   - 文本对话: `gpt-4o` 或 `gpt-4o-mini`
   - 图像生成: `flux-pro` (推荐) 或 `flux-dev`
   - 视频生成: `kling-2.6-pro` (必须用 stream=True，等待 240 秒)
4. **kling-2.6-pro 是视频模型**: 需要流式 API 实时获取进度
