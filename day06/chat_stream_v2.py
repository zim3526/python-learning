#导入库
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

#读取密钥
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("错误，没有找到DEEPSEEK_API_KEY，检查.env文件")
    sys.exit(1)

#创建客户端
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

#设定初始ai人格
messages = [
    {"role": "system", "content": "你是一个可爱的助手，每说完一句话之后都会带个喵"}
]

#开始循环
total_tokens = 0
print("输入exit退出：")

while True:
    user_input = input("\nuser：")
    if user_input == "exit":
        print("再见")
        break
    
    #添加用户对话
    messages.append({"role": "user", "content": user_input})

    #刷新缓冲区
    print("AI:", end = "", flush=True)

    #创建流式输出
    response = client.chat.completions.create(
        model= "deepseek-flash",
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
        extra_body={"thinking": {"type": "disabled"}}
    )

    #拼接输出内容
    full_answer = ""
    usage = None

    for chunk in response:
        if chunk.usage:
            usage = chunk.usage

        if chunk.choices:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush = True)
                full_answer += delta

    print()

    #记录ai回答
    messages.append({"role": "assistant", "content": full_answer})

    #统计tokens
    if usage:
        total_tokens += usage.total_tokens
        print(
            f"[本次 {usage.prompt_tokens} 输入 + {usage.completion_tokens} 输出 "
            f"= {usage.total_tokens} tokens｜累计 {total_tokens}｜历史 {len(messages)} 条]"
              )
    else:
        print(f"[没拿到 token 统计｜历史 {len(messages)} 条]")

print()
print(f"对话结束，累计消耗 {total_tokens} tokens")