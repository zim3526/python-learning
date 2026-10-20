# Day 6 弱项题（针对你的实际盲点）

> **出题依据**：你今天答错的、说"不懂"的、以及反复踩的坑。
> **规则**：先自己答，再看文末答案。**不要查资料，凭理解答。**
> **"不知道"是有效答案** —— 它比瞎猜有用。

---

# 第一部分：概念迁移（换个场景你还能认出它吗）

## 第 1 题

**你的项目现在用 DeepSeek。如果客户要求换成阿里通义千问，你最少要改代码里的哪几个地方？**

（提示：与你今天学的两个参数有关）

---

## 第 2 题

**你要做一个"中文翻译成英文"的机器人。下面两种写法，哪个更好？为什么？**

**写法 A**：
```python
messages = [
    {"role": "system", "content": "你是一个翻译，把用户的中文翻译成英文，只输出译文"},
    {"role": "user", "content": "今天天气很好"},
]
```

**写法 B**：
```python
messages = [
    {"role": "system", "content": "你是一个有用的助手"},
    {"role": "user", "content": "把下面这句话翻译成英文：今天天气很好"},
]
```

---

## 第 3 题

**你在 GitHub 上看到别人的项目，发现他把 API Key 直接写在代码里了。你提醒他，他说"我刚删掉那行代码重新提交了，应该没事了吧"。**

**他的做法够吗？为什么？应该怎么办？**

---

## 第 4 题

**下面这段代码，`client` 是什么？它和 `OpenAI` 是什么关系？**

```python
from openai import OpenAI
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
```

**追问**：`client.chat.completions.create(...)` 这一串里，**真正"执行动作"的是哪一部分？中间两段是干什么的？**

---

# 第二部分：代码判断（给代码，说结果）

## 第 5 题

**输入 `score = 70`，下面两段分别输出什么？**

**A**：
```python
if score > 60:
    print("及格")
else:
    print("不及格")
```

**B**：
```python
if score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

**再问**：如果输入 `score = 60`，A 和 B 分别输出什么？**这就是你反复踩的那个坑。**

---

## 第 6 题

**下面代码会打印几条进度？为什么？**

```python
import time

for i in range(3):
    print(f"进度 {i+1}/3")

for i in range(3):
    time.sleep(2)      # 模拟"干活"需要时间
```

**实际运行的用户体验是什么？应该怎么改？**（提示：你今天刚修过这个）

---

## 第 7 题

**下面代码会报什么错？**

```python
import json

text = '[1, 2, 3]'          # AI 返回了一个数组，不是对象
data = json.loads(text)
data["等级"] = "优秀"
```

**如果改成 `text = '{"评语": "不错"}'`，代码能跑通吗？**

---

## 第 8 题

**流式输出时，为什么 `response.usage` 拿不到？**

```python
response = client.chat.completions.create(..., stream=True)
print(response.usage.total_tokens)      # ← 报错
```

**如果一定要拿到 token 数，要加什么参数？加完之后，`usage` 出现在哪里？**

---

# 第三部分：找 bug（代码有错，指出来）

## 第 9 题

```python
def calc_level(score):
    if score > 90:
        return "优秀"
    elif score > 80:
        return "良好"
    elif score > 60:
        return "及格"
    else:
        return "不及格"

print(calc_level(90))     # 期望"优秀"，实际输出什么？
print(calc_level(60))     # 期望"及格"，实际输出什么？
```

---

## 第 10 题

```python
for chunk in response:                          # response 是流式对象
    delta = chunk.choices[0].delta.content
    print(delta, end="")
```

**这段代码有两个隐患，分别是什么？**

---

## 第 11 题

```python
messages = [{"role": "system", "content": "你是一个助手"}]

while True:
    q = input("你：")
    if q == "exit":
        break

    messages = [{"role": "user", "content": q}]        # ← 看这行

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
    )
    print(response.choices[0].message.content)
```

**这段代码看起来能跑，但有一个致命问题。是什么？**

---

# 第四部分：设计判断（这是 AI 应用开发的核心能力）

## 第 12 题

**需求**："输入一篇文章，输出**摘要** + **字数统计**"。

**字数统计该用 AI 还是 Python 代码？为什么？**

（提示：想想今天 `calc_level` 的教训）

---

## 第 13 题

**需求**："判断一条商品评论是**正面**还是**负面**"。

**下面三种方案，分别有什么优缺点？你会选哪个？**

| 方案 | 做法 |
|---|---|
| **A** | 关键词匹配：评论里出现"好"、"棒"就判正面 |
| **B** | 用 AI：让模型判断并返回 JSON `{"情感": "正面/负面"}` |
| **C** | 用 AI 判断 + 在 prompt 里给出 5 个正面和 5 个负面的例子 |

---

## 第 14 题

**你的同事写了一个 `main.py`，里面第一行是：**

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxxxx", base_url="https://api.deepseek.com")
```

**这个文件有什么问题？（至少说出两个）**

---
---

# 参考答案

---

## 第 1 题

**最少改 2 处**：

| 改哪 | 从 | 到 |
|---|---|---|
| **`base_url`** | `https://api.deepseek.com` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **`model`** | `deepseek-flash` | `qwen-plus`（或通义的模型名） |

**为什么只改这两处**：因为通义也"兼容 OpenAI 接口"，**同一个 `openai` 库、同样的 `messages` 结构都能用** —— 这叫**接口标准化的好处**。

**⚠️ 如果通义有私有参数**，还要改 `extra_body` 里的内容。

**这题考的是**：你是否理解 `base_url` 和 `model` 的作用。

---

## 第 2 题

**写法 A 更好。**

**原因**：**`system` 是"设定身份"，`user` 是"给任务"。**

| 写法 | 问题 |
|---|---|
| **A** | 一开始就告诉 AI"你是一个翻译" → **后续每一轮它都保持翻译身份** |
| **B** | 每轮都要在 `user` 里重复说"翻译成英文" → **啰嗦，而且容易被后续对话带偏** |

**更深一层**：`system` 的优先级最高，**它定义的是"这个 AI 是谁"**；`user` 定义的是"这次要干什么"。

**如果做多轮翻译**：
- A 的方式：之后用户直接发中文，AI 自动翻译 ✅
- B 的方式：用户每次都得说"翻译：xxx" ❌

---

## 第 3 题

**不够。**

**原因**：**Git 是"版本历史"** —— 你删掉代码再提交，**旧版本还在 `.git` 里**，`git log` 能看到，别人也能 `git checkout` 出那个版本。

**正确做法（顺序很重要）**：

| 步骤 | 做什么 |
|---|---|
| **1** | **立刻去平台作废这个 Key，重新生成**（最重要，先止损） |
| 2 | 把新 Key 放进 `.env`，加进 `.gitignore` |
| 3 | （可选）清理 Git 历史（`git filter-repo` 或 BFG）—— 但**Key 必须已经作废** |

**为什么第 1 步最重要**：**清理历史很麻烦，而且网上已经有爬虫扫过了。作废 Key 是唯一能真正止损的动作。**

**这题考的是**：你是否理解"Git 历史删不掉"和"止损优先"。

---

## 第 4 题

**`client` 是"对象"（实例），`OpenAI` 是"类"（设计图）。**

```
OpenAI                  → 类（设计图），不能直接用
OpenAI(api_key=..., ...) → 对象（造好的成品），能用
client = ...            → 把成品存进变量
```

**类比**：`OpenAI` 是**汽车设计图**，`client` 是**一辆能开的车**。

**追问的答案**：

```python
client.chat.completions.create(...)
  │      │        │        │
  │      │        │        └─ ⭐ 真正执行动作的：create()
  │      │        └─ 中间：定位到"文字生成"功能
  │      └─ 中间：定位到"对话"功能
  └─ 起点：客户端对象
```

**类比"写地址"**：中国 → 广东省 → 深圳市 → 具体门牌号
- `client` = 中国（大范围）
- `.chat` = 广东省
- `.completions` = 深圳市
- `.create()` = **门牌号（真正到达目的地）**

**这题考的是**：你是否理解了那串"点号"的含义（你之前完全不懂）。

---

## 第 5 题

**`score = 70`**：
- A：`70 > 60` 真 → **"及格"**
- B：`70 >= 80` 假 → `70 >= 60` 真 → **"及格"**

**`score = 60`**：
- A：`60 > 60` **假** → **"不及格"** ❌
- B：`60 >= 80` 假 → `60 >= 60` **真** → **"及格"** ✅

**这就是"边界"**：

| 运算符 | 60 分的结果 |
|---|---|
| `> 60` | ❌ 不及格（错了） |
| `>= 60` | ✅ 及格 |

**你今天就是在这里栽了三次。** 记住：**"及格线是 60 分"意思是"60 分及以上及格"，所以用 `>=`。**

---

## 第 6 题

**会打印 3 条进度，而且瞬间全部打印完，然后静默 6 秒。**

**为什么**：**代码是顺序执行的** —— 第一个 `for` 循环跑完（3 次打印，几乎瞬间）才进入第二个循环（真正干活，每次 2 秒）。

**用户体验**：

```
进度 1/3
进度 2/3
进度 3/3
[然后 6 秒什么都看不到，用户以为卡死]
```

**正确改法：合并成一个循环**

```python
for i in range(3):
    print(f"进度 {i+1}/3")
    time.sleep(2)       # 打印完立刻干活
```

**效果**：

```
进度 1/3
[等 2 秒]
进度 2/3
[等 2 秒]
进度 3/3
```

**这题考的是**：**"顺序执行"和"循环的意义"** —— 你今天的 `generate_all_comments` 就是这个 bug。

---

## 第 7 题

**报错**：

```
TypeError: list indices must be integers or slices, not str
```

**翻译**："列表只能用整数下标，不能用字符串。"

**原因**：`json.loads('[1,2,3]')` 得到的是**列表**，不是字典。**列表不能用 `data["等级"]` 这种字符串键取值。**

**改成 `text = '{"评语": "不错"}'` 后**：
- `json.loads` 得到字典 ✅
- `data["等级"] = "优秀"` 能跑通 ✅（给字典加新键）
- 但结果会变成 `{"评语": "不错", "等级": "优秀"}` —— **缺少"建议"字段**

**这题考的是**：**JSON 对象（`{}`）和 JSON 数组（`[]`）的区别**，以及"AI 返回的可能是数组"这个风险。

---

## 第 8 题

**为什么拿不到**：**流式模式下服务端"边生成边发"** —— 发到一半时它自己也不知道总共用了多少 token，所以 Stream 对象没有 `usage`。

**要加的参数**：

```python
stream_options={"include_usage": True}
```

**加完之后**：`usage` 会出现在**最后一个 chunk** 上。

**代码怎么拿**：

```python
usage = None
for chunk in response:
    if chunk.usage:              # ⭐ 最后一个 chunk 才有
        usage = chunk.usage
    if chunk.choices:            # 防统计包（choices 可能是空的）
        ...

print(usage.total_tokens)
```

**这题考的是**：**流式的"增量"本质** —— 你之前说"不知道为什么这么写"，根源在这里。

---

## 第 9 题

```python
print(calc_level(90))     # 实际输出：良好    ❌ 期望"优秀"
print(calc_level(60))     # 实际输出：不及格  ❌ 期望"及格"
```

**原因**：`>` 应该是 `>=`。

```
90 > 90  → False → 进入 elif 90 > 80 → True → 返回"良好"
60 > 60  → False → 进入 elif 60 > 80 → False → elif 60 > 60 → False → else → "不及格"
```

**修法**：

```python
if score >= 90:
elif score >= 80:
elif score >= 60:
```

**这题就是你今天犯的那个错**，再考一次是因为**它很重要**。

---

## 第 10 题

**两个隐患**：

### 隐患 1：统计包会让 `choices[0]` 崩

```python
delta = chunk.choices[0].delta.content
```

**统计包的 `choices` 可能是空列表**（OpenAI 风格）→

```
IndexError: list index out of range
```

**修法**：`if chunk.choices:`

### 隐患 2：`delta.content` 可能是 `None`

```python
print(delta, end="")
```

**当 `delta` 是 `None` 时**，`print(None)` 会打印出字面的 **"None"** 四个字符（不报错，但输出脏数据）。

**修法**：`if delta:`

**正确写法**：

```python
for chunk in response:
    if chunk.choices:                          # 防空箱子
        delta = chunk.choices[0].delta.content
        if delta:                              # 防 None
            print(delta, end="", flush=True)
```

**这题考的是**：**两层 `if` 各自在防什么** —— 你之前说"不知道"的地方。

---

## 第 11 题

**致命问题**：

```python
messages = [{"role": "user", "content": q}]      # ❌ 用 = 覆盖了历史
```

**每次循环都把 `messages` 整个换掉**，历史全部丢失 → **AI 永远"失忆"**。

**正确写法**：

```python
messages.append({"role": "user", "content": q})   # ✅ 追加
```

**而且还有第二个问题**：**没有把 AI 的回答 append 进去**，所以下一轮看不到上一轮的回答。

**完整正确写法**：

```python
messages.append({"role": "user", "content": q})
response = client.chat.completions.create(...)
answer = response.choices[0].message.content
messages.append({"role": "assistant", "content": answer})     # 别忘
```

**这题考的是**：**`append` vs `=`** —— 你今天第一次答错的地方（"覆盖"）。

---

## 第 12 题

**字数统计用 Python 代码。**

```python
def count_words(text):
    return len(text)
```

**为什么**：

| 理由 | 说明 |
|---|---|
| **准确性** | `len(text)` 100% 准确；AI 数数**经常出错** |
| **成本** | 0 元 vs 几百 tokens |
| **速度** | 瞬间 vs 1-3 秒 |
| **可测试** | `assert count_words("你好") == 2` |

**核心原则**：

> **能用规则算的，不要交给 AI。**

**正确的整体设计**：

```python
def analyze_article(text):
    word_count = len(text)              # ① 代码算（确定性）
    summary = ai_summarize(text)        # ② AI 写（语言能力）
    return {"摘要": summary, "字数": word_count}
```

**这题考的是**：**"确定性 vs AI"的分工** —— 今天最重要的一课。

---

## 第 13 题

| 方案 | 优点 | 缺点 |
|---|---|---|
| **A（关键词）** | 快、免费、完全可控 | **"一点都不好"会被判成正面**（因为含"好"）；反讽、复杂表达完全失效 |
| **B（纯 AI）** | 理解语义、能处理复杂表达 | **不稳定**（同一句话可能答不同）；**成本**；**没有明确标准** |
| **C（AI + 少样本示例）** | ⭐ **最稳定**：给了例子，AI 会"照着标准"判断 | 比 B 多写几行 prompt |

**推荐 C**，理由：

**"少样本示例"（few-shot）是 prompt 工程的核心技巧** —— **给 AI 5 个正面和 5 个负面的例子**，它就知道"你的标准是什么"，比纯描述准确得多。

**示例 prompt**：

```
判断评论情感，只输出 JSON {"情感": "正面"} 或 {"情感": "负面"}

示例：
"质量很好，物流快" → {"情感": "正面"}
"一点都不好，全是毛病" → {"情感": "负面"}
"还行吧，凑合用" → {"情感": "正面"}
"包装破了，东西也坏了" → {"情感": "负面"}
```

**这题考的是**：**什么时候用 AI、怎么让 AI 判断更可靠**。

---

## 第 14 题

**至少四个问题**：

### ① Key 泄露风险（最严重）

```python
client = OpenAI(api_key="sk-xxxxx", ...)     # ❌ 硬编码
```

**Key 写死在代码里** → 一旦提交到 Git，**永久留在历史记录里**。

**应该**：`os.getenv("DEEPSEEK_API_KEY")` + `.env` + `.gitignore`

### ② 违反分层

```python
# main.py
from openai import OpenAI                      # ❌ 界面层不该碰 AI 细节
```

**应该**：`main.py` 只 `from ai import generate_all_comments`，**完全不认识 `openai`**。

### ③ 没有检查 Key 是否存在

```python
client = OpenAI(api_key="sk-xxxxx", ...)      # 没有 if not api_key: 检查
```

**如果环境变量没读到**，会在后面报一个莫名其妙的错，而不是清楚的"没配置 Key"。

### ④ 客户端创建位置不对

**如果 `main.py` 里创建 `client`，那 `logic.py` 想用 AI 就得从 `main` 导入** → **循环依赖**。

**应该**：`client` 由 `ai.py` 内部创建（模块私有）。

**这题考的是**：**分层的实际意义** 和 **安全习惯**。

---

# 自评表

| 题号 | 主题 | 你的结果 |
|---|---|---|
| 1 | `base_url` 和 `model` | ⬜ 对 ⬜ 错 |
| 2 | `system` 的意义 | ⬜ 对 ⬜ 错 |
| 3 | Key 泄露的正确处理 | ⬜ 对 ⬜ 错 |
| 4 | 类 vs 对象、链式调用 | ⬜ 对 ⬜ 错 |
| 5 | `>` vs `>=` 边界 | ⬜ 对 ⬜ 错 |
| 6 | 顺序执行、进度条 | ⬜ 对 ⬜ 错 |
| 7 | JSON 对象 vs 数组 | ⬜ 对 ⬜ 错 |
| 8 | 流式拿 usage | ⬜ 对 ⬜ 错 |
| 9 | 找边界 bug | ⬜ 对 ⬜ 错 |
| 10 | 流式两层 if | ⬜ 对 ⬜ 错 |
| 11 | append vs 覆盖 | ⬜ 对 ⬜ 错 |
| 12 | 字数统计该谁做 | ⬜ 对 ⬜ 错 |
| 13 | 少样本、AI 适用场景 | ⬜ 对 ⬜ 错 |
| 14 | 分层与安全 | ⬜ 对 ⬜ 错 |

**任何一项打"错"，都把那题的解析再看一遍。**
