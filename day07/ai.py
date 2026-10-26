import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")      # ⭐ 明确指定路径
_api_key = os.getenv("DEEPSEEK_API_KEY")

if _api_key:
    _client = OpenAI(api_key=_api_key, base_url="https://api.deepseek.com")
else:
    _client = None
    

def calc_level(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

def generate_comment(name, score):
    if _client is None:
        print("[AI] 未配置 API Key, 请检查 .env 文件")
        return None
    
    level = calc_level(score)
    user_prompt = f"学生姓名{name}，成绩{score}分（满分100），等级是[{level}]"
    system_prompt = f"""你是一个中学老师，需要根据学生成绩写评语。
学生的等级已经确定为{level}
你必须只输出一个 JSON 对象，格式严格如下：
{{
  "评语": "一句鼓励性的话，30字以内，要和[{level}]相符",
  "建议": "一条具体可执行的学习建议，20字以内"
}}

不要输出 JSON 以外的任何内容。不要用 ```json 代码块包裹。"""

    try:
        response = _client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        extra_body={"thinking": {"type": "disabled"}}
        )
    except Exception as e:
        print(f"[API 失败]{e}")
        return None

    text = response.choices[0].message.content.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
        data["等级"] = level
    except json.JSONDecodeError:
        print(f"[JSON 解析失败] 原文：{text[:80]}")
        return None

    return data

def generate_all_comments(scores):
    ai_comments = {}
    for i, (name, score) in enumerate(scores.items(), 1):
        print(f"  ({i}/{len(scores)}) 正在生成 {name} 的评语...")
        r = generate_comment(name, score)
        if r:
            ai_comments[name] = r
        else:
            print(f"{name}生成失败，已跳过")
        
    return ai_comments


if __name__ == "__main__":
    # 边界测试：这是最重要的测试
    tests = [
        (100, "优秀"), (90, "优秀"), (89, "良好"),
        (80, "良好"), (79, "及格"), (60, "及格"),
        (59, "不及格"), (0, "不及格"),
    ]
    for score, expected in tests:
        actual = calc_level(score)
        status = "✅" if actual == expected else "❌"
        print(f"{status} {score} 分 → {actual}（期望 {expected}）")