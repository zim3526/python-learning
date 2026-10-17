# Day 4 知识总结：文件读写、JSON 与数据持久化

> 学习日期：2026-10-15
> 产出：`file_basic.py`、`json_basic.py`、`grade_manager3.py`（带持久化 + 删除功能）
> 核心主题：**让数据活过程序的生命周期**

---

# 目录

1. [今天要解决的问题](#一今天要解决的问题)
2. [文件读写三个步骤](#二文件读写三个步骤)
3. [三个模式的区别](#三三个模式的区别重要)
4. [`with` 为什么必须用](#四with-为什么必须用)
5. [`encoding="utf-8"` 不能省](#五encodingutf-8-不能省)
6. [JSON：存字典和列表的标准格式](#六json存字典和列表的标准格式)
7. [为什么 JSON 不能用追加模式](#七为什么-json-不能用追加模式)
8. [内存 ↔ 文件模型（核心心智模型）](#八内存--文件模型核心心智模型)
9. [异常处理：该抓哪个异常](#九异常处理该抓哪个异常)
10. [pop 和 del 的区别](#十pop-和-del-的区别)
11. [今天踩过的坑](#十一今天踩过的坑)
12. [自测题](#十二自测题先自己做再看答案)
13. [Day 5 预告](#十三day-5-预告)

---

# 一、今天要解决的问题

## 症状

昨天的成绩管理系统：**录入数据 → 退出 → 重新运行 → 数据全没了。**

```
程序运行中：scores = {"张三": 85}  →  存在内存（RAM）
程序退出后：内存被释放             →  数据消失
```

## 原因

**数据只存在内存里，而内存是"临时的"。**

| 存储位置 | 特点 |
|---|---|
| **内存（RAM）** | 快，但**程序一结束就清空** |
| **硬盘（文件）** | 慢，但**断电也在** |

## 解决方案：持久化

```
程序启动：读文件 → 数据进内存
用户操作：改内存里的数据
操作完成：写回文件
程序退出：文件还在硬盘上
下次启动：又能读回来
```

---

# 二、文件读写三个步骤

## 读文件

```python
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 读全部内容，返回字符串
    print(content)
```

**逐部分拆解**：

| 部分 | 含义 |
|---|---|
| `open(...)` | 打开文件的函数 |
| `"data.txt"` | **文件路径**（相对于当前工作目录） |
| `"r"` | **模式**：r = read |
| `encoding="utf-8"` | ⚠️ 编码，中文必须指定 |
| `as f` | 把文件对象叫 `f` |
| `f.read()` | 读全部内容 |

## 写文件

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")          # ⚠️ 不会自动加换行，要自己写 \n
    f.write("第二行\n")
```

## 逐行读（最常用）

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:                     # 文件对象可以直接遍历
        print(line.strip())            # .strip() 去掉行尾换行符
```

**为什么要 `.strip()`**：

```python
print(line)            # 文件里的 \n + print 自带的换行 = 多一个空行
print(line.strip())    # ✅ 干净
```

## 逐行读 + 编号：`enumerate()`

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):        # 1 表示从 1 开始数
        print(f"{i}: {line.strip()}")
```

**`enumerate` 的作用**：**遍历时顺便编号。**

**和手动计数对比**：

```python
# 手动（也能用，但啰嗦）
num = 0
for line in f:
    num += 1
    print(f"{num}：{line.strip()}")

# enumerate（简洁）
for num, line in enumerate(f, 1):
    print(f"{num}：{line.strip()}")
```

---

# 三、三个模式的区别（重要）

| 模式 | 含义 | 文件已存在时 | 文件不存在时 |
|---|---|---|---|
| `"r"` | 读 | 正常读 | ❌ **报错 `FileNotFoundError`** |
| `"w"` | 写 | ⚠️ **清空原内容，从头写** | ✅ **自动创建文件** |
| `"a"` | 追加 | 在末尾接着写 | ✅ 自动创建文件 |

## 🔴 `"w"` 是危险的

```python
with open("重要数据.txt", "w") as f:
    f.write("新内容")
```
**文件里原来的所有内容都被清空了！**

**想保留原内容 → 用 `"a"`。**

## ⭐ `"w"` 会自动创建文件（今天是重点）

**这就是"程序能自动创建 json 文件"的原理**：

```python
with open("全新的文件.json", "w", encoding="utf-8") as f:
    f.write("{}")
# 文件不存在也没关系，open 会创建它
```

**所以持久化程序的设计是**：
- **读的时候**：文件可能不存在 → 用 `try/except` 接住 → 返回空数据
- **写的时候**：用 `"w"` → 自动创建文件

---

# 四、`with` 为什么必须用

```python
# ❌ 不用 with（要手动关闭）
f = open("data.txt", "r", encoding="utf-8")
content = f.read()
f.close()                    # 忘了这行会怎样？

# ✅ 用 with（自动关闭）
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
# 出了 with 块，文件自动关闭
```

| 情况 | 不用 `with` | 用 `with` |
|---|---|---|
| 忘了 `close()` | 文件一直占用，可能丢数据 | ✅ 自动关闭 |
| 中途报错崩了 | **文件不会关闭**，可能损坏 | ✅ **依然自动关闭** |

**结论**：**读写文件永远用 `with`，没有例外。**

---

# 五、`encoding="utf-8"` 不能省

```python
open("data.txt", "r")                       # ❌ Windows 上默认用 GBK → 中文乱码
open("data.txt", "r", encoding="utf-8")     # ✅
```

**原因**：**Windows 中文系统的默认编码是 GBK，不是 UTF-8。**

**这跟 Day 1 的环境坑是同一个病根。**

**记法**：**只要文件里可能有中文，就必须写 `encoding="utf-8"`。**

## 一个有趣的事实：Python 会规范化编码名

**实测结果**：

```
'utf-8'        → OK
'utf -8'       → OK    ← 带空格也行！
'utf 8'        → OK
'UTF-8'        → OK
'utf_8'        → OK
'  utf-8  '    → OK

'utf-9'        → LookupError: unknown encoding: utf-9     ← 只有真不存在的名字才报错
'uft-8'        → LookupError: unknown encoding: uft-8
```

**Python 会主动去掉空格、把连字符转下划线、转小写，然后才查表。**

**验证方法**：
```python
import codecs
print(codecs.lookup("utf -8"))      # <codecs.CodecInfo object for encoding utf-8>
print(codecs.lookup("utf_8"))
```

**这个知识点的价值不在于"能写错"，而在于**：
> **任何人（包括老师、AI、同事）说"这里有问题"，你都要先跑一遍验证。**

---

# 六、JSON：存字典和列表的标准格式

## 为什么不用普通文本存字典

```python
# ❌ 自己拼字符串
for name, score in scores.items():
    f.write(f"{name},{score}\n")
```

| 问题 | 说明 |
|---|---|
| 读回来要自己解析 | 按逗号切开 |
| 数据里有逗号怎么办 | `"张,三"` → 切分就错了 |
| 有嵌套结构怎么办 | 完全处理不了 |

## JSON 是什么

**JSON（JavaScript Object Notation）**：一种**通用的数据格式**，长得跟 Python 的字典/列表几乎一样。

```json
{
  "张三": 85,
  "李四": 92
}
```

**好处**：
- **Python 字典 → JSON 文本 → 文件**，读回来还是字典
- **所有编程语言都支持**
- **API 传输数据都用它**（Day 6 调 AI 接口会大量见到）

## 四个函数

```python
import json

# ① Python 对象 → JSON 字符串
text = json.dumps({"张三": 85})
print(text)                    # {"张三": 85}

# ② JSON 字符串 → Python 对象
data = json.loads('{"张三": 85}')
print(data)                    # {'张三': 85}
print(type(data))              # <class 'dict'>

# ③ Python 对象 → 文件  ⭐ 最常用
with open("scores.json", "w", encoding="utf-8") as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

# ④ 文件 → Python 对象  ⭐ 最常用
with open("scores.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

## 记忆法：带 `s` 的操作字符串

| 函数 | 操作对象 | 记忆 |
|---|---|---|
| `json.dumps` | **字符串** | 有 s = **s**tring |
| `json.loads` | **字符串** | 有 s = **s**tring |
| `json.dump` | **文件** | 无 s = 直接对文件 |
| `json.load` | **文件** | 无 s = 直接对文件 |

## 🔴 `ensure_ascii=False` 必须加

```python
json.dump(data, f)                            # 中文变成 \u5f20\u4e09
json.dump(data, f, ensure_ascii=False)        # ✅ 中文正常显示
```

| 写法 | 文件内容 |
|---|---|
| `ensure_ascii=True`（默认） | `{"\u5f20\u4e09": 85}` |
| `ensure_ascii=False` | `{"张三": 85}` |

**记法**：**`ensure_ascii=False` = "别用 ASCII 转义，直接写中文"。**

## `indent=2` 让文件好读

```python
json.dump(data, f, ensure_ascii=False)                # 全挤在一行
json.dump(data, f, ensure_ascii=False, indent=2)      # ✅ 缩进 2 空格
```

**对比**：

```json
{"张三": 85, "李四": 92}          ← 挤在一行
```

```json
{
  "张三": 85,
  "李四": 92
}
```
**加了才好读**（也方便你手动检查数据）。

---

# 七、为什么 JSON 不能用追加模式

## 错误尝试

```python
with open("scores.json", "a", encoding="utf-8") as f:
    json.dump({"陈七": 90}, f)          # 想"追加"一个人
```

## 结果

```json
{
  "张三": 85
}{
  "陈七": 90
}
```

**两个 JSON 对象粘在一起了 —— 这不是合法 JSON，再读会报 `JSONDecodeError`。**

## 原因

> **JSON 文件是一个"完整的结构"，不是"一行一条记录"的流水账。**
> **你没法往一个完整结构里"插一块"** —— 必须整个重新写。

## 对比两种存数据的方式

| 格式 | 适合 | 能不能追加 |
|---|---|---|
| `.txt` / `.log` / `.csv` | 一行一条记录（日志、流水） | ✅ `"a"` 能追加 |
| **`.json`** | **一个完整的数据结构** | ❌ **必须整个重写** |

## 正确做法

```python
scores["陈七"] = 90                                      # ① 先改内存里的字典

with open("scores.json", "w", encoding="utf-8") as f:     # ② 整个重写文件
    json.dump(scores, f, ensure_ascii=False, indent=2)
```

**"先改内存，再整体写回文件"** —— 这是操作 JSON 数据的标准套路。

---

# 八、内存 ↔ 文件模型（核心心智模型）

## 数据流

```
  文件（硬盘）  ──load──>  内存里的字典  ──用户操作──>  修改字典  ──save──>  整个重写文件
```

## 各时刻数据在哪

| 时刻 | 数据在哪 |
|---|---|
| 程序启动 | 文件 → **读进内存**（只读一次） |
| 用户录入/删除 | **只改内存里的字典** |
| 每次修改后 | **把整个字典写回文件**（覆盖式重写） |
| 程序运行中查看 | 读内存，**不读文件** |

## 这个模型解释了两件事

**① 为什么性能没问题**
只在**启动**和**保存**时碰文件，不会每次查看都读盘。

**② 为什么"改了不保存"会丢数据**
你在内存里改的，**没调 `save_scores` 就丢了**。这就是为什么每次录入/删除后都要立刻存。

## 🔴 核心规律

> **每一次修改数据，都要立刻保存。**

**这就是为什么 `main` 里要这样写**：

```python
if choice == "1":
    input_score(scores)
    save_scores(scores, FILENAME)      # ⭐ 录完就存

elif choice == "5":
    delete_score(scores)
    save_scores(scores, FILENAME)      # ⭐ 删完就存
```

**如果删除后忘了保存**：
1. 你在内存里删掉了
2. **但文件里还在**
3. 下次运行 → `load_scores` 读回来 → **被删的人又回来了！**

**这叫"内存和文件不同步"，是很典型的 bug。**

## 这个模型的普适性

> 以后所有涉及数据存储的东西都是这个模式的变体：
> - **数据库**（内存缓存 ↔ 磁盘）
> - **Redis**（内存 ↔ 持久化文件）
> - **云存储**（本地 ↔ 远程）

---

# 九、异常处理：该抓哪个异常

## 今天的问题

```python
def load_scores(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileExistsError:          # ❌ 抓错了
        return {}
```

**实际报的错**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'scores2.json'
```

**抓的是 `FileExistsError`，报的是 `FileNotFoundError`** —— **这俩是相反的意思！**

| 异常 | 什么时候发生 |
|---|---|
| `FileNotFoundError` | **文件不存在**（用 `"r"` 打开时） |
| `FileExistsError` | 文件已存在（用 `"x"` 模式创建时） |

## 正确写法

```python
def load_scores(filename):
    """从文件读取成绩数据。文件不存在或损坏时返回空字典。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}                        # 第一次运行，文件还没建
    except json.JSONDecodeError:
        print("数据文件损坏，将从空数据开始")
        return {}
```

**两个必须处理的异常**：

| 异常 | 什么时候发生 | 为什么必须处理 |
|---|---|---|
| `FileNotFoundError` | **第一次运行程序时** | 不处理就直接崩溃 |
| `json.JSONDecodeError` | 文件内容不是合法 JSON | 用户可能手动改坏了 |

## 经验

> **`except` 抓的异常名，必须和实际抛出的异常名一致。**
> **不确定就故意触发一次，看报错里写的是什么。**

---

# 十、`pop` 和 `del` 的区别

## 核心区别

```python
del scores["张三"]        # 只删，不交出任何东西
scores.pop("张三")        # 删 + 把被删的值交出来（返回值）
```

## `pop` 干了**两件事**

```
scores.pop("张三")
        │
        ├─── ① 把 "张三" 这个键值对从字典里【删掉】
        │
        └─── ② 把被删掉的【值】85 交出来（作为返回值）
                    │
                    └── 你用变量接住 → 85 就保存了
                        你不接         → 85 就没了
```

## 亲手验证

```python
scores = {"张三": 85, "李四": 92}

# 实验 1：接住返回值
deleted = scores.pop("张三")
print(f"deleted 变量接到了：{deleted}")     # 85
print(f"现在的字典：{scores}")               # {'李四': 92}

# 实验 2：不接返回值
scores["王五"] = 78
scores.pop("王五")                          # 返回值没人接
print(f"现在的字典：{scores}")               # {'李四': 92}
# 78 去哪了？→ 没有任何变量指向它，被自动回收了
```

## "消失的值"到底去哪了

| 步骤 | 发生什么 |
|---|---|
| 1 | `pop` 从字典里移除这个键值对 |
| 2 | 返回值被临时放在"栈"上 |
| 3 | 因为**没有任何变量指向它**，也没被使用 |
| 4 | Python 的**垃圾回收**把它清理掉 |

**变量是一个"名字标签"，贴在值上面。**
**没有任何标签贴着的值，就会被自动清理掉。**

```python
x = 100          # 100 被 x 指着 → 活着
x = 200          # 100 没人指着了 → 被回收；200 被 x 指着 → 活着
```

## 和 Day 3 的 `print` / `return` 是同一件事

```python
def print_sum(a, b):
    print(a + b)         # 只是"喊了一声"，交不出东西

def return_sum(a, b):
    return a + b         # 把值"交出来"

r1 = print_sum(1, 2)     # → None（交不出来）
r2 = return_sum(1, 2)    # → 3
```

> **`pop()` 就像一个"会 return 的函数"** —— 它把值交出来。
> **你接不接是你的事；它交不交是它的事。**

## 用 `pop` 的正确姿势

```python
def delete_score(scores):
    del_name = input("姓名：")
    if del_name in scores:
        deleted = scores.pop(del_name)                     # ⭐ 接住
        print(f"已删除 {del_name} 的成绩（{deleted} 分）")    # ⭐ 用起来
    else:
        print("查无此人")
```

**运行效果**：
```
姓名：张三
已删除 张三 的成绩（85 分）      ← 比只显示"已删除"信息更完整
```

**这就是"接住返回值"的实际价值**：**能告诉用户"删掉了什么"。**

---

# 十一、今天踩过的坑

| # | 坑 | 现象 | 原因 | 解法 |
|---|---|---|---|---|
| 1 | **JSON 用 `"a"` 追加** | 两个 JSON 对象粘在一起 | JSON 是完整结构，不能追加 | 改内存后整体重写 |
| 2 | **`write()` 传字典** | `TypeError: write() argument must be str, not dict` | 把文件对象当 `json.dump` 用 | 用 `json.dump` 或 `str()` |
| 3 | **`except` 抓错异常** | `FileNotFoundError` 没被接住，程序崩溃 | 写成了 `FileExistsError`（意思相反） | 抓 `FileNotFoundError` |
| 4 | **不加 `ensure_ascii=False`** | JSON 里中文变成 `\u5f20\u4e09` | 默认会用 ASCII 转义 | 加 `ensure_ascii=False` |
| 5 | **删除后忘了保存** | 重启后被删的人又回来了 | 内存和文件不同步 | 每次修改后都 `save_scores` |
| 6 | **不加 `encoding`** | 中文乱码 | Windows 默认 GBK | `encoding="utf-8"` |

---

# 十二、自测题（先自己做，再看答案）

## A. 判断输出 / 找问题

**1. 这个文件写入后，文件里有几行？**
```python
with open("t.txt", "w", encoding="utf-8") as f:
    f.write("A")
    f.write("B")
    f.write("C")
```

**2. 运行两次下面的代码，文件里有什么？**
```python
with open("t.txt", "w", encoding="utf-8") as f:
    f.write("第一次\n")
```
再运行：
```python
with open("t.txt", "w", encoding="utf-8") as f:
    f.write("第二次\n")
```

**3. 改成 `"a"` 模式呢？**
```python
with open("t.txt", "a", encoding="utf-8") as f:
    f.write("第二次\n")
```

**4. 这段代码报什么错？**
```python
with open("不存在.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

**5. 这段代码输出的 JSON 长什么样？**
```python
import json
data = {"张三": 85}
print(json.dumps(data))
```

**6. 下面这段读文件的代码，哪个异常该被抓？**
```python
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

**7. 这个函数的 bug 在哪？**
```python
def load_scores(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileExistsError:
        return {}
```

**8. `pop` 之后，值去哪了？**
```python
scores = {"张三": 85}
scores.pop("张三")
print(scores)
```

**9. 这段代码能拿到被删除的值吗？**
```python
scores = {"张三": 85}
scores.pop("张三")
print(f"删掉了 {???} 分")
```

**10. 学生成绩管理程序：用户删除了"张三"，然后没退出程序就断电了。重启后张三还在吗？为什么？**

---

## 参考答案

**1.** **一行**：`ABC`
> `f.write()` **不会自动加换行**，三次写入连在一起了。要分行必须自己写 `\n`。

**2.** 只有 `第二次`
> `"w"` 模式会**清空原内容**再写。

**3.** 两行：`第一次` 和 `第二次`
> `"a"` 模式在**末尾追加**，不清空。

**4.** `FileNotFoundError: [Errno 2] No such file or directory: '不存在.txt'`
> 用 `"r"` 打开不存在的文件会报这个错。

**5.** `{"\u5f20\u4e09": 85}`
> 因为默认 `ensure_ascii=True`，中文被转义了。加 `ensure_ascii=False` 才会输出 `{"张三": 85}`。

**6.** 两个都要抓：
- `FileNotFoundError` —— 文件不存在
- `json.JSONDecodeError` —— 文件内容不是合法 JSON

**7.** `except FileExistsError` 抓错了，应该是 **`FileNotFoundError`**
> 这俩意思相反：`FileExistsError` 是"文件已存在"，`FileNotFoundError` 是"文件不存在"。

**8.** 输出 `{}`（空字典）
> `pop` 返回值没被接住，值 85 被垃圾回收了。

**9.** 接住返回值就行：
```python
scores = {"张三": 85}
deleted = scores.pop("张三")
print(f"删掉了 {deleted} 分")
```

**10.** **张三还在**（如果删除后没调 `save_scores`）
> 因为删除只改了**内存**，没写回**文件**。程序一结束，内存被清空，文件里还是老数据。
> **修改数据后必须立刻 `save_scores`。**

---

# 十三、Day 5 预告

## 主题：模块化 + 路径处理

**要解决的痛点**：

**① 代码越写越长**
`grade_manager3.py` 已经 130 行了。如果把整个项目都塞进一个文件，很快会到 1000 行、没法维护。

**解决**：把代码拆成多个文件（模块），用 `import` 互相调用。

```python
# storage.py    ← 只管读写文件
# logic.py      ← 只管业务逻辑
# main.py       ← 只管界面和菜单
```

**这也是真实项目的组织方式。**

**② 路径问题**
```python
FILENAME = "scores.json"
```
**这个文件到底在哪？** 取决于你**从哪个目录运行程序**。这里有个经典的坑：

```powershell
cd D:\aistudy\day04
py grade_manager3.py       # scores.json 在 day04 里 ✅
```

```powershell
cd D:\aistudy
py day04/grade_manager3.py # scores.json 会被创建在 aistudy 里！⚠️
```

**Day 5 会学 `__file__` 和 `pathlib`，让程序"永远在自己所在的位置找文件"。**

## 其他内容

| 主题 | 说明 |
|---|---|
| `import` 自己写的模块 | `from storage import load_scores` |
| `if __name__ == "__main__"` 的真正用途 | 为什么拆模块时需要它 |
| `pathlib.Path` | 现代 Python 处理路径的方式 |

---

# 十四、今日成果

## 文件（`D:\aistudy\day04\`）

| 文件 | 内容 |
|---|---|
| `file_basic.py` | 文件读写练习 + `FileNotFoundError` |
| `json_basic.py` | JSON 存取 + 亲手踩了"不能用追加"的坑 |
| **`grade_manager3.py`** | ⭐ **持久化 + 删除功能（能存数据的真工具）** |
| `scores.json` / `scores2.json` | 程序生成的数据文件（**不应提交到 Git**）|

## 核心能力

| 能力 | 说明 |
|---|---|
| 文件读写 | `open()` / `read()` / `write()` / `with` |
| 三个模式 | `"r"` / `"w"` / `"a"` 的区别和风险 |
| **JSON 序列化** | `json.dump` / `json.load` / `ensure_ascii` / `indent` |
| **数据持久化** | 程序重启后数据还在 |
| **内存 ↔ 文件模型** | 理解数据在哪个位置，知道为什么要立刻保存 |
| 异常处理 | `FileNotFoundError` / `JSONDecodeError` |
| **`pop` vs `del`** | 返回值的作用和去向 |

## 里程碑

> **你的成绩管理系统从"玩具"变成了"真工具"。**
>
> **今天的分界线是**：Day 3 结束时它只是个"能跑的程序"，Day 4 结束时它**有了数据存储能力** —— 这是所有实用软件的基本特征。

## Git 历史

```
8eedf37  Day4: 文件读写 + JSON持久化 + 删除功能
f764ffe  Day3: 函数基础 + grade_manager 重构为函数版
f7a5cd3  Day1-2: Python 基础练习 + 学生成绩管理系统
```
