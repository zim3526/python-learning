import streamlit as st
from logic import calc_stats

st.title("学生成绩管理")

# ---------- ① 初始化 session_state ----------
if "scores" not in st.session_state:
    st.session_state.scores = {}

# ---------- ② 录入表单 ----------
st.subheader("录入成绩")
with st.form("录入表单", clear_on_submit=True):
    name = st.text_input("姓名")
    score = st.number_input("分数", min_value=0, max_value=100, value=0)
    submitted = st.form_submit_button("添加")

if submitted:
    clean_name = name.strip()

    if not name.strip():
        st.warning("姓名不能为空")
    else:
        st.session_state.scores[clean_name] = score
        st.success("成功")

    

# ---------- ③ 统计区 ----------
st.subheader("统计")

if not st.session_state.scores:
    st.info("暂无数据")
else:
    stats = calc_stats(st.session_state.scores)
    col1,col2,col3 = st.columns(3)
    
    col1.metric("总人数：", stats["count"])
    
    col2.metric("平均分：", f"{stats['average']:.2f}")
    
    col3.metric("及格人数：", stats["pass_count"])

# ---------- ④ 列表区 ----------
st.subheader("全部成绩")

if not st.session_state.scores:
    st.info("暂无数据")
else:
    for n,s in st.session_state.scores.items():
        st.write(f"姓名：{n}   分数：{s}")

rows = [{"姓名": n, "分数": s} for n, s in st.session_state.scores.items()]
st.dataframe(rows, use_container_width=True)