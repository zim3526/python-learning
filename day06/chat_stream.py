# ===== 流式多轮对话（带 token 统计）=====
# 运行：py chat_stream.py

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("错误：没找到 DEEPSEEK_API_KEY，请检查 .env 文件")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

messages = [
    {"role": "system", "content": "你是一个回复消息非常简洁的助手，并且不会胡编乱造，不会就是不会"}
]

total_tokens = 0

print("流式对话演示（输入 exit 退出）")
print("=" * 55)

while True:
    user_input = input("\n你：")
    if user_input == "exit":
        print("再见！")
        break

    # ① 把你的话记进历史
    messages.append({"role": "user", "content": user_input})

    print("AI：", end="", flush=True)          # 先打前缀，不换行

    # ② 流式请求
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},     # ⭐ 让服务端最后发统计包
        extra_body={"thinking": {"type": "disabled"}},   # ⭐ 关掉思考模式（省钱）
    )

    # ③ 边收边打印，同时抓住最后的 usage
    full_answer = ""
    usage = None

    for chunk in response:
        # 检查是不是"统计包"（最后一个 chunk 带 usage）
        if chunk.usage:
            usage = chunk.usage

        # 处理文字（统计包的 choices 可能为空，必须判断）
        if chunk.choices:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                full_answer += delta

    print()                                     # 回答结束，换行

    # ④ 把 AI 的回答记进历史（否则下一轮会"失忆"）
    messages.append({"role": "assistant", "content": full_answer})

    # ⑤ 显示统计
    if usage:
        total_tokens += usage.total_tokens
        print(f"    [本次 {usage.prompt_tokens} 输入 + {usage.completion_tokens} 输出 "
              f"= {usage.total_tokens} tokens｜累计 {total_tokens}｜历史 {len(messages)} 条]")
    else:
        print(f"    [没拿到 token 统计｜历史 {len(messages)} 条]")

print()
print(f"对话结束，累计消耗 {total_tokens} tokens")
