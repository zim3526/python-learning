# Day 3 知识总结：函数与代码复用

> 学习日期：2026-10-14
> 产出：`func_basic.py`、`stats_func.py`、`input_func.py`、`grade_manager2.py`（函数版重构）
> 核心主题：**把重复的代码打包成函数**

---

# 目录

1. [为什么需要函数](#一为什么需要函数)
2. [函数的基本语法](#二函数的基本语法)
3. [`print` vs `return`（最重要）](#三print-vs-return最重要)
4. [参数与返回值详解](#四参数与返回值详解)
5. [变量的作用域](#五变量的作用域)
6. [引用传递：列表和字典的特殊性](#六引用传递列表和字典的特殊性)
7. [`try/except` 的位置（今天的调试重点）](#七tryexcept-的位置今天的调试重点)
8. [文档字符串 docstring](#八文档字符串-docstring)
9. [`if __name__ == "__main__":`](#九if-__name__-__main__)
10. [函数设计原则](#十函数设计原则)
11. [重构实战：grade_manager 前后对比](#十一重构实战grade_manager-前后对比)
12. [今天踩过的坑](#十二今天踩过的坑)
13. [自测题](#十三自测题先自己做再看答案)

---

# 一、为什么需要函数

## 问题：重复代码

假设"存钱、取钱、查余额"都要校验金额：

```python
if choice == "1":
    while True:                          # ← 校验代码
        try:
            amount = float(input("存入金额："))
            if amount > 0:
                break
            print("金额必须大于0")
        except ValueError:
            print("请输入数字")
    balance += amount

elif choice == "2":
    while True:                          # ← 一模一样
        try:
            amount = float(input("取出金额："))
            ...
```

## 重复代码的四个代价

| 代价 | 说明 |
|---|---|
| **改一处要改多处** | 规则变了，得改所有副本 |
| **容易漏改** | 改了 2 处忘了第 3 处 → bug |
| **代码变长** | 真正有意义的逻辑被淹没 |
| **没法单独测试** | 想测"金额校验"这段逻辑，做不到 |

## 函数是什么

**一句话**：**把一段代码打包起来，起个名字，需要时按名字调用。**

**生活类比**：函数就像"微波炉按钮"
- 按钮内部有几十个零件、复杂电路（= 函数体）
- 你只需要按一下（= 调用）
- 你不需要知道它内部怎么工作（= 抽象）
- 可以按很多次（= 复用）

---

# 二、函数的基本语法

## 定义

```python
def greet():
    print("你好！")
    print("欢迎使用本程序")
```

| 部分 | 含义 |
|---|---|
| `def` | **define**（定义），告诉 Python "我要定义函数" |
| `greet` | 函数名（规则同变量名） |
| `()` | 参数列表，空的表示不需要传入任何东西 |
| `:` | 冒号，和 `if`、`while` 一样不能少 |
| 缩进的代码 | **函数体**：调用时执行的内容 |

## 🔴 关键认知：定义了不会自动执行

```python
def greet():
    print("你好！")

# 到这里程序什么都不会输出！
```

**必须调用**：

```python
greet()        # ← 调用，这时才执行
greet()        # ← 可以调用多次
```

**⚠️ 调用时括号不能省**：

| 写法 | 含义 |
|---|---|
| `greet()` | ✅ **调用**函数，执行它 |
| `greet` | ❌ 只是提到函数本身，**不执行** |

**这个错误的症状**：`'function' object is not callable`（忘了括号）或反过来 `'list' object is not callable`（给不是函数的东西加了括号）。

---

# 三、`print` vs `return`（最重要）

## 对比实验

```python
def print_sum(a, b):
    print(a + b)         # 只"显示"

def return_sum(a, b):
    return a + b         # 把结果"交给调用者"

r1 = print_sum(3, 4)     # 屏幕显示 3
print(r1)                # → None     ⚠️

r2 = return_sum(3, 4)    # 屏幕什么都不显示
print(r2)                # → 3        ✅
```

## 区别表

| | `print` | `return` |
|---|---|---|
| 作用 | 把东西**显示在屏幕上** | 把结果**交给调用它的代码** |
| 结果能被后续使用吗 | ❌ 不能 | ✅ 能 |
| 类比 | 大声念出来 | 把东西递给你 |
| 什么时候用 | **只是给人看** | **结果还要参与计算** |

## 判断标准

> **问自己："这个结果后面还要用吗？"**
> - **要 → `return`**
> - **只是给人看 → `print`**

**没有 `return` 的函数返回 `None`**（Python 里的"空"）。

## 实践分工

```python
def calc_bmi(height, weight):
    return weight / (height ** 2)      # ✅ 算，用 return

def show_bmi(bmi):
    if bmi < 18.5:
        print(f"你的 BMI 是 {bmi:.2f}，偏瘦")     # ✅ 显示，用 print
```

**原则**：**函数负责"算"，外面负责"显示"。** 这样函数可以被别处复用。

---

# 四、参数与返回值详解

## 参数：把数据传进去

```python
def greet(name):
    print(f"你好，{name}！")

greet("张三")        # → 你好，张三！
```

**数据流**：
```
greet("张三")
      ↓
name = "张三"        ← 参数把值传进函数内部
```

**术语**：
- `name` = **参数**（函数定义时的占位符）
- `"张三"` = **实参**（实际传进去的值）

**多参数**：
```python
def add(a, b):
    return a + b

add(3, 5)            # 8
```

**⚠️ 参数个数必须对得上**：
```python
add(3)               # ❌ TypeError: missing 1 required positional argument: 'b'
add(3, 5, 7)         # ❌ TypeError: takes 2 positional arguments but 3 were given
```

## 返回值

```python
def add(a, b):
    return a + b

result = add(3, 5)       # 用变量接住
print(result)            # 8
```

## 返回多个值（用字典更清晰）

**方案 A：返回字典** ✅ 推荐
```python
def calc_stats(scores):
    return {
        "count": len(scores),
        "total": sum(scores),
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "pass_count": ...,
    }

# 调用：
stats = calc_stats(scores)
print(f"平均分：{stats['average']:.2f}")     # 有名字，一看就懂
```
**优点**：**有名字，不会搞错顺序**

**方案 B：返回元组**
```python
return count, total, average, highest, lowest, pass_count
# 调用：
count, total, avg, high, low, pc = calc_stats(scores)   # ← 容易搞混顺序
```
**缺点**：**6 个变量必须记住顺序**

**结论**：返回值多的时候**用字典**。

## ⚠️ 字典放进 f-string 的引号陷阱

```python
print(f"总人数：{stats['count']}")      # ✅ 外双内单
print(f'总人数：{stats["count"]}')      # ✅ 外单内双

print(f"总人数：{stats["count"]}")      # ❌ 内外都是双引号 → 冲突
```

**记法**：**f-string 里外引号必须不一样。**

---

# 五、变量的作用域

```python
def test():
    x = 10                   # x 是"局部变量"
    print(x)

test()                       # → 10
print(x)                     # ❌ NameError: name 'x' is not defined
```

**规则**：
- **函数内部定义的变量，函数结束后就消失**
- **外面看不见它**
- **函数的参数也是局部变量**

**类比**：函数像一个房间，里面的东西出了房间就看不见了。

**函数怎么改外面的数据？→ 靠 `return`**（或者改传入的可变对象，见下节）。

---

# 六、引用传递：列表和字典的特殊性

## 一个必须知道的事实

```python
def add_score(scores):
    scores.append(100)         # 直接改传进来的列表

my_scores = [85, 92]
add_score(my_scores)
print(my_scores)               # → [85, 92, 100]   ← 被改了！
```

**对比数字**：

```python
def add_one(n):
    n += 1                     # 只改了函数内部的 n

x = 5
add_one(x)
print(x)                       # → 5   ← 没变
```

## 对比表

| 传入类型 | 函数里改它 | 外面的变量 |
|---|---|---|
| 数字、字符串、布尔 | 改的是副本 | **不受影响** |
| **列表、字典** | 改的是原件 | **会跟着变** |

## 实践含义

**这解释了两件事**：

1. `input_score(scores)` 里 `scores[name] = score` **直接改到了 `main` 里的字典** → **所以不需要 `return scores`**
2. `calc_stats(scores)` 只是**读** `scores`，没有改它 → 所以它**用 `return` 把结果交出来**

**判断方法**：
> **函数是"读取数据算出结果" → 用 `return`**
> **函数是"往容器里加东西" → 直接改传入的容器，不用 return**

---

# 七、`try/except` 的位置（今天的调试重点）

## 今天你遇到的问题

```python
def get_number(prompt, low, high):
    num = int(input(f"{prompt}："))      # ← int() 在 try 外面
    while True:
        try:
            if low <= num <= high:       # ← try 里只有比较
                break
            print(f"请输入{low}到{high}之间的数字")
        except ValueError:
            print("请输入数字")
        num = input(f"{prompt}：")       # ← 忘了 int()！
    return num
```

**两个问题**：

| 问题 | 后果 |
|---|---|
| `int()` 在 `try` 外面 | **`ValueError` 抓不到**，用户输 `abc` 直接崩溃 |
| 第 10 行忘了 `int()` | `num` 变成字符串 → `TypeError: '<=' not supported between 'int' and 'str'` |

## 正确写法

```python
def get_number(prompt, low, high):
    """反复询问，直到用户输入一个在 [low, high] 范围内的整数。"""
    while True:
        try:
            num = int(input(prompt))       # ⭐ 转换在 try 里面
            if low <= num <= high:
                return num                 # ⭐ 合法直接返回
            print(f"请输入 {low} 到 {high} 之间的数字")
        except ValueError:
            print("请输入数字")
```

## 核心原则

> **`try/except` 必须把"可能出错的那行代码"包在里面。**
> **包在外面 = 什么都抓不到。**

**判断方法**：盯着 `try` 块问自己 —— **"我担心的那个错误，是在这里面发生的吗？"**

**你担心"用户输入的不是数字"，而"转换"这个动作（`int()`）必须在 `try` 里。**

## 一个技巧：用 `return` 代替 `break`

```python
# 啰嗦版
while True:
    if 条件:
        break
return num

# 简洁版
while True:
    if 条件:
        return num        # ⭐ 一步到位
```

**能 `return` 就别 `break`** —— 少一层缩进，逻辑更直。

---

# 八、文档字符串 docstring

```python
def get_number(prompt, low, high):
    """反复询问，直到用户输入一个在 [low, high] 范围内的整数。"""
    ...
```

**规则**：函数定义后的**第一行**，用**三个引号**包起来。

**好处**：
- 给读代码的人说明这个函数干什么
- **VS Code 里调用时会自动弹出这段说明**
- 专业代码都有

**写什么**：一句话说清"这个函数做什么、返回什么"。**别写"这是什么语法"**，写"这有什么用"。

---

# 九、`if __name__ == "__main__":`

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

## 这是什么

| 概念 | 说明 |
|---|---|
| `__name__` | Python 内置变量，**表示"当前文件是怎么被使用的"** |
| `py grade_manager2.py` | `__name__` 的值是 `"__main__"` → 条件成立 → **执行 `main()`** |
| 被别的文件 `import` 时 | `__name__` 是文件名 → 条件不成立 → **不执行** |

## 为什么专业代码都这么写

> **让这个文件既能"直接运行"，又能"被别人导入使用而不会自动乱跑"。**

**现在只需要记住这个写法**，理解可以慢慢来。

---

# 十、函数设计原则

## 1. 一个函数只干一件事

```python
# ❌ 不好：又算又打印
def show_stats(scores):
    print(f"总分：{sum(scores)}")
    print(f"平均分：{sum(scores)/len(scores):.2f}")

# ✅ 好：分开
def calc_stats(scores):
    return {"total": ..., "average": ...}      # 只算

def show_stats(scores):
    stats = calc_stats(scores)                 # 只显示
    print(f"总分：{stats['total']}")
```

**为什么**：算的部分能被别处复用（比如以后要写到文件里）。

## 2. 函数名要说明"做什么"

| ❌ | ✅ |
|---|---|
| `f1()`、`func()` | `calc_stats()` |
| `do()` | `input_score()` |
| `data()` | `get_number()` |
| `x()` | `show_all()` |

**命名动词参考**：

| 前缀 | 含义 |
|---|---|
| `get_` | 获取一个值（有返回值） |
| `calc_` | 计算（有返回值） |
| `show_` / `print_` | 显示（没有返回值，用 print） |
| `input_` | 录入（读用户输入） |
| `is_` / `has_` | 判断，返回 True/False |

## 3. 参数数量别太多

**3 个以内最好**。超过 5 个就要考虑换设计了。

```python
def get_number(prompt, low, high):        # ✅ 3 个
```

---

# 十一、重构实战：grade_manager 前后对比

## 重构前（Day 2 版）

```python
while True:
    # 菜单...
    choice = input("请选择（1-5）：")

    if choice == "1":
        # 20 行录入逻辑
    elif choice == "2":
        # 8 行查看逻辑
    elif choice == "3":
        # 15 行统计逻辑（塞在 elif 里）
    elif choice == "4":
        # 6 行查询逻辑
```

## 重构后（Day 3 版）

```python
def get_number(prompt, low, high): ...     # 通用校验
def input_score(scores): ...               # 录入
def show_all(scores): ...                  # 查看
def calc_stats(scores): ...                # 统计（算）
def show_stats(scores): ...                # 统计（显示）
def query_score(scores): ...               # 查询

def main():
    scores = {}
    while True:
        # 菜单...
        if choice == "1":
            input_score(scores)
        elif choice == "2":
            show_all(scores)
        elif choice == "3":
            show_stats(scores)
        elif choice == "4":
            query_score(scores)
        elif choice == "5":
            break
```

## 收益对比

| | 重构前 | 重构后 |
|---|---|---|
| 主循环行数 | ~60 行 | ~30 行 |
| 一眼看清"有哪些功能" | ❌ | ✅ |
| 能单独测试统计逻辑 | ❌ | ✅ `calc_stats(scores)` |
| 想在别处显示成绩 | 复制代码 | 调 `show_all(scores)` |
| 重复的输入校验 | 每次重写 | `get_number()` 复用 |

**核心收益**：
> **读 `main()` 就知道程序干什么，需要细节再进函数看。**

**这是所有大型程序的组织方式。**

---

# 十二、今天踩过的坑

| # | 坑 | 现象 | 原因 | 解法 |
|---|---|---|---|---|
| 1 | **`int()` 在 `try` 外面** | `abc` 输入直接崩溃 | `except` 抓不到 | 把转换放进 `try` |
| 2 | **循环内忘了 `int()`** | `TypeError: '<=' not supported between 'int' and 'str'` | `input()` 返回字符串 | 重新输入时也要转换 |
| 3 | **字典放进 f-string 引号冲突** | 语法错误 | 内外都用双引号 | 外双内单 或 外单内双 |
| 4 | **多余的 `return`** | 返回值没人接 | 函数已经改了传入的字典 | 删掉多余的 `return` |
| 5 | **测试漏了"有数据"的情况** | 统计功能没测到 | 只测了空字典 | **每个功能都要测"空"和"有数据"两种** |
| 6 | **`print` 当作 `return` 用** | 变量接住是 `None` | 混淆了两者 | 看结果后面要不要用 |

---

# 十三、自测题（先自己做，再看答案）

## A. 判断输出

**1.**
```python
def f(a, b):
    print(a + b)

r = f(2, 3)
print(r)
```

**2.**
```python
def f(a, b):
    return a + b

r = f(2, 3)
print(r)
```

**3.**
```python
def test():
    x = 100

test()
print(x)
```

**4.**
```python
def add_item(my_list):
    my_list.append(99)

nums = [1, 2]
add_item(nums)
print(nums)
```

**5.**
```python
def f(n):
    n = n + 1

x = 5
f(x)
print(x)
```

## B. 找 bug

**6. 这个函数想校验输入，但输 `abc` 就崩溃，问题在哪？**
```python
def get_num():
    num = int(input("输入数字："))
    while num < 0:
        print("必须大于0")
        num = int(input("输入数字："))
    return num
```

**7. 这个函数想返回统计结果，但调用方拿不到数据，问题在哪？**
```python
def calc_total(scores):
    print(sum(scores))

result = calc_total([1, 2, 3])
print(result * 2)
```

**8. 这个函数想算平均分，但空列表会崩溃，怎么修？**
```python
def calc_average(scores):
    return sum(scores) / len(scores)
```

**9. 这个函数想打印所有人成绩，但只打印了名字，问题在哪？**
```python
def show_all(scores):
    for name in scores:
        print(name)
```

**10. 这段代码的 `try` 有问题，什么问题？**
```python
def get_number(prompt):
    num = int(input(prompt))
    while True:
        try:
            if num > 0:
                return num
        except ValueError:
            print("请输入数字")
        num = int(input(prompt))
```

---

## 参考答案

**1.** 先显示 `5`，然后显示 `None`
> `f` 没有 `return`，所以 `r` 是 `None`

**2.** 只显示 `5`
> `f` 用 `return` 返回了结果，`print(r)` 打印它

**3.** `NameError: name 'x' is not defined`
> `x` 是函数内部的局部变量，出了函数就消失了

**4.** `[1, 2, 99]`
> **列表是引用传递**，函数里 `append` 直接改到了原来的列表

**5.** `5`
> **数字是值传递**，函数里的 `n = n + 1` 只改了副本，外面的 `x` 不受影响

**6.** 两个问题：
- `int()` 在 `try` 外面（而且根本没有 `try`！），输 `abc` 直接崩溃
- 应该用 `try/except` 包住 `int(input())`

```python
def get_num():
    while True:
        try:
            num = int(input("输入数字："))
            if num > 0:
                return num
            print("必须大于0")
        except ValueError:
            print("请输入数字")
```

**7.** `calc_total` 用了 `print` 而不是 `return`
> `result` 会是 `None`，然后 `None * 2` 报 `TypeError`
> 改成 `return sum(scores)`

**8.** 加空数据判断（或者在调用方判断）
```python
def calc_average(scores):
    if len(scores) == 0:
        return 0              # 或者 None，看需求
    return sum(scores) / len(scores)
```
> 空列表时 `len(scores)` 为 0 → `ZeroDivisionError`

**9.** `for name in scores:` 只拿到**键**（名字），没拿到值
```python
for name, score in scores.items():      # ✅ 用 .items()
    print(f"{name}：{score}分")
```

**10.** `int()` 在 `try` 外面，所以 `except` 抓不到 `ValueError`
> 用户第一次输 `abc` → 第 2 行直接崩溃，根本进不去 `while`
> 修法：把 `int(input(...))` 挪到 `try` 里面

---

# 十四、今日产出

## 文件（`D:\aistudy\day03\`）

| 文件 | 内容 |
|---|---|
| `func_basic.py` | 函数基础 6 个练习 + `print`/`return` 实验 |
| `stats_func.py` | 统计函数（复用昨天逻辑） |
| `input_func.py` | ⭐ **通用输入校验函数**（最实用，以后到处用） |
| `grade_manager2.py` | ⭐ **函数版成绩管理系统**（6 个函数 + `main`） |

## 核心能力

| 能力 | 说明 |
|---|---|
| 定义和调用函数 | `def` / 参数 / `return` |
| **区分 `print` 和 `return`** | 亲手验证了 `None` |
| 返回值设计 | 多结果用字典返回 |
| 作用域 | 局部变量出了函数就消失 |
| **引用传递** | 列表/字典能被函数内部修改 |
| **`try/except` 的正确位置** | 包住"可能出错的那一步" |
| **代码重构** | 把 60 行主循环拆成 6 个函数 |
| docstring | 函数说明文档 |

## 明天（Day 4）预告

**主题**：文件读写 + 让数据能存下来

**要解决的痛点**：你的成绩管理系统，**一退出数据就全没了**。Day 4 学会把数据存到文件里，下次打开还能读回来。

**新内容**：
- `open()` 读写文件
- `with` 语句
- JSON 格式（存字典/列表的标准格式）
- `import` 其他文件里的函数（模块化）

**结果是**：你的成绩管理系统会变成**真正能用的工具**——数据持久化。
