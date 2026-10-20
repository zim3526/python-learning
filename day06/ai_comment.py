import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("错误，请检查.env文件")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def level_score(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

    
def generate_comment(client, name, score):
    level = level_score(score)
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
        response = client.chat.completions.create(
        model= "deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type":"json_object"},
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

    for key in ("评语", "等级", "建议"):
        if key not in data:
            print(f"[缺少字段]{key}，实际返回{data}")
            return None

    return data


# 测试
for n, s in [("张三", 60),("李四",89),("王五", 59)]:
    r = generate_comment(client, n, s)
    print(f"\n{n}（{s}分）")

    if r:
        print(f"评语：{r['评语']}")
        print(f"等级：{r['等级']}")
        print(f"建议：{r['建议']}")
        