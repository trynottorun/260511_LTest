# app.py

import streamlit as st
from openai import OpenAI

from styles.genesis import inject_genesis_style
from services.planner_ai import generate_plan
from components.plan_view import render_plan


st.set_page_config(
    page_title="업무 분배 & 마일스톤 설계",
    page_icon="🧩",
    layout="wide",
)

inject_genesis_style()

st.markdown("# 업무 분배 & 마일스톤 설계")
st.markdown(
    "태스크를 입력하면 실행 가능한 작업 단위로 분해하고, 담당자와 마일스톤을 구조화합니다."
)

openai_api_key = st.text_input("OpenAI API 키", type="password")

if "plans" not in st.session_state:
    st.session_state.plans = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("태스크를 입력하세요.")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("업무 분배와 마일스톤을 생성하는 중입니다."):
            plan = generate_plan(client, prompt)
            st.session_state.plans.append(plan)

            response_text = f"'{plan.get('project_title', '프로젝트')}' 계획을 생성했습니다."
            st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})

st.divider()

st.markdown("## 생성된 계획")

if st.session_state.plans:
    render_plan(st.session_state.plans[-1])
else:
    st.info("아직 생성된 계획이 없습니다.")
