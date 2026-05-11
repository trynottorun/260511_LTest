# components/plan_view.py

import streamlit as st


def render_plan(plan: dict):
    st.subheader(f"프로젝트: {plan.get('project_title', '제목 없음')}")
    st.write(plan.get("summary", ""))

    assumptions = plan.get("assumptions", [])
    tasks = plan.get("tasks", [])
    milestones = plan.get("milestones", [])
    risks = plan.get("risks", [])

    if assumptions:
        with st.expander("가정 사항"):
            for item in assumptions:
                st.write(f"- {item}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 업무 분배")
        if tasks:
            st.dataframe(tasks, use_container_width=True)
        else:
            st.info("생성된 업무가 없습니다.")

    with col2:
        st.markdown("### 마일스톤")
        if milestones:
            st.dataframe(milestones, use_container_width=True)
        else:
            st.info("생성된 마일스톤이 없습니다.")

    if risks:
        st.markdown("### 리스크")
        for risk in risks:
            st.write(f"- {risk}")
