import streamlit as st
from storage import load_scores, save_scores
from logic import calc_stats
from ai import calc_level, generate_comment

st.set_page_config(page_title="成绩管理", page_icon="📊", layout="wide")

# ① 初始化：从文件加载（只在第一次）
if "scores" not in st.session_state:
    st.session_state.scores = load_scores()

# ② 顶部标题 + 概览
st.title("📊 学生成绩管理系统")
scores = st.session_state.scores
if scores:
    avg = sum(scores.values()) / len(scores)
    st.caption(f"共 {len(scores)} 名学生 · 平均分 {avg:.2f}")
else:
    st.caption("共 0 名学生 · 暂无数据")

# ③ 四个选项卡
tab1, tab2, tab3, tab4 = st.tabs(["录入", "全部成绩", "统计", "AI 评语"])

with tab1:
    st.header("录入成绩")
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
            save_scores(st.session_state.scores)
            st.success("成功")


with tab2:
    st.header("全部成绩")
    if not st.session_state.scores:
        st.info("暂无数据")
    else:
        rows = [{"姓名": n, "分数": s} for n, s in st.session_state.scores.items()]
        st.dataframe(rows, use_container_width=True)

    if st.session_state.scores:
        del_name = st.selectbox("选择要删除的学生",list(st.session_state.scores.keys()))
        if st.button("删除"):
            del st.session_state.scores[del_name]
            save_scores(st.session_state.scores)
            st.rerun()

with tab3:
    st.header("统计")
    if not st.session_state.scores:
        st.info("暂无数据")
    else:
        stats = calc_stats(st.session_state.scores)
        col1, col2, col3 = st.columns(3)

        col1.metric("总人数", stats["count"])
        col2.metric("平均分", f"{stats['average']:.2f}")
        col3.metric("及格人数", stats["pass_count"])

    st.subheader("成绩明细")

    if not st.session_state.scores:
        st.info("暂无数据")
    else:
        rows = []
        # 按分数从高到低排序
        sorted_scores = sorted(
            st.session_state.scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        for rank, (name, score) in enumerate(sorted_scores, 1):
            rows.append({
                "排名": rank,
                "姓名": name,
                "分数": score,
                "等级": calc_level(score),
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)


with tab4:
    st.header("评语")
    if not st.session_state.scores:
         st.info("暂无数据")
    else:
        review_name = st.selectbox("请选择学生：",list(st.session_state.scores.keys()))
        if st.button("生成评语"):
            with st.spinner("正在生成..."):
                review = generate_comment(review_name, st.session_state.scores[review_name])
            
       
            if review is None:
                st.error("生成失败，请检查网络或 API 配置")
            else:
                st.metric("等级", review["等级"])
                st.write(f"评语：{review['评语']}")
                st.write(f"建议：{review['建议']}")



