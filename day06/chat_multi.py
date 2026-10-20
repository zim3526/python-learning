# ===== 练习 1：多轮对话 =====
# 运行：py chat_multi.py
# 关键实验：把第 18 行注释掉，看 AI 会不会"失忆"

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# ---------- ① 准备：读密钥 + 创建客户端 ----------
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("错误：没找到 DEEPSEEK_API_KEY，请检查 .env 文件")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ---------- ② 聊天记录本（一开始只有 system）----------
messages = [
    {"role": "system", "content": "你是一个友好的助手"},
]

total_tokens = 0

# ---------- ③ 循环：每轮做同样的事 ----------
while True:
    user_input = input("你：")

    if user_input == "exit":
        print("再见！")
        break

    # ③-a 把用户这句话记进历史
    messages.append({"role": "user", "content": user_input})

    # ③-b 把【完整历史】发给 AI
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
    )

    # ③-c 从响应里取出回答（层层剥离）
    answer = response.choices[0].message.content

    # ③-d 把 AI 的回答也记进历史
    # ⭐ 实验：把下面这一行前面加 # 注释掉，再试一次，观察 AI 是否"失忆"
    messages.append({"role": "assistant", "content": answer})

    # ③-e 显示回答和统计
    used = response.usage.total_tokens
    total_tokens += used
    print(f"AI：{answer}")
    print(f"    [本次 {used} tokens，累计 {total_tokens} tokens，历史 {len(messages)} 条]")
