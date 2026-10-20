# ===== 多轮对话（带"透视"版，专门用来理解原理）=====
# 运行：py chat_multi_explain.py

import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI

# ---------- 准备 ----------
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("错误：没找到 DEEPSEEK_API_KEY，检查 .env 文件")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ---------- 聊天记录本 ----------
# 一开始只有一条：system（导演的要求）
messages = [
    {"role": "system", "content": "你是一个友好的助手，回答简短一些。"},
]

round_num = 0          # 记录第几轮
total_tokens = 0       # 累计 token

print("=" * 60)
print("多轮对话演示（输入 exit 退出）")
print("=" * 60)

while True:
    user_input = input("\n你：")

    # ② 退出判断
    if user_input == "exit":
        print("再见！")
        break

    round_num += 1

    # ③ 把你的话记进记录本
    messages.append({"role": "user", "content": user_input})

    # ---------- 透视：看看这次要发给 AI 什么 ----------
    print()
    print("┌" + "─" * 58 + "┐")
    print(f"│ 第 {round_num} 轮：即将发给 AI 的消息（共 {len(messages)} 条）".ljust(58) + "│")
    print("└" + "─" * 58 + "┘")
    for i, m in enumerate(messages, 1):
        role = m["role"]
        content = m["content"]
        # 内容太长就截断显示
        if len(content) > 30:
            content = content[:30] + "..."
        print(f"  {i}. [{role:9}] {content}")

    # ④ 发给 AI（发的是整个 messages 列表）
    prompt_estimate = sum(len(m["content"]) for m in messages)
    print(f"\n  （估算输入约 {prompt_estimate} 个字符，实际 token 以 API 返回为准）")

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
    )

    # ⑤ 从 response 里层层取出回答
    answer = response.choices[0].message.content

    # ⑥ 把 AI 的回答也记进记录本
    messages.append({"role": "assistant", "content": answer})

    # ⑦ 显示
    print(f"\nAI：{answer}")

    # 统计 token
    used = response.usage.total_tokens
    total_tokens += used
    print(f"\n  [本次 {used} tokens，累计 {total_tokens} tokens]")

print()
print("=" * 60)
print(f"总共聊了 {round_num} 轮，累计消耗 {total_tokens} tokens")
print(f"最终记录本里有 {len(messages)} 条消息")
print("=" * 60)

# 打印最终的完整聊天记录，看它长什么样
print()
print("最终的 messages 结构（前 200 字符）：")
print(json.dumps(messages, ensure_ascii=False, indent=2)[:200] + "...")
