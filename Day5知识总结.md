# Day 5 知识总结：路径处理与模块化

> 学习日期：2026-10-17
> 产出：`path_test.py`、`storage.py`、`logic.py`、`main.py`（成绩管理系统拆分版）
> 核心主题：**让程序不依赖"你站在哪"，让代码不挤在一个文件里**

---

# 目录

1. [今天要解决的两个问题](#一今天要解决的两个问题)
2. [相对路径 vs 绝对路径](#二相对路径-vs-绝对路径)
3. [`__file__` 和 `os.getcwd()` 的区别](#三__file__-和-osgetcwd-的区别)
4. [`pathlib` 处理路径](#四pathlib-处理路径)
5. [模块化：把一个文件拆成三个](#五模块化把一个文件拆成三个)
6. [`import` 机制详解](#六import-机制详解)
7. [`if __name__ == "__main__"` 的真正意义](#七if-__name__-__main__-的真正意义)
8. [分层设计与依赖方向](#八分层设计与依赖方向)
9. [生成器表达式与 values()](#九生成器表达式与-values)
10. [今天踩过的坑](#十今天踩过的坑)
11. [自测题](#十一自测题先自己做再看答案)
12. [Day 6 预告：进入 AI 领域](#十二day-6-预告进入-ai-领域)

---

# 一、今天要解决的两个问题

## 问题 1：路径不可靠

Day 4 的成绩管理系统里：

```python
FILENAME = "scores.json"           # 相对路径
```

**从不同目录运行，文件落到不同地方**：

| 你在哪运行 | 文件落在哪 |
|---|---|
| `cd D:\aistudy\day04` → `py grade_manager3.py` | `D:\aistudy\day04\scores.json` ✅ |
| `cd D:\aistudy` → `py day04/grade_manager3.py` | **`D:\aistudy\scores.json`** ❌ 跑外面去了 |

**后果**：用户数据"神秘消失"（其实在另一个位置），程序读不到自己的数据。

## 问题 2：代码挤在一个文件

`grade_manager3.py` 已经 **130 行**。加上更多功能会到几百上千行 → 难维护、难复用、多人协作冲突多。

## 今天的解法

| 问题 | 解法 |
|---|---|
| 路径不可靠 | **`__file__` + `pathlib`**，让路径永远相对于脚本 |
| 代码挤在一起 | **模块化**，拆成 `storage.py` / `logic.py` / `main.py` |

---

# 二、相对路径 vs 绝对路径

| 类型 | 例子 | 相对于什么 |
|---|---|---|
| **相对路径** | `"scores.json"`、`"data/scores.json"` | **当前工作目录**（你在哪） |
| **绝对路径** | `"D:\aistudy\day04\scores.json"` | 完整的、唯一的地址 |

## 核心坑

> **相对路径参照的是"你站在哪"（`os.getcwd()`），而不是"脚本在哪"（`__file__`）。**

**这就是为什么同一个脚本、同样的代码，换个目录运行，文件就跑到别处去了。**

## 实测证据

```python
# path_demo.py（用相对路径）
with open("demo_output.txt", "w", encoding="utf-8") as f:
    f.write("...")
```

| 运行方式 | 文件位置 |
|---|---|
| `cd day05` → `py path_demo.py` | `day05\demo_output.txt` |
| `cd aistudy` → `py day05/path_demo.py` | **`aistudy\demo_output.txt`** |

---

# 三、`__file__` 和 `os.getcwd()` 的区别

```python
print(__file__)         # D:\aistudy\day05\path_test.py   脚本自己在哪
print(os.getcwd())      # D:\aistudy\day05                 你当前站哪
```

| 变量 | 含义 | 会不会变 |
|---|---|---|
| **`__file__`** | **脚本自己**的路径 | ❌ 永远指向脚本 |
| **`os.getcwd()`** | **你**当前所在目录 | ✅ 你在哪就变哪 |

**类比**：
- `__file__` = "我的身份证地址"（不变）
- `os.getcwd()` = "我现在站的地方"（会变）

## 关键结论

> **你要的永远是"脚本自己附近"→ 用 `__file__`。**

**特别注意**：`path_demo.py` 里 `__file__` 显示 `day05\path_demo.py`，但文件却落到了 `aistudy` —— **因为 `open()` 用的是相对路径字符串，它只认 `os.getcwd()`。**

---

# 四、`pathlib` 处理路径

## 标准写法

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent              # 脚本所在的目录
DATA_FILE = BASE_DIR / "scores.json"          # 拼出完整路径
```

**逐部分拆解**：

| 部分 | 含义 |
|---|---|
| `Path(__file__)` | 把脚本路径变成 `Path` 对象 |
| `.parent` | **上一层目录**（脚本所在的文件夹） |
| `BASE_DIR / "scores.json"` | ⭐ **`/` 用来拼接路径**（不是除法！） |

## 为什么用 `/` 而不是 `+`

```python
# ❌ 字符串拼接，平台相关
path = str(BASE_DIR) + "\\" + "scores.json"     # 只在 Windows 对

# ✅ pathlib，自动处理分隔符
path = BASE_DIR / "scores.json"                 # Windows / Linux 都对
```

**`/` 运算符作用在 `Path` 对象上就是"路径拼接"** —— 这是 `pathlib` 最优雅的设计。

## 常用操作

```python
p = Path(__file__).parent / "scores.json"

p.exists()      # 文件存在吗？True / False
p.name          # "scores.json"     文件名
p.suffix        # ".json"           扩展名
p.parent        # 上一层目录
str(p)          # 转成普通字符串
```

**`open()` 可以直接接受 `Path` 对象**，不用 `str()` 转换：

```python
with open(DATA_FILE, "r", encoding="utf-8") as f:      # ✅ 可以直接传 Path
```

## 🔴 最重要的一条（今天你踩的坑）

> **"算出了正确的路径"和"用了正确的路径"是两件事。**

**你的错误写法**：

```python
BASE_DIR = Path(__file__).parent          # 算出来了
TEST_DIR = BASE_DIR / "test_data.txt"     # 也算出来了

with open("test_data.txt", "w") as f:     # ❌ 但 open 用的是相对路径！
    f.write("...")
```

**正确写法**：

```python
BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "test_data.txt"

with open(TEST_DIR, "w") as f:            # ✅ 把变量传进 open
    f.write("...")
```

**为什么难发现**：`print(TEST_DIR)` 输出的是正确路径，**你会以为文件就写那儿了**，但 `open` 根本没用它。

---

# 五、模块化：把一个文件拆成三个

## 拆分结构

```
day05/
├── storage.py     ← 数据层：只管读写文件
├── logic.py       ← 逻辑层：只管计算和查询
├── main.py        ← 界面层：只管菜单和交互
├── scores.json    ← 数据文件
└── __pycache__/   ← Python 自动生成的缓存（已在 .gitignore 里）
```

## 各层职责

| 模块 | 放什么 | 类比 |
|---|---|---|
| **`storage.py`** | `load_scores` / `save_scores` | **仓库管理员**（管存取） |
| **`logic.py`** | `calc_stats` / `is_pass` / `find_by_name` | **会计**（管算账） |
| **`main.py`** | 菜单 / `input_score` / `show_all` / `show_stats` | **前台**（管接待） |

## 为什么这样分

> **每一层只关心自己的事。**
> - `storage` 不关心成绩怎么算，只管"存和取"
> - `logic` 不关心界面长什么样，只管"算出结果"
> - `main` 不关心文件怎么存，只管"问用户要什么"
>
> 这叫**分层设计**，是所有大型软件的通用做法。

## 实际代码

### `storage.py`

```python
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEFAULT_FILE = BASE_DIR / "scores.json"


def load_scores(filename=DEFAULT_FILE):
    """从文件读取成绩数据，返回字典。文件不存在或损坏时返回空字典。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("数据文件损坏，将从空数据开始")
        return {}


def save_scores(scores, filename=DEFAULT_FILE):
    """把成绩数据写入文件。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)
```

**新语法：默认参数**

```python
def load_scores(filename=DEFAULT_FILE):      # 不传就用 DEFAULT_FILE
```

- `load_scores()` → 用默认的 `scores.json`
- `load_scores("other.json")` → 用指定的

**好处**：调用更灵活；**而且默认值是在 `storage.py` 里算好的绝对路径，不受调用方所在目录影响。**

### `logic.py`

```python
def is_pass(score):
    """判断是否及格（>= 60）。"""
    return score >= 60


def find_by_name(scores, name):
    """查找某个学生的成绩。找到返回分数，找不到返回 None。"""
    return scores.get(name)


def calc_stats(scores):
    """计算统计结果。返回字典；空字典返回 None。"""
    if not scores:
        return None
    ...
```

**新方法：`dict.get()`**

```python
scores["张三"]          # ❌ 不存在 → KeyError
scores.get("张三")      # ✅ 不存在 → None（安全查询）
```

**这是"安全查询"的标准做法。**

**新语法：`if not scores:`**

```python
if not scores:          # 空字典/空列表在 Python 里算"假"
    return None
```

**等价于 `if len(scores) == 0:`，但更简洁。**

### `main.py`

```python
from storage import load_scores, save_scores
from logic import calc_stats, find_by_name


def main():
    scores = load_scores()          # ← 用默认路径

    while True:
        ...
        if choice == "1":
            input_score(scores)
            save_scores(scores)      # ← 也用默认路径


if __name__ == "__main__":
    main()
```

**注意**：`main.py` **完全不碰 `json`、不碰 `open`、不关心文件在哪** —— **这就是分层的好处。**

---

# 六、`import` 机制详解

## 三种导入方式

```python
# 方式一：导入整个模块
import storage
storage.load_scores()               # 调用时写模块名

# 方式二：导入具体函数（推荐）
from storage import load_scores, save_scores
load_scores()                        # 直接用

# 方式三：起别名
import storage as st
st.load_scores()
```

**推荐方式二** —— **最简洁清楚**，而且能看出用了哪些函数。

## 模块会放在哪

**`main.py` 运行时，Python 会在这些地方找 `storage`**：

1. **当前脚本所在的目录**（`day05/`）✅ 你的模块在这里
2. 已安装的第三方库里
3. Python 标准库

**所以 `main.py` 和 `storage.py` 必须放在同一个目录**（或者 `storage.py` 在 Python 能搜到的路径里）。

## ⚠️ 一个重要限制：工作目录不影响 import

| 操作 | 结果 |
|---|---|
| `cd day05` → `py -c "import main"` | ✅ 成功 |
| `cd aistudy` → `py -c "import main"` | ❌ `ModuleNotFoundError: No module named 'main'` |

**为什么**：`py -c` 的搜索路径是**当前目录**，不是脚本目录。

**但 `py day05/main.py` 能正常运行** —— 因为 Python 会把**被运行脚本的所在目录**加入搜索路径。

**这个区别你实测到了**（测试结果第 454-462 行）：

```
PS D:\aistudy> py -c "import main"
ModuleNotFoundError: No module named 'main'          ← 当前目录没 main.py

PS D:\aistudy\day05> py -c "import main"
导入成功，没有进入菜单                                 ← 当前目录有 main.py
```

---

# 七、`if __name__ == "__main__"` 的真正意义

## Day 3 时我说"这是规范写法，先记住"。今天它有了实际意义。

## 问题

当你运行 `main.py` 时，它 `import storage` → **Python 会把 `storage.py` 整个执行一遍**。

**如果 `storage.py` 末尾有这样一行**：

```python
def load_scores(...): ...
print("storage 模块加载完成")       # ← 每次 import 都会执行这行！
```

**那么每次 `import storage`，屏幕都会多一行输出。**

**所以**：**模块文件里不应该有"直接执行的代码"**（除非你希望它在被导入时执行）。

## 解决方案

```python
# main.py
def main():
    ...

if __name__ == "__main__":
    main()          # ← 只在"直接运行 main.py"时执行
```

| 场景 | `__name__` 的值 | `main()` 执行吗 |
|---|---|---|
| `py main.py` | `"__main__"` | ✅ 执行 |
| `import main`（被别处导入） | `"main"` | ❌ 不执行 |

## 实测验证（你的测试结果）

```
PS D:\aistudy\day05> py -c "import main; print('导入成功，没有进入菜单')"
导入成功，没有进入菜单
```

**只打印了"导入成功"，没有进入菜单** —— **`if __name__ == "__main__"` 生效了。**

## 记忆

> `__name__` = "我是怎么被使用的"
> - **直接运行它** → `"__main__"`
> - **被别人导入** → 文件名（如 `"main"`）

---

# 八、分层设计与依赖方向

## 单向依赖原则

```
main  →  logic  →  storage        ✅ 好的（单向依赖）

storage  →  main                 ❌ 坏的（循环依赖）
```

**口头记法**：**上层可以调用下层，下层不能调用上层。**

## 你的项目实际依赖

```
main.py
  ├── import storage   →  load_scores, save_scores
  └── import logic     →  calc_stats, find_by_name

storage.py  （不依赖任何模块）
logic.py    （不依赖任何模块）
```

**这是很干净的结构。**

## 🔴 但"造了工具要使用"（你今天漏掉的）

**问题**：你定义了 `find_by_name` 和 `is_pass`，但一开始没在 `main.py` 里用：

```python
# ❌ 界面层直接操作字典 = 越界了
def query_score(scores):
    if query_name in scores:
        print(scores[query_name])

# ✅ 用逻辑层的函数
def query_score(scores):
    score = find_by_name(scores, query_name)
    if score is None:
        print("查无此人")
    else:
        print(f"分数为：{score}")
```

**同理**，`calc_stats` 里的 `if s >= 60` 应该用 `is_pass(s)`：

```python
# ❌ 及格线写死了
if s >= 60:

# ✅ 用统一判断
if is_pass(s):
```

**为什么重要**：**及格线只应该在一个地方定义**。如果哪天改成 50 分及格，**只改 `is_pass` 一处就全对了**。

> **这叫"单一数据源"原则 —— 同一个规则不要写两遍。**

## 判断方法

> **你 `import` 了什么，就一定要用。**（VS Code 会把没用的 import 灰掉提示你）

---

# 九、生成器表达式与 values()

## `scores.values()` 返回的不是列表

```python
type(scores.values())        # <class 'dict_values'>
scores.values()              # dict_values([85, 92])
```

**它是"视图"（view），不是列表。**

| | 视图 `dict_values` | 列表 `list` |
|---|---|---|
| 能 `len()` 吗 | ✅ | ✅ |
| 能**索引** `[0]` 吗 | ❌ `TypeError: 'dict_values' object is not subscriptable` | ✅ |
| 能 `append()` 吗 | ❌ | ✅ |
| 原字典变了会怎样 | **跟着变**（实时视图） | **不变**（是拷贝） |

## 视图 vs 列表的经典对比

```python
scores = {"张三": 85}
view = scores.values()
snapshot = list(scores.values())

scores["李四"] = 92

print(view)        # dict_values([85, 92])    ← 跟着变了
print(snapshot)    # [85]                    ← 没变
```

**比喻**：

| | 视图 | 列表 |
|---|---|---|
| 像什么 | **一扇窗** | **一张照片** |
| 原数据变了 | 窗里内容跟着变 | 照片不变 |

## `list(...)` 的作用

> **把"一扇窗"拍成"一张照片"** —— 得到固定的、可索引、可修改的列表。

```python
data = list(scores.values())       # 替代
# data = []
# for s in scores.values():
#     data.append(s)
```

**为什么需要转列表**（其实 `sum`/`max`/`min` 也能直接吃视图）：

1. **只算一次**，后面用三次不用重复生成
2. **可读性**：名字 `data` 说明这是数据快照
3. **可修改**：万一下次要排序/修改

## 生成器表达式：`sum(1 for s in data if is_pass(s))`

### 白话翻译

```
对 data 里的每一个 s：
    如果 is_pass(s) 是真：
        产出 1
    如果 is_pass(s) 是假：
        什么也不产出
```

**然后 `sum()` 把这些 1 加起来 = 及格人数。**

### 三段式结构

```python
sum(   1      for s in data      if is_pass(s)   )
       ↑      ↑                  ↑
    产出什么   遍历什么           什么条件下才产出
```

### 和 for 循环对照

```python
pass_count = 0
for s in data:
    if is_pass(s):
        pass_count += 1
```

| 传统写法 | 生成器表达式 |
|---|---|
| `pass_count = 0` | 省略（`sum` 从 0 开始） |
| `for s in data:` | `for s in data` |
| `if is_pass(s):` | `if is_pass(s)` |
| **`pass_count += 1`** | **产出 `1`** |
| 循环结束后的值 | **`sum(...)` 的结果** |

> **"符合条件的 +1" → "符合条件就产出 1，然后求和"**

### 四种写法，结果一样

```python
# ① for 循环（最好懂）
count = 0
for s in data:
    if is_pass(s):
        count += 1

# ② 生成器表达式（省内存）
count = sum(1 for s in data if is_pass(s))

# ③ 列表推导式
count = sum([1 for s in data if is_pass(s)])

# ④ 列表推导式 + len
count = len([s for s in data if is_pass(s)])
```

| 写法 | 评价 |
|---|---|
| `for` 循环 | ⭐ **新手期用这个，最好懂** |
| 生成器表达式 | 1 行，省内存，需要基本功 |
| 列表推导式 | 1 行，会先建出完整列表 |

> **建议：既然基础还在打，先用 `for` 循环写。**
> **代码是给人读的，"能看懂"比"短"重要。**

### 产出 ≠ 只能产出 1

```python
sum(s for s in data)                          # 所有分数之和
sum(s for s in data if s >= 60)               # 所有及格分数之和
sum(s for s in data if not is_pass(s))        # 所有不及格分数之和
sum(1 for s in data if is_pass(s))            # 及格分数个数
```

| 你想 | 产出什么 |
|---|---|
| **数个数** | **产出 `1`** |
| **求和** | **产出 `s`** |

> **产出 `1` = 计数；产出 `s` = 求和。**

---

# 十、今天踩过的坑

| # | 坑 | 现象 | 原因 | 解法 |
|---|---|---|---|---|
| 1 | **算对路径但没用** | 文件跑到上级目录 | `open()` 用的是相对路径字符串 | 把变量传进 `open()` |
| 2 | **用 `cd` 进文件** | `cd : 找不到路径` | `cd` 只能进文件夹 | 用 `dir 文件名` 查看 |
| 3 | **造了函数不用** | `find_by_name` / `is_pass` 是死代码 | 重构时忘了替换 | `import` 了就一定要用 |
| 4 | **规则写两遍** | `is_pass` 定义了，`calc_stats` 还硬编码 `>= 60` | 没做到单一数据源 | 统一用 `is_pass` |
| 5 | **`py -c "import main"` 在错目录** | `ModuleNotFoundError` | 当前目录没有 `main.py` | 先 `cd` 到脚本目录 |
| 6 | **函数定义顺序** | 先用的函数定义在后面 | 虽然能跑但读起来困惑 | 小工具函数放上面 |

---

# 十一、自测题（先自己做，再看答案）

## A. 判断

**1. 下面这段代码，文件会落在哪里？**
```python
# 脚本位置：D:\aistudy\day05\a.py
with open("out.txt", "w") as f:
    f.write("x")
```
- 在 `D:\aistudy\day05` 运行 `py a.py`
- 在 `D:\aistudy` 运行 `py day05/a.py`

**2. 怎么改才能让它永远落在 `day05`？**

**3. `Path(__file__).parent` 得到的是什么？**

**4. `BASE_DIR / "scores.json"` 里的 `/` 是除法吗？**

**5. `scores.values()` 能索引吗？**

**6. `scores["张三"]` 和 `scores.get("张三")` 有什么区别？**

**7. `sum(1 for s in data if s >= 60)` 在做什么？**

**8. `if __name__ == "__main__":` 里的代码，什么时候执行？**

**9. `main.py` 里 `import storage` 时，`storage.py` 里的代码会执行吗？哪部分会、哪部分不会？**

**10. 下面这段代码的问题在哪？**
```python
# logic.py
def calc_stats(scores):
    if not scores:
        return None
    pass_count = sum(1 for s in scores.values() if is_pass(s))
    ...

def is_pass(score):
    return score >= 60
```

---

## 参考答案

**1.**
- 在 `day05` 运行 → `D:\aistudy\day05\out.txt`
- 在 `aistudy` 运行 → **`D:\aistudy\out.txt`**
> 相对路径参照当前工作目录。

**2.** 用 `__file__`：
```python
from pathlib import Path
BASE_DIR = Path(__file__).parent
with open(BASE_DIR / "out.txt", "w") as f:
    f.write("x")
```

**3.** **脚本所在的目录**（`D:\aistudy\day05`）

**4.** **不是除法**，是 `pathlib` 的**路径拼接运算符**。

**5.** **不能**。`scores.values()` 返回 `dict_values` 视图，不支持 `[0]`，会报 `TypeError`。要先用 `list()` 转换。

**6.**
- `scores["张三"]` → 键不存在时**报 `KeyError`**
- `scores.get("张三")` → 键不存在时**返回 `None`**（安全查询）

**7.** **数出 `data` 里有多少个 `>= 60` 的元素**（即及格人数）。
> 对每个满足条件的元素产出 1，然后全部加起来。

**8.** **只在"直接运行这个文件"时执行**（`__name__ == "__main__"`）；被 `import` 时不执行。

**9.** **会执行整个模块**（包括函数定义、变量赋值、模块级代码），**但 `if __name__ == "__main__":` 里面的代码不会执行**（因为此时 `__name__` 是 `"storage"`，不是 `"__main__"`）。

**10.** 两个问题：
- **`is_pass` 定义在 `calc_stats` 之后** —— 虽然能运行（调用时才查找），但可读性差，建议挪到上面
- **`calc_stats` 里用了 `is_pass`，但 `is_pass` 的及格线是 60** —— 这是对的；不过如果 `calc_stats` 里另有硬编码的 `>= 60`，就违反了"单一数据源"

---

# 十二、Day 6 预告：进入 AI 领域

**这是里程碑式的一天。** 前 5 天学的都是"Python 基础"，Day 6 开始**接触真正的 AI**。

## 主题：调用大模型 API

**你的系统会迎来一个质的跳跃**：

| 现在 | Day 6 之后 |
|---|---|
| 程序只会"算分数、存文件" | 程序能**理解语言、生成文字、回答问题** |

## 要学的内容

| 技能 | 说明 |
|---|---|
| **HTTP 请求** | `requests` 库，程序怎么和服务器对话 |
| **API 是什么** | 接口、URL、请求方法、响应格式 |
| **API Key 与 `.env`** | ⚠️ **安全底线**，密钥绝不能提交到 Git |
| **调用大模型** | `openai` SDK / 直接发 HTTP 请求 |
| **Token 与成本** | 一次调用花多少钱，怎么省 |
| **错误处理** | 超时、限流、余额不足怎么处理 |

## 你之前埋的伏笔会派上用场

| 之前学的 | Day 6 怎么用 |
|---|---|
| `.gitignore` 里的 `.env` | **保护 API Key**，防止盗刷 |
| `try/except` | 处理网络错误、API 报错 |
| `json` 模块 | 解析 API 返回的 JSON |
| 模块化 + 路径 | `config.py` 读配置、`client.py` 封装 API 调用 |
| 函数设计 | `ask_ai(question)` 这样的封装 |

## 提前准备（明天前做好）

1. **注册一个国内大模型平台的账号**（任选其一）：
   - **DeepSeek**（deepseek.com）—— 便宜，中文好
   - **通义千问**（阿里云百炼）
   - **智谱 GLM**（bigmodel.cn）
2. **完成实名认证**（国内平台都要求）
3. **看懂怎么拿 API Key**（通常在"控制台 → API Keys"）

**不需要充值**，一般都有免费额度或几块钱够你练很久。

## 明天第一件事

**创建 `.env` 文件存 API Key** —— 到时候你会亲眼看到 `.gitignore` 里那一行 `.env` 是怎么保护你的钱的。

---

# 十三、今日成果

## 文件（`D:\aistudy\day05\`）

| 文件 | 内容 |
|---|---|
| `path_demo.py` | 路径陷阱演示（我写的，教学用） |
| `path_test.py` | ✅ 路径练习（`__file__` + `pathlib`） |
| **`storage.py`** | ⭐ 数据层（`load_scores` / `save_scores`） |
| **`logic.py`** | ⭐ 逻辑层（`calc_stats` / `is_pass` / `find_by_name`） |
| **`main.py`** | ⭐ 界面层（菜单 + 交互） |
| `demo_syntax.py` | 生成器表达式演示（我写的，教学用） |

## 核心能力

| 能力 | 说明 |
|---|---|
| **路径绝对化** | `__file__` + `pathlib`，文件永远落在脚本附近 |
| **模块化拆分** | 数据层 / 逻辑层 / 界面层分离 |
| **`import` 机制** | 三种导入方式、模块搜索路径 |
| **`if __name__ == "__main__"`** | 让模块既可运行又可导入 |
| **分层设计** | 单向依赖，上层调用下层 |
| **单一数据源** | 规则只写一处（`is_pass`） |
| `dict.get()` | 安全查询，不存在的键返回 `None` |
| `if not scores:` | Pythonic 的空值判断 |
| 生成器表达式 | `sum(1 for ... if ...)` 计数 |

## 里程碑

> **你的项目从"一个文件"变成了"一个真正的项目结构"。**
>
> 这是从"写脚本"到"做工程"的分界线 —— **而且这是 RAG 项目必备的基础**（那会是十几个文件的项目）。

## 验证记录

| 测试 | 结果 |
|---|---|
| 从 `day05` 运行 `path_test.py` | ✅ 文件落在 `day05` |
| **从 `aistudy` 运行 `py day05/path_test.py`** | ✅ **文件依然落在 `day05`** |
| `py day05/main.py` 录入数据 | ✅ 数据存到 `day05/scores.json` |
| `py -c "import main"` | ✅ 只打印"导入成功"，没进菜单 |
| 删除后重启 | ✅ 数据正确持久化 |

## Git 历史（截至目前）

```
Day1-2: Python 基础练习 + 学生成绩管理系统
Day3: 函数基础 + grade_manager 重构为函数版
Day4: 文件读写 + JSON持久化 + 删除功能
Day5: （待提交）路径处理 + 模块化拆分
```

**记得提交 Day 5**：

```powershell
cd D:\aistudy
git add .
git commit -m "Day5: 路径处理（__file__ + pathlib）+ 模块化拆分"
git push
```
