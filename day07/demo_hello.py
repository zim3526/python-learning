# ===== 最小可运行示例：感受 Streamlit =====
# 运行：streamlit run demo_hello.py
# 然后在浏览器里操作，观察「每次交互脚本都会重跑」

import streamlit as st

# ---------- 页面标题 ----------
st.title("我的第一个网页")
st.caption("这个页面完全用 Python 写，没有一行 HTML")

st.divider()

# ---------- ① 输入组件 ----------
st.header("① 输入")
name = st.text_input("你叫什么名字？")

if name:
    st.success(f"你好，{name}！")

st.divider()

# ---------- ② 演示「重跑」：普通变量 ----------
st.header("② 普通变量 —— 每次重跑都会被重置")
normal_count = 0

if st.button("给普通变量加一"):
    normal_count += 1

st.write(f"普通变量当前值：**{normal_count}**（无论点几次都是 1）")

st.divider()

# ---------- ③ 演示「重跑」：session_state ----------
st.header("③ session_state —— 跨重跑保留")

# 初始化：只在第一次执行
if "persist_count" not in st.session_state:
    st.session_state.persist_count = 0

if st.button("给 session_state 加一"):
    st.session_state.persist_count += 1

st.write(f"session_state 当前值：**{st.session_state.persist_count}**（点几次就加几次）")

st.divider()

# ---------- ④ 数字输入 + 指标卡 ----------
st.header("④ 数字输入和指标卡")

score = st.number_input("输入一个分数", min_value=0, max_value=100, value=85)

col1, col2, col3 = st.columns(3)
col1.metric("分数", score)
col2.metric("是否及格", "是" if score >= 60 else "否")
col3.metric("等级", (
    "优秀" if score >= 90 else
    "良好" if score >= 80 else
    "及格" if score >= 60 else
    "不及格"
))

st.divider()

# ---------- ⑤ 折叠面板 ----------
with st.expander("点开看说明"):
    st.write("右上角会显示脚本正在运行。每次你点按钮或输入文字，整个脚本都会从头执行一遍。")
