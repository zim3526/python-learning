# 测试：流式模式下如何拿到 token 统计
# 运行：py test_stream_usage.py

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("没找到 Key")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

print("=" * 60)
print("测试：stream_options={'include_usage': True}")
print("=" * 60)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "用一句话说明什么是列表"}],
    stream=True,
    stream_options={"include_usage": True},      # ⭐ 关键参数
)

print("逐个 chunk 观察：")
print()

chunk_index = 0
final_usage = None
answer = ""

for chunk in response:
    chunk_index += 1
    # 检查这个 chunk 有没有 usage
    has_usage = getattr(chunk, "usage", None) is not None
    choice_count = len(chunk.choices) if chunk.choices else 0

    # 只打印关键信息，避免刷屏
    if has_usage:
        print(f"  chunk #{chunk_index}: choices={choice_count}  ⭐ 带 usage！")
        print(f"      usage = {chunk.usage}")
        final_usage = chunk.usage
    elif choice_count > 0:
        delta = chunk.choices[0].delta.content
        if delta:
            answer += delta
            if chunk_index <= 5:
                print(f"  chunk #{chunk_index}: 文字片段 {delta!r}")
    else:
        print(f"  chunk #{chunk_index}: choices 是空的")

print()
print("=" * 60)
print("结果")
print("=" * 60)
print(f"  总 chunk 数      : {chunk_index}")
print(f"  拼接出的回答      : {answer}")
print(f"  拿到的 usage     : {final_usage}")

if final_usage:
    print()
    print(f"  ✅ 成功！输入 {final_usage.prompt_tokens} tokens，"
          f"输出 {final_usage.completion_tokens} tokens，"
          f"共 {final_usage.total_tokens} tokens")
else:
    print()
    print("  ❌ 最后一个 chunk 里也没有 usage —— DeepSeek 可能不支持这个参数")
