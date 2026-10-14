# Day 2 知识总结：循环、列表、字典

> 学习日期：2026-10-13
> 产出：11 个 Python 文件 + 学生成绩管理系统 + GitHub 仓库
> 配套：`语法速查卡.md`（Day 1 版）

---

# 目录

1. [`while` 循环](#一while-循环)
2. [`for` 循环](#二for-循环)
3. [列表 list](#三列表-list)
4. [字典 dict](#四字典-dict)
5. [累加器模式（重要套路）](#五累加器模式重要套路)
6. [`if` vs `elif`（今天最大的坑）](#六if-vs-elif今天最大的坑)
7. [`try/except` 错误处理](#七tryexcept-错误处理)
8. [空数据的处理](#八空数据的处理)
9. [变量命名规范](#九变量命名规范)
10. [Git 推送到 GitHub](#十git-推送到-github)
11. [今天踩过的坑（复习重点）](#十一今天踩过的坑复习重点)
12. [自测题](#十二自测题先自己做再看答案)

---

# 一、`while` 循环

## 用途

**不知道要循环几次**的时候用它。想的是"**直到……为止**"。

## 四个零件（缺一不可）

```python
count = 5                    # ① 初始化变量
while count > 0:             # ② 条件：为真就继续，为假就退出
    print(count)             # ③ 循环体
    count -= 1               # ④ 更新变量 ← 少这步会死循环！
```

| 零件 | 漏了会怎样 |
|---|---|
| ① 初始化 | `NameError` |
| ② 条件 | 语法错误 |
| ③ 循环体 | 循环没意义 |
| ④ **更新变量** | **死循环** |

**遇到死循环**：按 **`Ctrl + C`** 强制中断。

## 执行顺序（逐步推演）

```
count = 5
  ↓
检查 5 > 0 ? 真 → 打印 5 → count = 4
检查 4 > 0 ? 真 → 打印 4 → count = 3
检查 3 > 0 ? 真 → 打印 3 → count = 2
检查 2 > 0 ? 真 → 打印 2 → count = 1
检查 1 > 0 ? 真 → 打印 1 → count = 0
检查 0 > 0 ? 假 → 退出循环
```

## 典型用法：输入校验（工作中天天用）

```python
score = int(input("输入分数："))

while score < 0 or score > 100:
    print("分数必须在 0 到 100 之间，请重新输入")
    score = int(input("输入分数："))

# 走到这里说明分数合法了
if score >= 90:
    print("优秀")
```

**设计要点**：**先输入一次，再检查**。这样结构最清晰。

## `while True` + `break`（菜单程序的标准写法）

```python
while True:                    # 永远循环
    choice = input("请选择：")
    if choice == "5":
        break                  # 靠 break 退出
```

## 简写运算符

```python
count -= 1        # 等价于 count = count - 1
count += 1        # 等价于 count = count + 1
total += score    # 累加
count *= 2        # 乘
```

---

# 二、`for` 循环

## 用途

**遍历一个集合**（列表、字典）。想的是"**对每一个……都做**"。

## 基本语法

```python
scores = [85, 92, 78]

for s in scores:
    print(s)
```

**读法**：对于 `scores` 里的**每一个**元素，把它叫做 `s`，执行下面的代码。

## `while` vs `for` 怎么选

| | `while` | `for` |
|---|---|---|
| 用在 | **不知道**循环几次 | **知道**要遍历什么 |
| 例子 | 密码验证（可能输 1 次也可能 10 次） | 遍历成绩列表 |
| 口诀 | "**直到**……为止" | "**对每一个**……" |

## 配合 `range()`

```python
for i in range(5):        # 0 1 2 3 4（从 0 开始，不含 5）
for i in range(1, 6):     # 1 2 3 4 5
```

## 遍历字典的三种方式

```python
scores = {"张三": 85, "李四": 92}

for k in scores:                  # 只拿「键」
    print(k)                      # 张三、李四

for v in scores.values():         # 只拿「值」
    print(v)                      # 85、92

for k, v in scores.items():       # 同时拿「键和值」⭐ 最常用
    print(f"{k}：{v}")
```

---

# 三、列表 list

## 是什么

**一个变量里装一串值。**

```python
scores = [85, 92, 78, 90, 66]
#          ↑   ↑   ↑   ↑   ↑
# 索引:     0   1   2   3   4      ← 从 0 开始！
```

## 基本操作

```python
scores = [85, 92, 78]

scores[0]            # → 85      第一个
scores[2]            # → 78      第三个
scores[-1]           # → 78      最后一个（-1 表示从后往前）
len(scores)          # → 3       一共几个

scores.append(100)   # 末尾添加  → [85, 92, 78, 100]
scores.remove(92)    # 删除指定值 → [85, 78, 100]
scores.pop()         # 删除末尾并返回它
```

## ⚠️ 常见错误

```python
scores[5]            # ❌ IndexError: list index out of range
```
**5 个元素 → 索引是 0~4。** 用 `len()` 得到的数字**不能直接当索引用**。

## 括号的记忆

| 符号 | 用途 |
|---|---|
| `[ ]` 方括号 | 列表 / 取索引 |
| `{ }` 花括号 | 字典 |
| `( )` 圆括号 | 调用函数，如 `print()` |

---

# 四、字典 dict

## 是什么

**存"键 → 值"对应关系。** 适合有对应关系的数据（人名→分数）。

```python
scores = {"张三": 85, "李四": 92}
#           ↑    ↑
#          键    值
```

## 列表 vs 字典

| | 列表 | 字典 |
|---|---|---|
| 写法 | `[85, 92]` | `{"张三": 85}` |
| 怎么取 | 用**位置** `scores[0]` | 用**键** `scores["张三"]` |
| 适合 | 一堆同类数据 | 有对应关系的数据 |
| 记忆 | "第几个" | "谁" |

## 基本操作

```python
scores = {"张三": 85, "李四": 92}

scores["张三"]              # → 85        取值
scores["王五"] = 78         # 添加新的键值对
scores["张三"] = 90         # 修改已存在的值
len(scores)                 # → 3         几个键值对
"张三" in scores            # → True      判断键是否存在
```

## ⚠️ 常见错误

```python
scores["赵六"]              # ❌ KeyError: '赵六'
```

**所以取值前要先判断**：
```python
if "赵六" in scores:
    print(scores["赵六"])
else:
    print("查无此人")
```

## 🔴 f-string 里的引号陷阱（今天的重要一课）

```python
scores = {"张三": 85}
name = "张三"

scores[name]        # ✅ name 是变量 → 取出它的值 "张三" → 查到 85
scores["name"]      # ❌ "name" 是字符串 → 找一个叫 "name" 的键 → KeyError
```

**记忆口诀**：

> **变量加了引号，就变成了字面文字。**
> - 不加引号 `name` → "把 name 变量里的东西拿出来"
> - 加了引号 `"name"` → "就是 name 这两个字本身"

**验证脚本**：`day02/demo_quote.py`

---

# 五、累加器模式（重要套路）

## 三个变体

### ① 求和

```python
total = 0                    # 准备累加器，从 0 开始
for s in scores:
    total += s               # 每次加进去
print(total)
```

### ② 计数

```python
count = 0
for s in scores:
    if s >= 60:
        count += 1           # 满足条件才加
print(count)
```

### ③ 找最值

```python
biggest = scores[0]          # ⚠️ 用第一个元素做初始值，不是 0！
for s in scores:
    if s > biggest:
        biggest = s
print(biggest)
```

**为什么不能用 `biggest = 0`**：如果所有分数都是负数，`0` 会比它们都大，结果就错了。
**正确做法**：拿集合里的第一个元素当初始值。

## 简化：用内置函数

```python
sum(scores)          # 求和
max(scores)          # 最大值
min(scores)          # 最小值
len(scores)          # 长度
```

**实践中的选择**：

| 思路 | 优点 | 缺点 |
|---|---|---|
| 手写循环 | **理解原理** | 长、容易错 |
| 内置函数 | 短、快、不易错 | 需要先理解原理 |

**正确顺序**：先手写理解原理 → 再用内置函数提高效率。

---

# 六、`if` vs `elif`（今天最大的坑）

## 核心区别

| 写法 | 行为 | 用在哪 |
|---|---|---|
| `if` + `if` + `if` | 每个条件**独立判断**，可命中多个 | 多件**互不相关**的事 |
| `if` + `elif` + `elif` | 命中一个就**跳过其余**，最多命中一个 | **同类的互斥**情况 |

## 判断口诀

> **问自己：这几件事"可能同时发生"吗？**
> - **可能同时发生 → 用 `if`**
> - **只能是其中一种 → 用 `elif`**

## 今天的实战案例

### 场景 A：成绩等级 → 用 `elif` ✅

```python
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```
**理由**：一个分数**不可能**既优秀又良好 → **互斥** → `elif` 正确

### 场景 B：统计（求最值 + 计数）→ 必须用 `if` ✅

```python
for s in scores:
    if big < s:              # 任务1：更新最高分
        big = s

    if small > s:            # 任务2：更新最低分
        small = s

    if s >= 60:              # 任务3：统计及格
        num2 += 1
```
**理由**：一个 92 分的同学**既是**新的最高分，**又及格** → **同时成立** → 必须用 `if`

## 用 `elif` 写场景 B 会怎样（你今天踩的坑）

```python
for s in scores:
    if big < s:
        big = s
    elif small > s:          # ← 前面命中了就跳过
        small = s
    elif s >= 60:            # ← 前面命中了就跳过 → 统计漏掉大部分
        num2 += 1
```

**后果**：`[85, 92, 78, 90, 66, 100, 45]` 的及格人数算出来是 **2**，正确答案是 **6**。
**因为大部分轮次都被前两个条件"抢先命中"，`num2 += 1` 根本没机会执行。**

---

# 七、`try/except` 错误处理

## 用途

**让程序在遇到错误时不崩溃**，而是给出提示继续运行。

## 语法

```python
while True:
    try:
        score = int(input("请输入分数："))
        if 0 <= score <= 100:
            break                        # 合法，跳出
        else:
            print("分数必须在 0 到 100 之间")
    except ValueError:
        print("请输入数字，不要输入字母")
```

| 关键字 | 作用 |
|---|---|
| `try:` | "试着执行下面的代码" |
| `except ValueError:` | "如果出现了 ValueError 这种错误，就执行这里" |

## 为什么必须要有它

**没有 `try/except`**：用户在分数那里输入 `abc` → 程序直接崩溃退出。

```
ValueError: invalid literal for int() with base 10: 'abc'
```

**这是真实程序不能接受的**——用户乱输一下程序就死了。

## 常见异常类型

| 异常名 | 什么情况 |
|---|---|
| `ValueError` | 值不对，如 `int("abc")` |
| `TypeError` | 类型不对，如字符串和数字相加 |
| `KeyError` | 字典里没有这个键 |
| `IndexError` | 列表索引越界 |
| `ZeroDivisionError` | 除以零 |
| `NameError` | 变量没定义就用 |

---

# 八、空数据的处理

## 问题

**功能 2 你检查了空数据，功能 3 忘了** → 选 3 时程序崩溃：

```
总人数：0
总分：0
ZeroDivisionError: division by zero     ← 平均分 0/0
```

**即使不崩在除法，也会崩在这里**：
```python
max([])      # ❌ ValueError: max() arg is an empty sequence
```

## 规律

> **任何一个"对数据做操作"的功能，都要先问：数据可能是空的吗？**

## 标准写法

```python
elif choice == "3":
    if len(scores) == 0:
        print("暂无数据")
    else:
        # 你的统计代码（整体缩进一层）
```

**两种判断方式都可以**：
```python
if len(scores) == 0:      # 方式一
if not scores:            # 方式二：空字典/空列表在 Python 里算"假"
```

---

# 九、变量命名规范

## 三条规则

### ① 全小写，下划线分隔

```python
student_name = "张三"      # ✅
studentName = "张三"       # ❌ 这是 Java/C# 风格
StudentName = "张三"       # ❌ 这是类名风格
```

### ② 别用内置名字（会覆盖掉它们）

```python
dict = {...}          # ❌ 覆盖了内置的 dict 类型
list = [...]          # ❌ 覆盖了内置的 list
str = "abc"           # ❌
int = 5               # ❌
sum = 0               # ❌
max = 100             # ❌
```

**症状**：你今天就踩了一次——`'list' object is not callable`
**原因**：变量名撞上了内置名字

```python
dict = {"张三": 80}
d = dict()            # ❌ TypeError: 'dict' object is not callable
```

### ③ 名字要有信息量

| ❌ 模糊 | ✅ 清楚 |
|---|---|
| `a`、`b`、`n`、`s` | `name`、`score`、`student`、`total` |
| `alist` | `score_list` |
| `num`、`num2` | `total`、`pass_count` |
| `name2` | `query_name` |

**判据**：**三个月后你回来看这份代码，能不能一眼看懂这个变量装的是什么？**

## 命名建议表

| 变量用途 | 推荐名字 |
|---|---|
| 学生姓名 | `name`、`student_name` |
| 分数 | `score` |
| 一堆分数 | `scores`、`score_list` |
| 总分 | `total` |
| 平均分 | `average` |
| 最高分 | `highest`、`max_score` |
| 最低分 | `lowest`、`min_score` |
| 及格人数 | `pass_count` |
| 计数器 | `count` |
| 用户的选择 | `choice` |

---

# 十、Git 推送到 GitHub

## 完整流程

### 首次（只做一次）

```powershell
cd D:\aistudy
git init                                          # 建仓库
git add .                                         # 加入暂存区
git commit -m "说明"                               # 提交

# 在 GitHub 网页创建仓库后：
git remote add origin https://github.com/用户名/仓库名.git
git branch -M main
git push -u origin main
```

**`-u` 的作用**：记住"本地 main ↔ 远程 origin/main"的对应关系，**以后只敲 `git push` 两个字就行**。

### 日常（每天）

```powershell
git status                    # 看有什么改动
git add .
git commit -m "DayN: 做了什么"
git push                      # 因为用过 -u，不用写 origin main
```

## `.gitignore`（安全底线）

**作用**：列在这里的文件，Git **永远不看、不上传**。

**必须写进去的**：

| 内容 | 为什么 |
|---|---|
| **`.env`** | ⚠️ 存 API Key，泄露会被盗刷 |
| `.venv/` | 虚拟环境，几百 MB 的垃圾 |
| `__pycache__/` | Python 自动生成的缓存 |
| `*.log` | 日志 |

**⚠️ 最重要的使用方法**：**项目一开始就建 `.gitignore`，再写代码。** 提交过再补，历史里还留着。

**写法**：
```
.venv/            # 任意位置的 .venv 目录
*.pyc             # 所有 .pyc 结尾的文件
.env              # 这个文件
# 注释
```

## 有用的 Git 命令

| 命令 | 作用 |
|---|---|
| `git branch` | 列出所有分支，`*` 表示当前所在 |
| `git remote -v` | 看远程仓库地址 |
| `git status --ignored` | 额外显示被忽略的文件 |
| `git commit --amend -m "新说明"` | **修改上一次提交**（合并新改动进去） |
| `git add -A` | 加入所有变化，**包括"删除文件"** |

**⚠️ `--amend` 的注意事项**：它**改写历史**。**没推送过 → 安全；已推送过 → 会导致远程和本地不一致，别用。**

## 排错三板斧

遇到推送问题，**按顺序查这三个**：

```powershell
git status              # 1. 有没有未提交的东西？
git branch              # 2. 分支名对不对？
git remote -v           # 3. 远程地址对不对？
```

**今天的案例**：分支被误命名为 `mian`（不是 `main`），导致：
```
error: src refspec main does not match any
```
**翻译**：你要推的 `main` 分支，我在本地找不到。
**第一反应**：`git branch` 看看分支到底叫什么。

---

# 十一、今天踩过的坑（复习重点）

| # | 坑 | 现象 | 原因 | 解法 |
|---|---|---|---|---|
| 1 | **列表用圆括号** | `TypeError: 'list' object is not callable` | `score(0)` 应该是 `score[0]` | 取索引用**方括号** |
| 2 | **索引越界** | `IndexError: list index out of range` | 6 个元素访问 `[8]` | 索引范围是 0~len-1 |
| 3 | **`elif` 用错** | 及格人数算成 2（应 6） | 前面条件命中就跳过后面 | 独立任务用 `if` |
| 4 | **`> 60` 应为 `>= 60`** | 60 分被判不及格 | 边界漏了等号 | 用 `>=`，并测边界值 |
| 5 | **变量名撞内置** | `'dict' object is not callable` | 变量名叫 `dict` | 改名 `scores` |
| 6 | **f-string 引号陷阱** | `KeyError: 'name'` | `scores["name"]` 找的是"name"这个键 | 用变量就不加引号 `scores[name]` |
| 7 | **空数据崩溃** | `ZeroDivisionError` / `max()` 报错 | 没检查空字典 | 先 `if len(scores) == 0` |
| 8 | **非数字输入崩溃** | `ValueError: invalid literal for int()` | 用户输了 `abc` | `try/except` |
| 9 | **变量名 `mian`** | `src refspec main does not match any` | 拼写错误 | `git branch -M main` |
| 10 | **忘保存就运行** | 输出和代码对不上 | 跑的是旧文件 | `Ctrl + S`（今天又踩一次） |
| 11 | **多余的 `int()`** | `int(len(scores))` | 以为 `len()` 返回的不是整数 | `len()` 本来就返回 int |

---

# 十二、自测题（先自己做，再看答案）

## A. 判断输出

**1. 这段代码输出什么？**
```python
count = 3
while count > 0:
    print(count * 2)
    count -= 1
```

**2. 这段代码输出什么？**
```python
scores = [10, 20, 30]
total = 0
for s in scores:
    total += s
print(total, len(scores))
```

**3. 这段代码输出什么？**
```python
scores = {"A": 60, "B": 70}
for k, v in scores.items():
    if v >= 65:
        print(k)
```

**4. 这段代码会报什么错？**
```python
data = [1, 2, 3]
print(data[3])
```

**5. 这段代码会报什么错？**
```python
info = {"name": "张三"}
print(info["age"])
```

## B. 找出 bug

**6. 这段代码想统计及格人数，但结果不对，问题在哪？**
```python
count = 0
for s in scores:
    if s > 60:
        count += 1
```

**7. 这段代码想找最高分，但结果不对，问题在哪？**
```python
highest = 0
for s in scores:
    if s > highest:
        highest = s
```

**8. 这段代码想更新最高分和最低分，但最低分总是不对，问题在哪？**
```python
high = scores[0]
low = scores[0]
for s in scores:
    if s > high:
        high = s
    elif s < low:
        low = s
```

**9. 这个字典查找为什么报 KeyError？**
```python
scores = {"张三": 85}
name = "张三"
print(scores["name"])
```

**10. 这段代码想求平均分，但空列表时会崩溃，怎么修？**
```python
total = sum(scores)
average = total / len(scores)
```

---

## 参考答案

**1.** 输出 `6`、`4`、`2`
> 循环 3 次：`3*2=6`、`2*2=4`、`1*2=2`

**2.** 输出 `60 3`
> `total` 累加得 60，`len` 是 3

**3.** 输出 `B`
> 只有 70 满足 `>= 65`；60 不满足

**4.** `IndexError: list index out of range`
> 索引范围是 0~2，`data[3]` 越界

**5.** `KeyError: 'age'`
> 字典里只有 `"name"` 这个键

**6.** `> 60` 应该是 **`>= 60`**
> 60 分应该算及格。**在你原来的测试数据上看不出来，测一个 60 就暴露了。**

**7.** `highest = 0` 应该是 **`highest = scores[0]`**
> 如果所有分数都是负数，`0` 比它们都大，结果就错了。**正确做法：用第一个元素当初始值。**

**8.** `elif` 应该是 **`if`**
> `if s > high` 命中后，`elif s < low` 就被跳过了。
> 但"更新最高分"和"更新最低分"是**两件独立的事**，必须用两个 `if`。

**9.** `scores["name"]` 里 `"name"` 是**字符串**，程序会去找一个叫 `"name"` 的键，但字典里只有 `"张三"`。
> 应该写 `scores[name]`（不加引号，用变量的值）。

**10.** 加空数据判断：
```python
if len(scores) == 0:
    print("暂无数据")
else:
    total = sum(scores)
    average = total / len(scores)
```
> 两个问题：`len(scores)` 为 0 时除零报错；`sum([])` 返回 0 不报错但 `0/0` 会崩。

---

# 十三、今天的产出清单

## 代码文件（`D:\aistudy\day02\`）

| 文件 | 练了什么 |
|---|---|
| `countdown.py` | `while` 基本结构 |
| `password.py` | `while` + 输入校验 |
| `score2.py` | `while` + 范围校验 |
| `list_demo.py` | 列表操作、`IndexError` |
| `dict_demo.py` | 字典操作、`KeyError` |
| `demo_quote.py` | f-string 引号陷阱演示 |
| `lookup.py` | 字典查询 + `in` 判断 |
| `stats.py` | `for` + 累加器模式 |
| **`grade_manager.py`** | ⭐ **综合项目：学生成绩管理系统** |

## GitHub

**仓库地址**：https://github.com/zim3526/python-learning

**提交记录**：`f7a5cd3 Day1-2: Python 基础练习 + 学生成绩管理系统`

---

# 十四、下一步（Day 3）

| 主题 | 解决什么问题 |
|---|---|
| **函数 `def`** | `grade_manager.py` 里有重复代码，函数可以把它们打包复用。**这是让代码"专业"的关键一步** |
| **错误处理进阶** | 你的程序还有很多地方一输错就崩 |

**Day 3 结束后，你的程序会从"能跑"变成"像样"。**
