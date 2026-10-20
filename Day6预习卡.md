# Day 6 预习卡：调用 AI 会用到的全部新东西

> 用法：**看代码之前先扫一遍这张卡。** 不用背，知道"有这么个东西、大概干什么"就够。
> 遇到不懂的回来查对应条目。

---

# 目录

1. [标准库：os / sys](#一标准库os--sys)
2. [标准库：json](#二标准库json)
3. [第三方库：dotenv](#三第三方库dotenv)
4. [第三方库：openai](#四第三方库openai)
5. [OpenAI 对象的内部结构（最重要）](#五openai-对象的内部结构最重要)
6. [参数速查表](#六参数速查表)
7. [常见报错对照表](#七常见报错对照表)
8. [一个完整调用的"读法"](#八一个完整调用的读法)
9. [将来还会遇到的（预告）](#九将来还会遇到的预告)

---

# 一、标准库：os / sys

**标准库 = Python 自带，不用 `pip install`。**

## `import os`

**os = operating system（操作系统）**

| 用法 | 作用 | 例子 | 返回值 |
|---|---|---|---|
| `os.getenv("名字")` | **读一个环境变量** | `os.getenv("DEEPSEEK_API_KEY")` | 有就返回字符串，没有返回 `None` |
| `os.getcwd()` | 当前工作目录 | `os.getcwd()` | `"D:\\aistudy\\day06"` |
| `os.path.exists("路径")` | 路径存不存在 | `os.path.exists(".env")` | `True` / `False` |

**你会用到的**：`os.getenv` —— **从 `.env` 里读 API Key**。

**记忆点**：**`os` 管"系统层面"的事**（环境变量、目录、路径）。

## `import sys`

**sys = system（Python 解释器本身相关）**

| 用法 | 作用 | 例子 |
|---|---|---|
| `sys.exit(1)` | **立即结束程序**，`1` 表示"出错了" | 没读到 Key 时退出 |
| `sys.exit(0)` | 正常结束（等价于程序自然跑完） | 很少写 |

**为什么用 `sys.exit`**：**程序出错时，与其让它继续说胡话，不如立刻停。**

```python
if not api_key:
    print("错误：没找到 API Key")
    sys.exit(1)          # ← 程序到此为止，后面的代码不执行
```

**`1` 和 `0` 的区别**：

| 退出码 | 含义 |
|---|---|
| `0` | 正常结束 |
| `1`（或非 0） | 出错了 |

**这个约定是全世界的**，脚本、API、系统服务都遵守。

---

# 二、标准库：json

**你 Day 4 已经学过了，这里复习一下它在 Day 6 的用途。**

| 用法 | 作用 |
|---|---|
| `json.dump(数据, 文件)` | Python 对象 → 文件 |
| `json.load(文件)` | 文件 → Python 对象 |
| `json.dumps(数据)` | Python 对象 → 字符串 |
| `json.loads(字符串)` | 字符串 → Python 对象 |

**Day 6 用在哪**：
- 打印 `messages` 的结构：`print(json.dumps(messages, ensure_ascii=False, indent=2))`
- **后面会用它来解析 AI 返回的 JSON**（让 AI 输出结构化数据）

---

# 三、第三方库：dotenv

**库名**：`python-dotenv`（`pip install python-dotenv`）
**导入名**：`dotenv`

## `load_dotenv()`

| 项目 | 说明 |
|---|---|
| **作用** | **读 `.env` 文件，把里面的键值对塞进"环境变量"** |
| **参数** | 通常不传（默认读当前目录的 `.env`） |
| **返回值** | `True`（成功） / `False`（没找到文件）—— **基本不用管** |

```python
load_dotenv()                                  # 执行后，PATH 里就多了 DEEPSEEK_API_KEY
api_key = os.getenv("DEEPSEEK_API_KEY")        # 然后就能读出来
```

**为什么必须调它**：**不调的话 `os.getenv` 读不到 `.env` 里的内容**（因为 `.env` 不是操作系统环境变量，需要这个库先"导入"进去）。

**常见坑**：

| 现象 | 原因 |
|---|---|
| `os.getenv` 返回 `None` | 忘了 `load_dotenv()` |
| 依然 `None` | `.env` 文件名错（可能是 `.env.txt`） |
| 依然 `None` | `.env` 不在"当前工作目录"（`os.getcwd()` 那个目录） |
| 依然 `None` | `.env` 内容格式错（多了引号、空格） |

---

# 四、第三方库：openai

**库名**：`openai`（`pip install openai`）
**导入名**：`openai`

## `OpenAI` 类

| 项目 | 说明 |
|---|---|
| **作用** | 创建"客户端对象"（你的电话机） |
| **常用参数** | `api_key=`（密钥）、`base_url=`（服务器地址） |
| **返回** | 一个 `client` 对象 |

```python
client = OpenAI(
    api_key=api_key,                          # 你的身份证
    base_url="https://api.deepseek.com",      # 拨号地址
)
```

**⚠️ `base_url` 必须改**，否则会连到 OpenAI 官方（你的 DeepSeek Key 无效）。

---

# 五、OpenAI 对象的内部结构（最重要）

**这是你最困惑的地方。我画成"剥洋葱"。**

## 创建客户端后

```
client                                    ← 对象（电话机）
  ├─ .base_url                            ← 属性：服务器地址
  ├─ .api_key                             ← 属性：密钥
  └─ .chat                                ← 功能：对话
       └─ .completions                    ← 功能：文字生成
            └─ .create(...)               ← 方法：发起请求
```

**所以这一长串**：

```python
client.chat.completions.create(...)
```
**读法**：**用 client → 进入 chat 功能 → 进入 completions → 执行 create（发请求）**

## 普通模式返回什么（非流式）

```
response                                  ← 响应对象（一整封信）
  ├─ .id                                  ← 请求编号
  ├─ .model                               ← 用了哪个模型
  ├─ .choices                             ← 【列表】候选回答（通常 1 个）
  │    └─ [0]                             ← 第 1 个候选
  │         ├─ .message                   ← 消息对象
  │         │    ├─ .role                 ← "assistant"
  │         │    ├─ .content              ← ⭐ 你要的文字
  │         │    └─ .reasoning_content    ← 思考过程（思考模式才有）
  │         └─ .finish_reason             ← "stop"（正常结束）
  └─ .usage                               ← 统计
       ├─ .prompt_tokens                  ← 输入用了多少
       ├─ .completion_tokens              ← 输出用了多少（含思考）
       └─ .total_tokens                   ← 总和
```

**所以你要的那句话，路径是**：

```python
response.choices[0].message.content
   │        │      │       │
   │        │      │       └─ 文字内容  ⭐
   │        │      └─ 消息对象
   │        └─ 第 1 个候选
   └─ 整个响应
```

**记忆口诀**：**"响应 → 第1个候选 → 消息 → 内容"**

## 流式模式返回什么（`stream=True`）

**完全不同的结构！**

```
response                                  ← Stream 对象（不是完整响应！）
   │                                         ⚠️ 没有 .usage、没有 .choices[0].message
   └─ 每次 for 循环吐出一个 chunk          ← chunk（一小块）
        ├─ .choices
        │    └─ [0]
        │         └─ .delta               ← ⚠️ 注意！是 delta 不是 message
        │              └─ .content        ← 这一块新增的文字（可能为 None）
        └─ .usage                         ← ⚠️ 只有最后一个 chunk 有
```

**关键差异**：

| | 普通模式 | 流式模式 |
|---|---|---|
| 对象类型 | `ChatCompletion` | **`Stream`** |
| 取文字 | `.message.content` | **`.delta.content`** |
| 有完整 `usage` 吗 | ✅ 有 | ❌ **没有** |
| 怎么拿 usage | `response.usage` | **`stream_options={"include_usage": True}` + 最后一个 chunk** |

**"delta" 这个词的意思**：**增量、变化量** —— 就是"只看这一小块新增的部分"。

---

# 六、参数速查表

## `client.chat.completions.create()` 的常用参数

| 参数 | 作用 | 例子 |
|---|---|---|
| `model` | **必填**，用哪个模型 | `"deepseek-flash"` |
| `messages` | **必填**，消息列表 | `[{"role": "user", "content": "你好"}]` |
| `stream` | 是否流式返回 | `True` / `False` |
| `stream_options` | 流式下的额外选项 | `{"include_usage": True}` |
| `extra_body` | **塞入服务商私有参数** | `{"thinking": {"type": "disabled"}}` |
| `reasoning_effort` | 思考强度 | `"low"` / `"high"` / `"max"` |
| `temperature` | 随机性（0-2，越大越发散） | `0.7` ⚠️ 思考模式下无效 |
| `max_tokens` | 限制最大输出长度 | `500` |

## `stream_options`

| 值 | 作用 |
|---|---|
| `{"include_usage": True}` | ⭐ **让服务端在最后一个 chunk 里附带 token 统计** |
| `{"include_usage": False}` | 默认，不带统计 |

## `extra_body`

**作用**：**绕过 SDK 的参数校验，把内容直接塞进发给服务器的 JSON 里。**

**为什么要它**：`thinking` 是 **DeepSeek 私有参数**，OpenAI 的 SDK 不认识它。直接写 `thinking=...` 会报：

```
TypeError: Completions.create() got an unexpected keyword argument 'thinking'
```

**正确写法**：

```python
extra_body={"thinking": {"type": "disabled"}}      # ✅
```

**这个技巧通用**：以后换通义、智谱，它们的私有参数也走 `extra_body`。

## `thinking` 的取值

| 值 | 效果 | 什么时候用 |
|---|---|---|
| `{"type": "enabled"}` | **默认**，先思考再回答 | 复杂推理、数学题 |
| `{"type": "disabled"}` | 直接回答 | **简单问答、格式转换、分类**（省钱） |

**⚠️ 实测成本差异**：

| 同问"什么是列表" | 输出 tokens |
|---|---|
| 思考模式（默认） | **75**（含 55 思考） |
| 关闭思考 | **6**（第一句） |

## `reasoning_effort` 的取值

| 传入 | 实际强度 |
|---|---|
| `"minimal"` | low |
| `"low"` | low |
| `"medium"` | high |
| `"high"` | high（默认） |
| `"xhigh"` | high |
| `"max"` / `"ultra"` | max |

## `usage` 对象里的字段

| 字段 | 含义 |
|---|---|
| `usage.prompt_tokens` | 输入消耗 |
| `usage.completion_tokens` | 输出消耗（**含思考**） |
| `usage.total_tokens` | 总和 |
| `usage.completion_tokens_details.reasoning_tokens` | **其中"思考"用了多少** |
| `usage.prompt_tokens_details.cached_tokens` | 输入里有多少命中缓存（**便宜 25 倍**） |

---

# 七、常见报错对照表

| 报错 | 原因 | 解决 |
|---|---|---|
| `NameError: name 'client' is not defined` | 没写 `client = OpenAI(...)` | 补上创建客户端的代码 |
| `NameError: name 'api_key' is not defined` | 没读密钥 | `load_dotenv()` + `os.getenv()` |
| `AttributeError: 'Stream' object has no attribute 'usage'` | **流式模式下直接读 `response.usage`** | 加 `stream_options={"include_usage": True}`，在循环里抓 `chunk.usage` |
| `TypeError: unexpected keyword argument 'thinking'` | SDK 不认识这个参数 | 用 `extra_body={"thinking": ...}` |
| `AuthenticationError` / `401` | Key 错/没读到 | 检查 `.env` |
| `Insufficient Balance` / `402` | 余额不足 | 充值 |
| `RateLimitError` / `429` | 请求太频繁 | 等几秒 |
| `IndexError: list index out of range` | `chunk.choices[0]` 但 choices 为空（统计包） | 加 `if chunk.choices:` |
| `ModuleNotFoundError: openai` | 没装 | `py -m pip install openai` |

---

# 八、一个完整调用的"读法"

**把这段代码拆成"五层"，逐层读**：

```python
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
    stream_options={"include_usage": True},
    extra_body={"thinking": {"type": "disabled"}},
)
```

| 层 | 代码 | 含义 |
|---|---|---|
| **1** | `response = ` | 把结果存进变量 |
| **2** | `client` | 用哪个电话机 |
| **3** | `.chat.completions.create` | 走哪条通道、执行什么动作 |
| **4** | `(...)` 里的参数 | 这次请求的"设置" |
| **5** | `model` / `messages` / ... | 每个参数的具体值 |

**参数里只有两个是"必须"的**：`model` 和 `messages`。**其他都是可选的"调优"**。

---

# 九、将来还会遇到的（预告）

> 这些你**现在不用管**，只是让你有个心理准备。

| 名字 | 什么时候用 | 一句话 |
|---|---|---|
| `response_format={"type": "json_object"}` | **让 AI 只输出 JSON** | 程序能直接解析（**下一个练习会用**） |
| `tools` | **让 AI 调用函数** | 比如"查数据库"（Day 7-8） |
| `tool_calls` | AI 决定要调用哪个函数 | 同上 |
| `temperature` | 控制随机性 | 创作类任务调高，数据类调低 |
| `max_tokens` | 限制输出长度 | 省钱 |
| `tiktoken` | 精确数 token（OpenAI 的） | DeepSeek 用 API 返回的 usage 更准 |
| `httpx` | 底层网络库 | `openai` 内部在用它 |
| `FastAPI` / `Streamlit` | 做 Web 界面 | Day 8 之后 |

---

# 十、学习建议（针对你的情况）

## 你今天的困惑，根源不是"笨"，是"信息密度"

**今天一天你接触了**：

| 类别 | 数量 |
|---|---|
| 新的 import | 4 个 |
| 新的库/对象 | 3 个（client / response / chunk） |
| 新的参数 | 8 个以上 |
| 新的概念 | 6 个（无状态、幻觉、流式、思考模式、四要素、角色） |

**这相当于别人 3-4 天的量。** 你觉得吃力是**正常的**。

## 建议的学习方法

**① 遇到不懂的，先查《预习卡》，别硬扛**

**② 用"三层理解法"对待每一行代码**

| 层 | 问什么 | 够了就行 |
|---|---|---|
| **这行在干什么** | 一句话说清 | ✅ 最重要 |
| **它的输入输出是什么** | 给什么、得到什么 | ✅ 够用 |
| **它内部怎么实现** | 源码细节 | ❌ **现在不用管** |

**③ 不要怕"记不住"**

**你不是要背下来，你是要知道"有这么个东西"** —— **写代码时查文档、查预习卡、问 AI，都是正常的工作方式。**

**④ 每段代码都跑一遍**

**看不懂就改一点、跑一下、看变化** —— 刚才你那个 `APPEND_ASSISTANT = True/False` 的实验，比看十遍解释有用。

## 以后每节课的安排（承诺）

**每个新板块开始前，我会先给一份《预习卡》**，包含：

1. **新函数/方法清单**（名字、来自哪、干什么、什么参数）
2. **新概念解释**（用生活类比）
3. **常见报错对照**
4. **一个完整示例的"读法"**

**你先看卡，再看代码。** 如果卡里漏了什么，随时告诉我，我补上。
