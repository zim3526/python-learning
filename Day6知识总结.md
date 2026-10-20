# Day 6 知识总结：调用 AI 与做第一个 AI 应用

> 学习日期：2026-10-18 ~ 10-20（跨了三天，实际学习时间约 6-8 小时）
> 产出：`chat_first.py`、`chat_multi.py`、`chat_stream.py`、`chat_stream_v2.py`、`ai_comment.py`、**`grade_ai/`（完整 AI 应用）**
> 核心主题：**从"会写程序"到"会用 AI 做程序"**

---

# 目录

1. [Day 6 的意义](#一day-6-的意义)
2. [API 是什么](#二api-是什么)
3. [API Key 与安全](#三api-key-与安全)
4. [openai SDK 的结构](#四openai-sdk-的结构)
5. [messages：对话的完整数据结构](#五messages对话的完整数据结构)
6. [AI 没有记忆（无状态）](#六ai-没有记忆无状态)
7. [流式输出](#七流式输出)
8. [思考模式与成本](#八思考模式与成本)
9. [AI 幻觉](#九ai-幻觉)
10. [结构化输出（JSON）](#十结构化输出json)
11. [分层设计：把 AI 封装成模块](#十一分层设计把-ai-封装成模块)
12. [确定性 vs AI 的分工](#十二确定性-vs-ai-的分工)
13. [今天踩过的坑](#十三今天踩过的坑)
14. [核心能力清单](#十四核心能力清单)
15. [下一步](#十五下一步)

---

# 一、Day 6 的意义

**Day 1-5 你学的**：让程序"能算、能存、能组织"。

**Day 6 你学的**：让程序"**能理解语言、能生成文字**"。

| 之前 | 现在 |
|---|---|
| 程序只会按规则算分数 | 程序能**理解"张三考了 85 分"并写出评语** |
| 你写死所有逻辑 | 你**描述任务，AI 执行** |
| 数据是人输入的 | 数据可以是**自然语言** |

**这是"编程"到"AI 应用开发"的分水岭。**

---

# 二、API 是什么

## 一句话

> **API = 别人开的一个窗口，你按规矩递进去一个问题，它按规矩返回一个答案。**

## 生活类比：餐厅点菜

| 餐厅 | API |
|---|---|
| 菜单（有什么菜） | 接口文档（能做什么） |
| 你点的菜名 | 请求参数 |
| 服务员 | 网络传输 |
| 端菜出来 | 响应结果 |
| 叫号牌 | API Key |

## API 的四要素

| 要素 | 说明 | DeepSeek 的例子 |
|---|---|---|
| **URL（地址）** | 服务器在哪 | `https://api.deepseek.com/chat/completions` |
| **方法（Method）** | 要干什么 | `POST`（提交数据） |
| **请求头（Headers）** | 附加信息 | `Authorization: Bearer sk-xxx` |
| **请求体（Body）** | 提交的内容 | `{"messages": [...], "model": "..."}` |

## 响应也分三部分

| 部分 | 说明 |
|---|---|
| **状态码** | `200` 成功、`401` 没权限、`402` 余额不足、`429` 太频繁、`500` 服务器错 |
| **响应头** | 附加信息 |
| **响应体** | **你要的数据**（JSON） |

## 用 Python 调 API 的四个步骤

```python
import requests

response = requests.get(url)         # ① 发请求
response.status_code                 # ② 看状态码
response.text                        # ③ 原始文本
data = response.json()               # ④ 解析成字典
```

**所有 API 调用都是这个骨架** —— AI API 只是"响应体里装的是一段文字"。

---

# 三、API Key 与安全

## API Key 是什么

> **API Key = 你的"身份证 + 银行卡"。**

| 特征 | 说明 |
|---|---|
| 证明你是谁 | 服务器靠它知道"这是谁的请求" |
| 用来计费 | 每次调用从你的账户扣钱 |
| **泄露 = 别人用你的钱** | 有人专门扫 GitHub 上的 Key |
| 可以随时作废 | 在平台控制台删掉重发 |

## 🔴 三层安全防线

| 防线 | 做法 |
|---|---|
| **① 不写进代码** | Key 只放在 `.env` 文件里 |
| **② 不让 Git 看见** | `.gitignore` 里有 `.env` |
| **③ 平台侧保护** | 设置消费限额、必要时作废重发 |

## `.env` 文件的标准写法

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

**⚠️ 三个必须注意**：
- **不要加引号**
- **不要有空格**
- **不要提交到 Git**

## 代码里怎么读

```python
import os
from dotenv import load_dotenv

load_dotenv()                                  # 把 .env 内容塞进环境变量
api_key = os.getenv("DEEPSEEK_API_KEY")        # 从环境变量取出

if not api_key:
    print("错误：没找到 API Key")
    sys.exit(1)                                # 立刻停止，别让它带着 None 往下跑
```

## 数据流

```
.env 文件  ──load_dotenv()──>  环境变量  ──os.getenv()──>  你的变量
```

**`os.getenv` 不直接读 `.env` 文件** —— 是 `load_dotenv` 先把它搬进了环境变量。

## 验证 `.gitignore` 生效

```powershell
git status --ignored
```

**`Ignored files:` 下能看到 `.env` = 安全**
**`Untracked files:` 下看到 `.env` = 立刻停下检查**

---

# 四、openai SDK 的结构

## 创建客户端

```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,                          # 身份证
    base_url="https://api.deepseek.com",      # 电话号码（服务器地址）
)
```

## 两个参数的作用

| 参数 | 解决什么 | 不写会怎样 |
|---|---|---|
| **`api_key`** | **我是谁** | 报 `AuthenticationError` |
| **`base_url`** | **我要找谁** | 默认连 OpenAI 官方，你的 DeepSeek Key 无效 → 401 |

**用银行类比**：
- `api_key` = 你的银行卡
- `base_url` = 哪家银行
- **拿工商的卡去建设银行取钱 → 被拒，不是因为卡是假的，是因为走错门了**

## 为什么 DeepSeek 能用 OpenAI 的库

**因为 DeepSeek 的接口"模仿"了 OpenAI 的格式**（业内叫 "OpenAI 兼容"）。

**类比**：不同品牌的手机都用同一个充电口（Type-C）—— **线不用换，只是插到不同的手机上。**

**所以换平台只需要改两个地方**：

| 要改的 | OpenAI | DeepSeek |
|---|---|---|
| `base_url` | `https://api.openai.com/v1` | `https://api.deepseek.com` |
| `model` | `gpt-4o` 等 | `deepseek-flash` 等 |

## 链式调用：`client.chat.completions.create(...)`

```
client                      ← 整个公司（你创建的对象）
  └─ .chat                  ← 公司的「对话事业部」
       └─ .completions      ← 事业部里的「文字生成组」
            └─ .create()    ← 让这个组「执行一项任务」
```

**读法**：**"请公司(client)的对话事业部(chat)，找文字生成组(completions)，执行一次任务(create)。"**

**为什么这么设计**：一个 `client` 能做很多事，用"点号"层层定位。

| 想做的事 | 调用 |
|---|---|
| **文字对话** | `client.chat.completions.create()` |
| 画图 | `client.images.generate()` |
| 语音转文字 | `client.audio.transcriptions.create()` |
| 查有哪些模型 | `client.models.list()` |

---

# 五、messages：对话的完整数据结构

## 结构：列表套字典

```python
messages = [
    {"role": "system",    "content": "你是一个中学老师"},
    {"role": "user",      "content": "什么是 token？"},
    {"role": "assistant", "content": "Token 是..."},
]
```

| 结构 | 为什么 |
|---|---|
| **列表 `[...]`** | 对话有**多条**消息，要按顺序 |
| **字典 `{...}`** | 每条消息有**两个属性**：谁说的 + 说了什么 |

## 哪些固定，哪些自由

| 部分 | 能不能改 |
|---|---|
| 键名 `"role"` | ❌ **固定** |
| 键名 `"content"` | ❌ **固定** |
| `"system"` 这个值 | ⚠️ **只能是 `system` / `user` / `assistant`** |
| **`content` 的内容** | ✅ **完全自由** |

> **一句话：结构固定，内容自由。**

## 三个角色的含义

| 角色 | 谁说的 | 类比 | 作用 |
|---|---|---|---|
| **`system`** | **你（开发者）** | **导演给演员的剧本要求** | 设定人格、规则、格式 |
| **`user`** | 用户 | 观众问的话 | 提问 |
| **`assistant`** | AI | 演员的表演 | 回答（历史记录用） |

## system 的威力（实测）

**同一句问题"介绍一下你自己"，三种 system**：

| system 内容 | AI 回答 |
|---|---|
| "你是一个惜字如金的人，最多回答 10 个字" | `我是AI助手，乐于助人` |
| "你是一个热情洋溢的老师，语气要活泼，带表情符号" | `嗨～我是热情满满、随时准备陪你一起探索知识的AI老师😄！` |
| "你是一个只说英文的助手" | `I am a concise English-only assistant...` |

> **你写什么，AI 就扮演什么。**

**⚠️ 成本提示**：`system` 写得越长，每次调用成本越高（因为每轮都要发它）。**简洁但有效，别写小作文。**

---

# 六、AI 没有记忆（无状态）

## 核心事实

> **API 是无状态的 —— 每次请求都是全新的，服务器不记得上次聊了什么。**
> **AI 的"记忆"完全靠你每次把历史对话重新发过去。**

## 数据流

```
第 1 轮：发送 [system, user1]
第 2 轮：发送 [system, user1, assistant1, user2]        ← 历史越来越长
第 3 轮：发送 [system, user1, assistant1, user2, assistant2, user3]
```

## 消息条数规律

| 轮次 | 发送时 messages 里有几条 |
|---|---|
| 第 1 轮 | **2 条**（system + user） |
| 第 2 轮 | **4 条** |
| 第 N 轮 | **2N 条** |

## `append` 是"追加"，不是"覆盖"

```python
messages.append({...})       # ✅ 旧的都在，新的贴后面（列表变长）
messages = [{...}]           # ❌ 整个换掉，旧的没了
```

**判断方法**：**`append` 之后 `len(messages)` 会变大；`=` 之后会变回 1。**

## 实验验证：删掉 assistant 追加会怎样

```python
messages.append({"role": "assistant", "content": answer})     # 删掉这行
```

| 实验 | 第 1 轮 AI 说 | 第 2 轮问"刚才的数字是多少" | 结果 |
|---|---|---|---|
| **保留这行** | 73 | **73** | ✅ 记得 |
| **删掉这行** | 37 | **42** | ❌ **不是"不知道"，是编了一个！** |

> **没有上下文时，AI 不会说"我不知道"，它会编一个看起来合理的答案。**
> **这就是"幻觉"。**

---

# 七、流式输出

## 为什么需要

```
普通模式：
  [屏幕卡住 8 秒]
  AI：[500 字一次性吐出来]

流式模式：
  AI：今天...天气...很...好...
  [字一个个出现，用户知道它在工作]
```

## 代码只改三处

```python
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    stream=True,                                      # ⭐ ① 打开流式
)

full_answer = ""
for chunk in response:                                # ⭐ ② 一块块取
    if chunk.choices:                                 # 防统计包（空箱子）
        delta = chunk.choices[0].delta.content        # ⭐ ③ 取增量（delta 不是 message）
        if delta:                                     # 防 None
            print(delta, end="", flush=True)
            full_answer += delta
```

## 普通模式 vs 流式模式

| | 普通模式 | 流式模式 |
|---|---|---|
| 对象类型 | `ChatCompletion` | **`Stream`** |
| 取文字 | `.message.content` | **`.delta.content`** |
| 有 `.usage` 吗 | ✅ 有 | ❌ **没有** |
| 结果形式 | 一次性完整 | **一块块增量** |

## `delta` 和 `message` 的区别

| | `message.content` | `delta.content` |
|---|---|---|
| 装的是什么 | **完整回答** | **这一小块新增的文字** |
| 数量 | 只有 1 个 | 很多个，拼起来才完整 |

**类比**：

| | 对应 |
|---|---|
| **`message`** | 一封**完整的信** |
| **`delta`** | **信被撕成一片片纸屑**，你一片片收到 |

**`delta` 这个词本身的意思就是"增量、变化量"。**

## 流式下怎么拿 token 统计

**问题**：`response.usage` 报错 `AttributeError: 'Stream' object has no attribute 'usage'`。

**原因**：流式模式下服务端"边生成边发"，**发到一半时它自己也不知道总共用了多少**。

**解法**：**加 `stream_options`，让它在最后额外发一个"账单"**：

```python
response = client.chat.completions.create(
    ...,
    stream=True,
    stream_options={"include_usage": True},      # ⭐ 最后发统计包
)

usage = None
for chunk in response:
    if chunk.usage:                  # ⭐ 遇到账单就收
        usage = chunk.usage
    if chunk.choices:                # ⭐ 统计包可能没 choices
        ...
```

**实测验证**：

```
chunk #76: choices=1  ⭐ 带 usage！
    usage = CompletionUsage(completion_tokens=75, prompt_tokens=35, total_tokens=110, ...)
```

## 为什么要有 `if chunk.usage:`（防御性写法）

```
chunk #1:  .usage = None
...
chunk #75: .usage = None
chunk #76: .usage = CompletionUsage(...)     ← 只有这个有真数据
```

**`if chunk.usage:` = "只有真的有账单时，才更新 usage 变量"** —— **防止被 `None` 覆盖。**

## 为什么要有 `if chunk.choices:`（防空箱子）

**流式输出时，服务器会发两类 chunk**：

| 类型 | 里面有啥 | `choices` |
|---|---|---|
| **文字包**（大部分） | 一小段文字 | ✅ 有 |
| **统计包**（最后一个） | **只有 usage，没有文字** | ⚠️ **可能为空** |

**不检查**：`chunk.choices[0]` → `IndexError: list index out of range`

**两个平台的差异**：

| 平台 | 统计包的 `choices` |
|---|---|
| **OpenAI 官方** | **空列表** `[]` |
| **DeepSeek** | 有 1 项，但 `delta.content` 是 `None` |

> **所以两个都要防** —— 这就是为什么代码里有两层 `if`。

## 流式下必须自己拼完整回答

```python
full_answer = ""
for chunk in response:
    delta = ...
    if delta:
        full_answer += delta        # ⭐ 拼

messages.append({"role": "assistant", "content": full_answer})    # ⭐ 存历史
```

**⚠️ 最容易犯的错**：**忘了 `append` 完整回答**，因为流式模式下没有现成的 `answer` 变量，**你必须自己拼一个。**

---

# 八、思考模式与成本

## DeepSeek 默认开启思考模式

```
你问：什么是列表？
    ↓
[思考过程] 用户问的是编程概念... 需要分语言说明...
    ↓
[最终回答] 列表是编程中的一种数据结构...
```

**思考过程也消耗 token，按"输出价格"计费。**

## 实测成本差异

**同问"什么是列表"**：

| 模式 | `completion_tokens` | 其中思考 |
|---|---|---|
| 思考模式（默认） | **75** | **55** |
| **关闭思考** | **6** | 0 |

**实际输出文字只有 ~20 tokens，但付了 75 tokens 的钱。**

## 怎么关

```python
extra_body={"thinking": {"type": "disabled"}}
```

## ⚠️ 为什么不能直接写 `thinking=...`

```python
client.chat.completions.create(
    ...,
    thinking={"type": "disabled"},        # ❌ 报错
)
```

```
TypeError: Completions.create() got an unexpected keyword argument 'thinking'
```

**原因**：**`thinking` 是 DeepSeek 私有参数，OpenAI 的 SDK 不认识它。**

**`extra_body` = "绕过 SDK 的参数校验，把内容直接塞进发给服务器的 JSON 里"。**

**类比**：

| | 对应 |
|---|---|
| **SDK 参数检查** | 快递公司只收"标准包装" |
| **标准参数** | 标准箱子，直接寄 |
| **私有参数**（`thinking`） | 形状奇怪的物品 |
| **`extra_body`** | **额外买一个"自定义箱子"，照样寄** |

**这个技巧通用**：以后换通义、智谱，它们的私有参数也走 `extra_body`。

## 思考强度控制

```python
reasoning_effort="low"       # 想少一点（更省）
reasoning_effort="high"      # 想多一点（默认）
reasoning_effort="max"       # 想最多
```

## 什么时候关思考

| 场景 | 建议 |
|---|---|
| **简单问答、格式转换、分类** | **关掉**（省钱 + 快） |
| **数学题、复杂推理、多步逻辑** | **开着**（质量更好） |
| **成绩评语这类简单任务** | **关掉** |

**⚠️ 坑**：**思考模式不支持 `temperature`、`presence_penalty`、`frequency_penalty`** —— 传了不报错，也不生效。

---

# 九、AI 幻觉

## 亲眼看到的案例

**实验**：第 1 轮让 AI 说一个随机数，第 2 轮问它"刚才说了什么"，删掉 assistant 历史。

```
第 1 轮：AI 说 37
第 2 轮（没有 assistant 历史）：AI 回答 42
```

**AI 没有说"我不知道"，它编了一个 42。**

## 为什么会这样

**模型的任务是"根据上下文生成最可能的回答"。当上下文里没有这个信息时，它不会说"我没有"，而是会"编一个看起来合理的"。**

## 三层防御

| 方法 | 说明 |
|---|---|
| **在 `system` 里明确要求** | `"如果不知道，就说不知道，不要编造"` |
| **提供上下文（RAG）** | 把资料一起发给它，让它"照材料回答" |
| **让它引用来源** | 要求它标出答案来自哪段材料（**RAG 的核心**） |
| **后处理校验** | 程序检查答案里有没有捏造的字段 |

> **"42" 就是你要解决的"幻觉问题"的最小案例。**
> **RAG（检索增强生成）就是它的主要解法 —— 也是你后面要做的求职主力项目。**

---

# 十、结构化输出（JSON）

## 为什么需要

**普通输出**（自由文字）：

```
张三同学的成绩是85分，属于良好水平。
建议：多练习综合题型。
```

**程序没法直接处理** —— 你得写正则表达式去抠。

**JSON 输出**：

```json
{
  "评语": "张三同学基础扎实，继续保持！",
  "等级": "良好",
  "建议": "多练习综合题"
}
```

**`json.loads()` 一下就能变成字典，直接取字段用。**

## 怎么让 AI 输出 JSON

### ① 加参数

```python
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    response_format={"type": "json_object"},      # ⭐ 强制合法 JSON
    extra_body={"thinking": {"type": "disabled"}},
)
```

### ② 在 prompt 里"画出"结构

```python
system_prompt = """你是一个中学老师，需要根据学生成绩写评语。

你必须只输出一个 JSON 对象，格式严格如下：
{
  "评语": "一句鼓励性的话，30字以内",
  "建议": "一条具体可执行的学习建议，20字以内"
}

不要输出 JSON 以外的任何内容。不要用 ```json 代码块包裹。"""
```

**为什么这样写有效**：

| 做法 | 为什么 |
|---|---|
| **给出完整的 JSON 示例** | AI 会"照着样子"输出 |
| **说明每个字段的要求** | 避免它编造没用的字段 |
| **明确说"不要输出别的"** | 防止它加前言后语 |

### ③ 代码里清洗（双保险）

```python
text = response.choices[0].message.content.strip()
text = text.replace("```json", "").replace("```", "").strip()
data = json.loads(text)
```

**⚠️ 最常见的坑**：AI 很"热心"，会用 ```json 包起来 → `JSONDecodeError`

## 三层错误处理

```python
# 第一层：防网络/API 错误
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"[API 失败] {e}")
    return None

# 第二层：防格式错误
text = response.choices[0].message.content.strip()
text = text.replace("```json", "").replace("```", "").strip()
try:
    data = json.loads(text)
except json.JSONDecodeError:
    print(f"[JSON 解析失败] 原文：{text[:80]}")
    return None

# 第三层：防缺字段
for key in ("评语", "建议"):
    if key not in data:
        print(f"[缺少字段] {key}")
        return None
```

**为什么分层**：**出问题时你能立刻知道"是哪一类问题"，不用猜。**

## `response_format` 的两个限制

| 限制 | 说明 |
|---|---|
| **只保证"是合法 JSON"** | **不保证有你要的字段** |
| **可能返回 `{}` 空对象** | 如果 prompt 没说清 |

> **`response_format` 是"格式保险"，内容还得靠 prompt 说清楚。**

---

# 十一、分层设计：把 AI 封装成模块

## 项目结构

```
day06/grade_ai/
├── storage.py     ← 数据层：读写文件
├── logic.py       ← 逻辑层：统计、查询
├── ai.py          ← AI 层：调模型、生成评语
├── main.py        ← 界面层：菜单、交互
└── .gitignore
```

## 各层职责

| 模块 | 放什么 | 类比 |
|---|---|---|
| **`storage.py`** | `load_scores` / `save_scores` | **仓库管理员**（管存取） |
| **`logic.py`** | `calc_stats` / `is_pass` / `find_by_name` | **会计**（管算账） |
| **`ai.py`** | `calc_level` / `generate_comment` / `generate_all_comments` | **AI 专家**（管调模型） |
| **`main.py`** | 菜单 / 输入 / 显示 | **前台**（管接待） |

## 核心原则

> **`main.py` 不应该知道任何 AI 细节** —— 不认识 `openai`、不认识 `token`、不认识 `client`。
> **它只需要知道一件事**：调用 `generate_all_comments(scores)` 能拿到结果。

**验证方法**：**`main.py` 里 `grep openai` 应该没有结果。**

## `ai.py` 自己管理客户端

```python
# ai.py 顶部
load_dotenv()
_api_key = os.getenv("DEEPSEEK_API_KEY")

if _api_key:
    _client = OpenAI(api_key=_api_key, base_url="https://api.deepseek.com")
else:
    _client = None
```

**为什么用下划线开头**：**`_client` 表示"模块内部私有，别在外面用"。** 这是 Python 的约定。

**为什么外面不该传 client 进来**：**`client` 是 AI 模块的内部实现细节，换平台时只改 `ai.py` 一个文件。**

## 单向依赖

```
main  →  ai / logic / storage          ✅ 好的
storage  →  main                       ❌ 坏的
```

**口头记法**：**上层可以调用下层，下层不能调用上层。**

---

# 十二、确定性 vs AI 的分工

## 核心原则（今天最重要的一课）

> **能用规则算出来的东西，不要交给 AI。**

## 成绩评语的正确拆法

| 数据 | 谁来做 | 为什么 |
|---|---|---|
| **等级**（优秀/良好/及格/不及格） | **Python 的 `if/elif`** | **确定性，100% 准确，不花钱** |
| **评语、建议** | **AI** | **需要语言能力，规则写不出来** |

## 错误的做法（全丢给 AI）

```python
system_prompt = "根据成绩判断等级并写评语"
```

**结果**：AI 把 85 分判成"优秀"（应该"良好"）—— **因为 prompt 没说分档规则，它只能猜。**

## 正确的做法

```python
def calc_level(score):
    """用规则算等级 —— 确定性，不靠 AI"""
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"


def generate_comment(name, score):
    # ① 等级：程序自己算
    level = calc_level(score)

    # ② 评语：把算好的等级告诉 AI
    user_prompt = f"学生姓名{name}，成绩{score}分，等级是[{level}]"

    # ③ AI 只负责写文字
    ...

    # ④ 程序把等级填回结果
    data["等级"] = level
```

## 对比表

| | 全交给 AI | 拆开 |
|---|---|---|
| 准确性 | **看运气** | **确定部分 100%** |
| 成本 | 高 | **低** |
| 可测试 | ❌ | ✅ **可以写断言** |
| 出错定位 | 难（是 AI 还是规则问题？） | **容易** |

> **"哪些交给 AI，哪些交给代码" —— 这个判断决定了你做的应用靠不靠谱。**

---

# 十三、今天踩过的坑

| # | 坑 | 现象 | 原因 | 解法 |
|---|---|---|---|---|
| 1 | **`'Stream' object has no attribute 'usage'`** | 流式下读 `.usage` 报错 | Stream 没有完整 usage | `stream_options={"include_usage": True}` |
| 2 | **`unexpected keyword argument 'thinking'`** | 传私有参数报错 | SDK 不认识 | `extra_body={"thinking": ...}` |
| 3 | **`AttributeError: 'ChatCompletionMessage' has no attribute 'choices'`** | 取内容报错 | 多写了一个 `.choices` | `response.choices[0].message.content` |
| 4 | **`TypeError: string indices must be integers`** | 显示结果报错 | 遍历的不是 `{name: dict}` 结构 | 确认 `generate_all_comments` 的返回结构 |
| 5 | **`>` 写成 `>=`** | **60 判成不及格、80 判成及格、90 判成良好** | **边界漏等号** | `score >= 60` + **断言测试** |
| 6 | **进度提示和实际生成是两个循环** | 7 行进度瞬间全出，然后静默 20 秒 | 代码顺序执行，两个循环分开 | **合成一个循环** |
| 7 | **API 调用没 `try/except`** | 网络抖动一次全崩 | 重写时丢了保护 | 加 `try/except` |
| 8 | **失败的存成 `None`** | 显示时 `info['等级']` 崩溃 | 没有过滤 | `if r: ai_comments[name] = r` |
| 9 | **AI 把 85 分判成"优秀"** | 等级不准 | prompt 没给分档规则 | **等级用代码算** |
| 10 | **`== None` 写回退** | 不规范 | 重写时忘了 | `is None` |

## 一个反复出现的规律

> **你今天踩了 3 次"边界值"的坑**：
> 1. Day 2：`> 60` 应该是 `>= 60`（及格人数）
> 2. Day 2：闰年漏了 `% 400` 规则
> 3. **今天：`calc_level` 用 `>` 而不是 `>=`**
>
> **这不是偶然 —— 说明"边界"是你需要专门建立意识的点。**

**解法：写边界测试。**

```python
tests = [(90, "优秀"), (89, "良好"), (80, "良好"), (79, "及格"),
         (60, "及格"), (59, "不及格")]
for score, expected in tests:
    assert calc_level(score) == expected
```

**`assert` 是什么**：**"我断言这是对的，如果不对就报错。"**

```python
assert 1 + 1 == 2        # 通过，什么都不输出
assert 1 + 1 == 3        # ❌ AssertionError
```

**这比"肉眼看输出"可靠 100 倍，一秒钟跑完所有边界。**

---

# 十四、核心能力清单

| 能力 | 你会了吗 |
|---|---|
| 理解 API 四要素和状态码 | ✅ |
| 用 `.env` 安全存 Key | ✅ |
| 创建客户端、切换平台 | ✅ |
| 理解 `messages` 三角色 | ✅ |
| **用 `system` 塑造 AI 人格** | ✅ |
| **多轮对话（重发历史）** | ✅ |
| **流式输出 + 拿 usage** | ✅ |
| **用 `extra_body` 传私有参数** | ✅ |
| 关闭思考模式省钱 | ✅ |
| **识别 AI 幻觉** | ✅ |
| **用 `response_format` 拿结构化输出** | ✅ |
| **分层设计（AI 独立成模块）** | ✅ |
| **确定性 vs AI 的分工** | ✅ |
| 三层错误处理 | ✅ |
| **用断言做边界测试** | ✅ |

---

# 十五、下一步

## Day 7 预告：把 AI 应用变得"更好用"

| 主题 | 说明 |
|---|---|
| **Web 界面** | 用 `Streamlit` 把你现在的命令行程序变成网页 |
| **Prompt 工程进阶** | 少样本示例、思维链、角色扮演 |
| **批量与并发** | 一次处理几十个学生（比现在的串行快很多） |
| **成本控制** | 缓存、限制输出长度、批量请求 |

**为什么先做 Web 界面**：**命令行程序只能自己用，网页才能给别人用** —— 而"能给别人用"是项目能写进简历的前提。

## 但先做一件事：提交代码

```powershell
cd D:\aistudy
git add .
git commit -m "Day6: 调用 AI API + 流式对话 + AI 评语生成应用"
git push
```

**你的 GitHub 上即将出现第一个 AI 项目。** 🎉

---

# 附：你今天的产出清单

| 文件 | 内容 |
|---|---|
| `chat_first.py` | 第一次调用 AI |
| `chat_multi.py` | 多轮对话 |
| `chat_stream.py` | 流式对话（带 token 统计） |
| **`chat_stream_v2.py`** | **你自己重写的流式对话**（比原版多了 else 分支） |
| `ai_comment.py` | AI 生成评语的独立版本 |
| `demo_api.py` / `demo_explain.py` / `cost_growth.py` | 教学演示 |
| **`grade_ai/`** | ⭐ **完整的 AI 应用（4 个模块）** |
| `Day6预习卡.md` / `Day6预习卡2-结构化输出.md` | 预习资料 |
