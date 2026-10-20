# ===== 正确的"失忆"实验 =====
# 原理：让 AI 说的信息（一个随机数）只存在于 assistant 消息里
#      如果 assistant 没被追加，AI 第二轮就答不出来
#
# 运行：py chat_memory_test.py
# 切换实验：把下面的 APPEND_ASSISTANT 改成 True / False 各跑一次

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# ============ 实验开关 ============
APPEND_ASSISTANT = False      # ← 改成 False 再跑一次，对比结果
# =================================

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("错误：没找到 DEEPSEEK_API_KEY")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

messages = [
    {"role": "system", "content": "你是一个助手，回答要非常简短，不要解释。"},
]

print("=" * 60)
print(f"实验模式：APPEND_ASSISTANT = {APPEND_ASSISTANT}")
print("=" * 60)

# ---------- 第 1 轮：让 AI 说一个随机数 ----------
q1 = "请随机说一个 1 到 100 的整数，只输出数字，不要其他文字。"
print(f"\n你：{q1}")
messages.append({"role": "user", "content": q1})

r1 = client.chat.completions.create(model="deepseek-flash", messages=messages)
a1 = r1.choices[0].message.content
print(f"AI：{a1}")

if APPEND_ASSISTANT:
    messages.append({"role": "assistant", "content": a1})
    print("    → 已把 AI 的回答追加进历史")
else:
    print("    → ⚠️ 没有追加 AI 的回答")

# ---------- 第 2 轮：问它刚才说了什么 ----------
print()
print("=" * 60)
print(f"第 2 轮发送的消息（共 {len(messages) + 1} 条）：")
for i, m in enumerate(messages, 1):
    c = m["content"][:25]
    print(f"  {i}. [{m['role']:9}] {c}")
print(f"  {len(messages) + 1}. [user     ] 我刚才让你说的数字是多少？")
print("=" * 60)

q2 = "我刚才让你说的数字是多少？只输出数字。"
messages.append({"role": "user", "content": q2})

r2 = client.chat.completions.create(model="deepseek-flash", messages=messages)
a2 = r2.choices[0].message.content
print(f"\n你：{q2}")
print(f"AI：{a2}")

# ---------- 结论 ----------
print()
print("=" * 60)
print("结论")
print("=" * 60)
print(f"  第 1 轮 AI 说的数字：{a1.strip()}")
print(f"  第 2 轮 AI 的回答  ：{a2.strip()}")
if a1.strip() in a2:
    print("  ✅ AI 记得 —— 因为 assistant 消息在历史里")
else:
    print("  ❌ AI 失忆 —— 因为 assistant 消息不在历史里")

if not APPEND_ASSISTANT:
    print()
    print("  把 APPEND_ASSISTANT 改回 True 再跑一次，对比结果。")
