# 预习卡 2：把 AI 接进你的程序（结构化输出）

> **用途：看代码之前先扫一遍。** 今天的项目要用到"让 AI 输出 JSON"这个核心技能。

---

# 目录

1. [项目要解决什么问题](#一项目要解决什么问题)
2. [新参数：response_format](#二新参数response_format)
3. [怎么写"让 AI 输出 JSON"的提示](#三怎么写让-ai-输出-json的提示)
4. [解析 AI 的 JSON：json.loads](#四解析-ai-的-jsonjsonloads)
5. [函数的返回值设计](#五函数的返回值设计)
6. [错误处理三件套](#六错误处理三件套)
7. [完整调用示例（带注释）](#七完整调用示例带注释)
8. [常见报错对照](#八常见报错对照)
9. [prompt 设计的三个原则](#九prompt-设计的三个原则)
10. [本次项目用到的全部新东西清单](#十本次项目用到的全部新东西清单)

---

# 一、项目要解决什么问题

**你现在的程序**：能存成绩、能算统计，**但不会"说人话"**。

**目标**：让 AI 根据成绩**生成评语**，并且**返回程序能用的结构化数据**（不是一段随便的文字）。

```
输入：{"张三": 85}
  ↓
AI 处理
  ↓
输出：{"评语": "张三同学基础扎实，继续保持！", "等级": "良好", "建议": "多练习综合题"}
  ↓
程序可以直接用"等级"字段做判断，用"评语"字段显示
```

> **关键洞察：AI 输出的"格式"决定了你的程序能不能用它的结果。**
> **自由文字 → 只能给人看**
> **JSON → 程序能处理**

---

# 二、新参数：`response_format`

## 是什么

**告诉 AI："你必须输出合法的 JSON，别输出别的东西。"**

```python
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    response_format={"type": "json_object"},      # ⭐ 新参数
    extra_body={"thinking": {"type": "disabled"}},
)
```

## 三个取值

| 值 | 含义 |
|---|---|
| `{"type": "json_object"}` | ⭐ **输出一个 JSON 对象**（最常用） |
| `{"type": "text"}` | 默认，普通文字 |
| `{"type": "json_schema", ...}` | 按严格的 schema 输出（更高级，暂不用） |

## 用了之后有什么变化

**不用时**，AI 可能返回：

```
张三同学的成绩是85分，属于良好水平。
建议：多练习综合题型，注意计算速度。
```

**用了之后**，AI 一定返回：

```json
{
  "评语": "张三同学基础扎实，继续保持！",
  "等级": "良好",
  "建议": "多练习综合题"
}
```

**程序拿到后**，`json.loads()` 一下就能变成字典，**直接取字段用**。

## ⚠️ 两个重要限制

| 限制 | 说明 |
|---|---|
| **必须在 prompt 里说明要什么字段** | `json_object` 只保证"是合法 JSON"，**不保证有你要的字段** |
| **可能返回 `{}` 空对象** | 如果 prompt 没说清，AI 可能返回空 JSON |

**所以：`response_format` 是"格式保险"，**内容还得靠 prompt 说清楚**。

---

# 三、怎么写"让 AI 输出 JSON"的提示

## 核心：在 prompt 里"画出"你想要的 JSON 结构

**推荐写法**（把 schema 直接写进 system 或 user）：

```python
system_prompt = """你是一个中学老师，需要根据学生的成绩写评语。

你必须只输出一个 JSON 对象，格式如下：
{
  "评语": "一句鼓励性的话，30字以内",
  "等级": "优秀 或 良好 或 及格 或 不及格",
  "建议": "一条具体的学习建议，20字以内"
}

不要输出 JSON 以外的任何内容。不要用 markdown 代码块包裹。"""
```

**为什么这样写有效**：

| 做法 | 为什么 |
|---|---|
| **给出完整的 JSON 示例** | AI 会"照着样子"输出 |
| **说明每个字段的类型/取值范围** | 避免它编造没用的字段 |
| **明确说"不要输出别的"** | 防止它加前言后语（导致解析失败） |

## ⚠️ 最常见的坑：AI 用 ```json 包起来

**AI 很"热心"，它可能返回**：

````
```json
{"评语": "...", "等级": "良好"}
```
````

**这会让 `json.loads()` 报错**（因为前面有 ```json 这些字符）。

**两个解法**：

**解法 A：在 prompt 里明确禁止**（推荐）
```
不要用 markdown 代码块包裹，不要输出 ```json 标记。
```

**解法 B：代码里清洗**（保险）
```python
text = response.choices[0].message.content.strip()
# 去掉可能的 ```json 和 ``` 标记
if text.startswith("```"):
    text = text.split("\n", 1)[1] if "\n" in text else text
    if text.endswith("```"):
        text = text[:-3]
text = text.strip()
```

**实践建议：两个都做**（prompt 约束 + 代码清洗）。

---

# 四、解析 AI 的 JSON：`json.loads`

## 你 Day 4 学过，这里复习

```python
import json

text = '{"评语": "很好", "等级": "良好"}'
data = json.loads(text)          # 字符串 → 字典
print(data["评语"])              # 很好
print(data["等级"])              # 良好
```

## ⚠️ 这里会踩的坑

| 情况 | 报错 |
|---|---|
| AI 返回的不是合法 JSON | `json.JSONDecodeError` |
| AI 返回了空字符串 | `json.JSONDecodeError: Expecting value` |
| AI 返回了数组 `[...]` 而不是对象 | 能解析，但取键会 `TypeError` |

**所以必须用 `try/except` 包起来。**

---

# 五、函数的返回值设计

## 推荐：返回字典，失败返回 None

```python
def generate_comment(name, score):
    """
    为学生生成评语。
    成功返回: {"评语": str, "等级": str, "建议": str}
    失败返回: None
    """
    try:
        # ... 调用 API
        # ... 解析 JSON
        return data
    except Exception as e:
        print(f"生成失败：{e}")
        return None
```

## 为什么"失败返回 None"是好设计

**调用方可以这样用**：

```python
result = generate_comment("张三", 85)
if result is None:
    print("AI 暂时不可用")
else:
    print(result["评语"])
```

**对比"失败抛异常"**：

| 设计 | 优点 | 缺点 |
|---|---|---|
| **返回 None** | 调用方必须检查，代码清晰 | 需要 `if` 判断 |
| **抛异常** | 不写 `if` 也能跑 | **忘了处理就崩** |

**教育场景推荐"返回 None"** —— **强迫你处理失败情况**。

---

# 六、错误处理三件套

## 一个 AI 调用可能在哪出错

```
① 网络问题        → ConnectionError / Timeout
② 密钥/余额问题   → AuthenticationError / 402
③ 限流           → RateLimitError / 429
④ AI 返回格式不对 → JSONDecodeError
⑤ 返回的 JSON 缺字段 → KeyError
```

## 三层防护写法

```python
def generate_comment(name, score):
    # 第一层：整个流程包起来，防网络/API 错误
    try:
        response = client.chat.completions.create(...)
    except Exception as e:
        print(f"[API 调用失败] {e}")
        return None

    # 第二层：清洗 + 解析，防格式错误
    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print(f"[AI 返回的不是合法 JSON] {text[:80]}")
        return None

    # 第三层：检查字段，防缺字段
    for key in ("评语", "等级", "建议"):
        if key not in data:
            print(f"[AI 返回缺少字段] {key}")
            return None

    return data
```

## 为什么三层要分开

| 层 | 防什么 | 出错时你看到的信息 |
|---|---|---|
| **第一层** | 网络/密钥/余额 | "API 调用失败" |
| **第二层** | 格式不对 | "返回的不是合法 JSON" + 前 80 个字 |
| **第三层** | 字段缺了 | "缺少字段 xxx" |

> **分开处理的价值：出问题时你能立刻知道"是哪一类问题"，不用猜。**

---

# 七、完整调用示例（带注释）

```python
import json
from openai import OpenAI

def generate_comment(client, name, score):
    """根据成绩生成结构化评语。成功返回字典，失败返回 None。"""

    system_prompt = """你是一个中学老师，需要根据学生成绩写评语。

你必须只输出一个 JSON 对象，格式严格如下：
{
  "评语": "一句鼓励性的话，30字以内",
  "等级": "优秀 或 良好 或 及格 或 不及格 中的一个",
  "建议": "一条具体可执行的学习建议，20字以内"
}

不要输出 JSON 以外的任何内容。不要用 ```json 代码块包裹。"""

    user_prompt = f"学生姓名：{name}，成绩：{score} 分（满分 100）"

    try:
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},          # ⭐ 强制 JSON
            extra_body={"thinking": {"type": "disabled"}},     # 关思考（省钱）
        )
    except Exception as e:
        print(f"[API 失败] {e}")
        return None

    # 取出文本
    text = response.choices[0].message.content.strip()

    # 清洗可能存在的 markdown 标记
    text = text.replace("```json", "").replace("```", "").strip()

    # 解析
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print(f"[JSON 解析失败] 原文：{text[:80]}")
        return None

    # 校验字段
    for key in ("评语", "等级", "建议"):
        if key not in data:
            print(f"[缺少字段] {key}，实际返回：{data}")
            return None

    return data
```

---

# 八、常见报错对照

| 报错 | 原因 | 解决 |
|---|---|---|
| `json.JSONDecodeError` | AI 返回不是合法 JSON | 加强 prompt + 代码清洗 |
| `KeyError: '评语'` | AI 没返回这个字段 | prompt 里强调字段名 |
| `TypeError: list indices...` | AI 返回了数组不是对象 | prompt 里强调"输出 JSON 对象" |
| `AuthenticationError` | Key 错 | 检查 .env |
| `402` | 余额不足 | 充值 |
| `429` | 频率超限 | 加延时 |
| `AttributeError: 'NoneType'` | 忘了检查返回值 | 用 `if result is None` |

---

# 九、prompt 设计的三个原则

## 原则 1：明确角色（system）

```
你是...（身份）
```

**"你是中学老师" vs "你是数据分析师"** → 写出的评语风格完全不同。

## 原则 2：明确格式（JSON schema）

**给完整的示例，而不是描述。**

| ❌ 差 | ✅ 好 |
|---|---|
| "输出学生的评语和等级" | 给出完整 JSON 示例，标出每个字段的取值范围 |

## 原则 3：明确禁止（负面约束）

**AI 很"热心"，不说清就会加东西。**

| 常见多余动作 | 怎么禁 |
|---|---|
| 加"好的，以下是..." | "不要输出任何解释性文字" |
| 用 markdown 包裹 | "不要用代码块包裹" |
| 加"希望对你有帮助" | "只输出 JSON" |

---

# 十、本次项目用到的全部新东西清单

| 新东西 | 来自 | 作用 | 什么时候用 |
|---|---|---|---|
| **`response_format={"type": "json_object"}`** | openai SDK | 强制 AI 输出合法 JSON | 需要程序处理 AI 结果时 |
| **`json.loads(字符串)`** | json（Day 4 学过） | 字符串 → 字典 | 解析 AI 返回 |
| **`json.JSONDecodeError`** | json | 解析失败时的异常 | `except` 里抓 |
| **`text.replace("```json", "")`** | 字符串方法（Day 1 学过） | 清洗 markdown 标记 | 解析前 |
| **`text.strip()`** | 字符串方法 | 去首尾空白 | 解析前 |
| **`raise` / 自定义函数** | 基础 | 结构组织 | 分层 |
| **`for key in (...)` 检查字段** | 基础 | 校验完整性 | 解析后 |

**没有全新的概念** —— **只是把你已经会的零件（函数、字典、JSON、异常）组装起来用。**

---

# 十一、项目分三步（建议按顺序）

| 步骤 | 内容 | 产出 |
|---|---|---|
| **1** | 单独写 `ai_comment.py`，测通"生成单个学生评语" | 能打印出一个学生的结构化评语 |
| **2** | 写"批量生成"（遍历字典里所有学生） | 能给全班生成评语 |
| **3** | 接进 `main.py`，加一个菜单项 | 程序里能选"AI 评语" |

**每一步都先跑通再往下。** 卡住随时问（这次允许问，但要说清卡在哪一行）。
