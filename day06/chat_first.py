# ===== 第一次调用 AI API =====
# 运行前必须：1) 在 day06 目录建好 .env  2) .env 里写 DEEPSEEK_API_KEY=sk-xxx
# 运行：py chat_first.py

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# ---------- ① 读密钥 ----------
load_dotenv()                                  # 读 .env 文件
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("=" * 55)
    print("错误：没有找到 DEEPSEEK_API_KEY")
    print("=" * 55)
    print("请检查：")
    print("  1. day06 目录下有没有 .env 文件？")
    print("  2. .env 内容是不是 DEEPSEEK_API_KEY=sk-xxxx（不要加引号）")
    sys.exit(1)

print(f"密钥读取成功，前 8 位：{api_key[:8]}...（后面的不显示，安全）")
print()

# ---------- ② 创建客户端 ----------
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",       # DeepSeek 的地址
)

# ---------- ③ 发请求 ----------
print("=" * 55)
print("正在问 AI：什么是 token？")
print("=" * 55)

response = client.chat.completions.create(
    model="deepseek-flash",                    # 模型名
    messages=[
        {"role": "system", "content": "你是一个耐心的编程老师，回答要简短清楚。"},
        {"role": "user", "content": "用两三句话解释什么是 token，给一个中文例子。"},
    ],
)

# ---------- ④ 取出回答 ----------
answer = response.choices[0].message.content
print()
print("AI 的回答：")
print(answer)

# ---------- ⑤ 看花了多少 token ----------
print()
print("=" * 55)
print("本次调用消耗")
print("=" * 55)
print(f"  输入 tokens: {response.usage.prompt_tokens}")
print(f"  输出 tokens: {response.usage.completion_tokens}")
print(f"  总计 tokens: {response.usage.total_tokens}")

# 粗略估算费用（空闲时段：输入 1元/百万，输出 4元/百万）
cost = response.usage.prompt_tokens / 1_000_000 * 1 + \
       response.usage.completion_tokens / 1_000_000 * 4
print(f"  估算费用: {cost:.6f} 元  （约 {cost * 100:.4f} 分钱）")
