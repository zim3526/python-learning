# ===== 解剖演示：import / client / messages =====
# 运行：py demo_explain.py
# 这个脚本不花钱（除了最后一个小测试）

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

print("=" * 65)
print("【问题1】这几个 import 到底导入了什么")
print("=" * 65)
print(f"  1. os        = {os}")
print(f"     os.__name__ = {os.__name__}")
print(f"     它是 Python 自带的，不用 pip 安装")
print()
print(f"  2. sys       = {sys}")
print(f"     也是 Python 自带的")
print()
print(f"  3. load_dotenv = {load_dotenv}")
print(f"     type = {type(load_dotenv)}")
print(f"     它是第三方库 python-dotenv 里的一个函数")
print()
print(f"  4. OpenAI    = {OpenAI}")
print(f"     type = {type(OpenAI)}")
print(f"     它是一个【类】（class）—— 可以理解成'设计图'")

print()
print("=" * 65)
print("【问题2】client 是什么")
print("=" * 65)
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("  没有找到 API Key，跳过这部分")
    sys.exit(1)

# 创建客户端
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

print(f"  client       = {client}")
print(f"  type(client) = {type(client)}")
print()
print("  client 是 OpenAI 类造出来的【对象】（成品）")
print()
print("  它身上装着这些'零件'（叫属性）：")
print(f"    client.base_url = {client.base_url}")
print(f"    client.api_key  = {'***已隐藏***' if client.api_key else '空'}")
print()
print("  它还能做这些'动作'（叫方法）：")
print(f"    有 chat 功能吗      : {hasattr(client, 'chat')}")
print(f"    有 models 功能吗    : {hasattr(client, 'models')}")
print(f"    有 images 功能吗    : {hasattr(client, 'images')}")

print()
print("=" * 65)
print("【问题3】messages 的结构")
print("=" * 65)

# 一条消息的三种可能
msg_system = {"role": "system", "content": "你是一个友好的助手"}
msg_user = {"role": "user", "content": "你好"}
msg_assistant = {"role": "assistant", "content": "你好！有什么可以帮你？"}

print("  单条消息长这样（是个字典，2 个键）：")
print(f"    {msg_user}")
print(f"    键有哪些: {list(msg_user.keys())}")
print()
print("  多条消息放一起（是个列表，可以装任意多条）：")
messages = [msg_system, msg_user, msg_assistant]
print(f"    {messages}")
print(f"    一共 {len(messages)} 条")

print()
print("  ⭐ 哪些能改，哪些不能改：")
print("  ┌─────────────────────────────────────────────────────┐")
print("  │  键名 'role' / 'content'          → 固定，不能改      │")
print("  │  role 的值 'system'/'user'/'assistant' → 只能这 3 个  │")
print("  │  content 的内容                    → 完全由你决定 ✅  │")
print("  └─────────────────────────────────────────────────────┘")

print()
print("=" * 65)
print("【实测】system 的内容怎么影响 AI 的回答")
print("=" * 65)

question = "用一句话介绍一下你自己"
print(f"  同一个问题：{question}")
print()

# 三种不同的 system 设定
tests = [
    ("你是一个惜字如金的人，最多回答 10 个字", "极简风格"),
    ("你是一个热情洋溢的老师，语气要活泼，带表情符号", "活泼风格"),
    ("你是一个只说英文的助手", "英文风格"),
]

for system_content, label in tests:
    print(f"  --- system = 「{system_content}」（{label}）")

    resp = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": question},
        ],
    )
    answer = resp.choices[0].message.content.strip()
    print(f"      AI：{answer}")
    print(f"      （消耗 {resp.usage.total_tokens} tokens）")
    print()

print("=" * 65)
print("结论：结构固定（role/content + 三个角色值），但 content 完全自由")
print("      你写什么，AI 就扮演什么。这就是 system 的力量。")
print("=" * 65)
