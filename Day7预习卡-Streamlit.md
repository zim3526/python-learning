# 预习卡 3：Streamlit —— 把 Python 脚本变成网页

> **用途：写代码之前先扫一遍。** 今天你会遇到一个全新的编程模型：**脚本会被反复重新执行**。
> 这是 Streamlit 最大的特点，也是最大的坑。

---

# 目录

1. [Streamlit 是什么](#一streamlit-是什么)
2. [★ 核心心智模型：脚本会反复重跑](#二核心心智模型脚本会反复重跑)
3. [★ st.session_state：跨重跑保存数据](#三stsession_state跨重跑保存数据)
4. [常用组件速查](#四常用组件速查)
5. [布局：列、侧边栏、分栏](#五布局列侧边栏分栏)
6. [表单与按钮的正确用法](#六表单与按钮的正确用法)
7. [★ st.write_stream：流式输出](#七stwrite_stream流式输出)
8. [命令行 → Streamlit 对照表](#八命令行--streamlit-对照表)
9. [怎么运行、怎么停](#九怎么运行怎么停)
10. [常见报错对照](#十常见报错对照)
11. [本次项目用到的全部新东西](#十一本次项目用到的全部新东西)

---

# 一、Streamlit 是什么

**一句话**：**一个 Python 库，让你只写 Python 就能得到网页。**

**不用写 HTML、CSS、JavaScript。**

```python
import streamlit as st

st.title("你好，世界")
st.write("这是我的第一个网页")
```

**跑一条命令**：`streamlit run app.py` → **浏览器自动打开** → 看到网页。

## 对比三种界面方式

| 方式 | 要学什么 | 适合 |
|---|---|---|
| **命令行**（你现在的） | 无 | 自己用、调试 |
| **Streamlit** | 一个库 | **数据/AI 工具、原型、作品集** |
| **前端框架**（React 等） | HTML/CSS/JS + 框架 | 正式产品 |

**为什么选 Streamlit**：**投入产出比最高**。几十行代码就能做出能给别人用的界面，而你已有的 `storage.py` / `logic.py` / `ai.py` **一行都不用改**。

---

# 二、★ 核心心智模型：脚本会反复重跑

## 这是今天最重要的一节

**你之前的程序**：

```python
while True:                    # 一直循环，等用户输入
    choice = input(...)        # 阻塞，等
    if choice == "1":
        ...
```

**Streamlit 的程序**：

```python
import streamlit as st

st.title("成绩管理")            # 每次交互都会重新执行这一行
name = st.text_input("姓名")    # 每次交互都会重新创建这个输入框

if st.button("保存"):
    ...                        # 点击时执行

# 脚本到此结束 —— 函数返回后，Streamlit 等下一次交互
```

## 关键规则

> **用户每点一次按钮、每输入一个字、每切换一个选项，Streamlit 都会把整个脚本从头到尾重新执行一遍。**

**推演一遍**：

```
① 用户打开页面
   → 执行脚本：st.title(...) → st.text_input(...) → 结束
   → 页面显示

② 用户在输入框里打字 "张三"
   → 整个脚本重新执行一遍
   → 页面重新渲染

③ 用户点「保存」按钮
   → 整个脚本再执行一遍
   → 这次 st.button() 返回 True → 执行保存逻辑
```

## 这意味着什么（三条后果）

| 后果 | 说明 |
|---|---|
| **不能用 `while True`** | 脚本会立刻跑完，循环会卡死页面 |
| **不能用 `input()`** | 命令行输入在网页里无效，要用 `st.text_input` |
| **普通变量每次都会被重置** | ⚠️ **这就是为什么需要 `session_state`** |

## 反面示例（新手必踩）

```python
import streamlit as st

count = 0                      # ❌ 每次重跑都变回 0

if st.button("加一"):
    count += 1
    st.write(f"当前：{count}")  # 永远显示 1，永远不会变成 2
```

**为什么**：**每次点按钮，脚本都从头跑，`count = 0` 重新执行。**

**正确写法**：

```python
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0         # 只在第一次初始化

if st.button("加一"):
    st.session_state.count += 1

st.write(f"当前：{st.session_state.count}")    # ✅ 会累加
```

---

# 三、★ st.session_state：跨重跑保存数据

## 它是什么

**一个「跨脚本重跑仍然存在」的字典。** 数据存在浏览器会话里。

**类比**：

| | 普通变量 | `st.session_state` |
|---|---|---|
| 生命周期 | **一次脚本执行** | **整个浏览器会话** |
| 每次重跑 | 重置 | **保留** |
| 类比 | 便签纸，用完丢 | 抽屉，一直存着 |

## 三种基本操作

```python
# ① 判断是否存在
if "scores" not in st.session_state:
    st.session_state.scores = {}       # ② 初始化（只执行一次）

# ③ 读写（像字典一样用）
st.session_state.scores["张三"] = 85
print(st.session_state.scores)
```

## 初始化模式（背下来）

```python
if "key" not in st.session_state:
    st.session_state.key = 默认值
```

**为什么必须判断**：**不判断的话，每次重跑都会把数据重置成默认值**，等于没用。

## 两种访问语法

```python
st.session_state["scores"]      # 像字典（键不存在会 KeyError）
st.session_state.scores         # 像属性（推荐，更短）
```

## 什么该放 session_state

| 该放 | 不该放 |
|---|---|
| 成绩字典 | 临时的中间计算结果 |
| 当前选中的学生 | 一次性的局部变量 |
| 对话历史 messages | 常量配置 |

**判据**：**「用户下次交互时，这个值还需要在吗？」需要 → 放 session_state。**

---

# 四、常用组件速查

## 文本显示

| 函数 | 作用 | 例子 |
|---|---|---|
| `st.title("...")` | 大标题 | 页面顶部 |
| `st.header("...")` | 二级标题 | 分区 |
| `st.subheader("...")` | 三级标题 | 小节 |
| `st.write("...")` | **万能显示**（文字、数据、表格、对象都能显示） | 最常用 |
| `st.markdown("**粗体**")` | 支持 Markdown | 想要格式时 |
| `st.code("print(1)")` | 代码块 | 展示代码 |
| `st.caption("...")` | 小字说明 | 注释 |
| `st.divider()` | 分隔线 | 分段 |

## 输入组件

| 函数 | 作用 | 返回 |
|---|---|---|
| `st.text_input("标签")` | 单行文本 | `str` |
| `st.number_input("标签", min_value=0, max_value=100)` | 数字输入 | `int` 或 `float` |
| `st.text_area("标签")` | 多行文本 | `str` |
| `st.selectbox("标签", ["A","B"])` | 下拉选择 | 选中的值 |
| `st.radio("标签", ["A","B"])` | 单选按钮 | 选中的值 |
| `st.slider("标签", 0, 100)` | 滑块 | `int` |
| `st.checkbox("标签")` | 复选框 | `bool` |

**⚠️ 重要**：**这些组件每次重跑都会返回「当前值」**，不需要你保存。

```python
name = st.text_input("姓名：")     # 用户输入什么，name 就是什么（每次重跑重新读）
```

## 按钮

```python
if st.button("保存"):
    ...        # 只有点击的那一次重跑，返回 True
```

**⚠️ 按钮的 `True` 只持续一次执行**。所以「点击后要做的事」必须写在这个 `if` 里面。

## 反馈组件

| 函数 | 作用 |
|---|---|
| `st.success("成功！")` | 绿色提示 |
| `st.error("出错了")` | 红色提示 |
| `st.warning("注意")` | 黄色提示 |
| `st.info("提示")` | 蓝色提示 |
| `st.spinner("加载中...")` | 转圈（配 `with` 用） |

```python
with st.spinner("正在生成..."):
    result = 慢操作()
```

## 数据展示

| 函数 | 作用 |
|---|---|
| `st.dataframe(df)` | 表格（可排序） |
| `st.table(df)` | 静态表格 |
| `st.json(data)` | 显示 JSON |
| `st.metric("平均分", "79.43", "+2.1")` | 指标卡（大数字） |

**`st.metric` 特别适合展示统计结果**：

```python
col1, col2, col3 = st.columns(3)
col1.metric("总人数", 7)
col2.metric("平均分", "79.43")
col3.metric("及格人数", 6)
```

---

# 五、布局：列、侧边栏、分栏

## 列（横向并排）

```python
col1, col2 = st.columns(2)          # 2 列，等宽
with col1:
    st.write("左边")
with col2:
    st.write("右边")

# 不等宽
col1, col2 = st.columns([2, 1])     # 2:1
```

## 侧边栏

```python
with st.sidebar:
    st.header("设置")
    model = st.selectbox("模型", ["deepseek-flash"])
```

**适合放**：配置项、导航、说明文字。

## 分栏（带边框的区块）

```python
with st.container(border=True):
    st.write("这个区块有边框")
```

## 展开面板

```python
with st.expander("点开看详情"):
    st.write("隐藏的内容")
```

---

# 六、表单与按钮的正确用法

## 问题：每个组件都会触发重跑

```python
name = st.text_input("姓名")        # 输入一个字 → 重跑
score = st.number_input("分数")     # 改数字 → 又重跑
if st.button("保存"):               # 再重跑
    ...
```

**输入时页面不断刷新，体验差。**

## 解法：`st.form`（提交时才触发）

```python
with st.form("录入表单"):
    name = st.text_input("姓名")
    score = st.number_input("分数", 0, 100)
    submitted = st.form_submit_button("保存")     # ⚠️ 是 form_submit_button，不是 button

if submitted:
    # 这里能拿到 name 和 score
    ...
```

**特点**：**表单里的组件值在「提交」前不会触发重跑**，用户填完一次性提交。

## 两种写法的选择

| 场景 | 用什么 |
|---|---|
| 单个输入 + 立即生效 | `st.button` |
| 多个输入一起提交 | `st.form` |
| 下拉筛选（即时生效） | `st.selectbox`（不加 form） |

---

# 七、★ st.write_stream：流式输出

## 这是 Streamlit 最适合 AI 的地方

**你 Day 6 写的流式代码**：

```python
for chunk in response:
    if chunk.choices:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            full_answer += delta
```

**Streamlit 一行搞定**：

```python
def stream_answer(messages):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        stream=True,
    )
    for chunk in response:
        if chunk.choices:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta                    # ⚠️ 用 yield 而不是 print

answer = st.write_stream(stream_answer(messages))
```

## 关键区别：`yield` 而不是 `print`

| 关键字 | 作用 |
|---|---|
| `print(delta)` | 直接打印到终端 |
| **`yield delta`** | **把这一块交出去，让调用方处理** |

**`yield` 是什么**：**让函数变成「生成器」—— 可以一个一个吐出值**。

**类比**：

| | 普通函数 | 生成器（用 yield） |
|---|---|---|
| 返回 | 全部算完，一次性 `return` | **算一块，吐一块** |
| 适合 | 有确定结果 | **流式、大数据、边算边用** |

**`st.write_stream` 的返回值**：**拼好的完整字符串** —— 你可以直接存进历史。

```python
full_answer = st.write_stream(stream_answer(messages))
messages.append({"role": "assistant", "content": full_answer})
```

---

# 八、命令行 → Streamlit 对照表

| 命令行写法 | Streamlit 写法 |
|---|---|
| `print("...")` | `st.write("...")` |
| `input("姓名：")` | `st.text_input("姓名")` |
| `int(input("分数："))` | `st.number_input("分数", 0, 100)` |
| `while True:` + 菜单 | **删掉**，改成页面上的控件 |
| `if choice == "1":` | `if st.button("录入"):` |
| 全局字典 `scores = {}` | `st.session_state.scores` |
| `os.system("cls")` | （不需要） |
| `break` | （不需要） |
| `print()` 流式 | `st.write_stream(...)` + `yield` |

## 结构对照

**命令行**：

```python
def main():
    scores = {}
    while True:
        # 打印菜单
        # 读 choice
        # 分发到各函数
```

**Streamlit**：

```python
# 没有 main、没有 while
if "scores" not in st.session_state:
    st.session_state.scores = load_scores()

# 页面顶部：标题 + 统计指标
st.title("成绩管理")
# 主体：选项卡 或 展开面板
# 每个功能一个区块
```

---

# 九、怎么运行、怎么停

## 运行

```powershell
cd D:\aistudy\day07
streamlit run app.py
```

**会发生什么**：
1. 终端显示 `You can now view your Streamlit app in your browser.`
2. **浏览器自动打开** `http://localhost:8501`
3. 终端会一直占用（这是服务器在跑）

## 停

**在终端按 `Ctrl + C`**。

## ⚠️ 改代码后

- **Streamlit 会自动检测文件变化并重新加载**（页面右上角会提示 "Rerun"）
- **如果没自动刷新，点页面右上角的 `Rerun` 按钮，或按 `R`**

## ⚠️ 端口被占用

```
Port 8501 is already in use
```

**说明上一次没关**。两种解法：
- 关掉旧终端
- 换端口：`streamlit run app.py --server.port 8502`

---

# 十、常见报错对照

| 报错 / 现象 | 原因 | 解法 |
|---|---|---|
| `StreamlitAPIException` | 组件用法错误 | 看报错里的具体组件名 |
| `st.button()` 一直返回 False | 点在别处，或已经执行过 | 确认点击位置；`True` 只持续一次 |
| 数据一刷新就没了 | 用了普通变量 | 改成 `st.session_state` |
| 页面一直转圈 | 有死循环或慢操作没加 spinner | 删掉 `while True`；慢操作加 spinner |
| `TypeError: write_stream() ...` | 传的不是生成器 | 函数里用 `yield`，不用 `return` |
| 中文乱码 | 文件编码 | 确保 `# -*- coding: utf-8 -*-` 或直接 UTF-8 保存 |
| `ModuleNotFoundError: streamlit` | 没装 | `py -m pip install streamlit` |
| 端口被占用 | 上次没关 | `Ctrl+C` 或换端口 |
| 改了代码页面没变 | 自动重载失败 | 手动点 Rerun 或按 `R` |

---

# 十一、本次项目用到的全部新东西

## 必须掌握（今天会写）

| 名字 | 作用 |
|---|---|
| `import streamlit as st` | 导入（约定简称 st） |
| `st.title` / `st.header` / `st.subheader` | 标题层级 |
| `st.write` | 万能显示 |
| `st.text_input` | 文本输入 |
| `st.number_input` | 数字输入（带范围） |
| `st.button` | 按钮 |
| `st.form` / `st.form_submit_button` | 表单（多输入一次提交） |
| `st.selectbox` | 下拉选择 |
| `st.columns` | 横向分列 |
| `st.metric` | 指标卡（大数字） |
| `st.session_state` | **跨重跑保存数据** |
| `st.success` / `st.error` / `st.warning` | 反馈提示 |
| `st.spinner` | 加载转圈 |
| `st.divider` | 分隔线 |
| `st.expander` | 折叠面板 |
| `st.write_stream` | 流式输出 |
| `yield` | 生成器关键字 |
| `st.rerun()` | 主动刷新页面 |
| `st.stop()` | 立即停止执行 |

## 暂不需要（以后会用）

| 名字 | 什么时候用 |
|---|---|
| `st.cache_data` | 缓存耗时计算（Day 8） |
| `st.chat_message` / `st.chat_input` | 聊天界面（Day 8） |
| `st.tabs` | 选项卡 |
| `st.file_uploader` | 上传文件（RAG 项目要） |
| `st.session_state` 的 `callback` | 高级用法 |

---

# 附录：最小可运行示例

**文件 `app.py`**：

```python
import streamlit as st

st.title("我的第一个网页")
st.write("这个页面是用 Python 写的，没有一行 HTML。")

name = st.text_input("你叫什么名字？")

if name:
    st.success(f"你好，{name}！")
```

**运行**：

```powershell
streamlit run app.py
```

**浏览器打开 `http://localhost:8501`**，你应该看到标题、一个输入框，输入名字后出现绿色问候。

---

# 附录：本项目的目标结构

```
day07/
├── storage.py      ← 从 day06 复制，一行不改
├── logic.py        ← 从 day06 复制，一行不改
├── ai.py           ← 从 day06 复制，一行不改
├── app.py          ← ⭐ 新写：网页界面
└── scores.json     ← 数据文件
```

**注意**：`main.py`（命令行菜单）**不再需要** —— 网页版的逻辑在 `app.py` 里。

**关键认知**：**数据层、逻辑层、AI 层完全复用，只换界面层。** 这就是 Day 5 分层设计的回报。
