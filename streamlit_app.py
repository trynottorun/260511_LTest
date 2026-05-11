import json
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="업무 분배 & 마일스톤 챗봇", page_icon="🧩", layout="wide")

st.title("🧩 업무 분배 & 마일스톤 생성 챗봇")
st.write(
    "태스크를 입력하면 업무를 세부 작업으로 나누고, 담당자와 마일스톤을 제안합니다. "
    "캘린더 등록, 외부 검색, RAG는 사용하지 않습니다."
)

openai_api_key = st.text_input("OpenAI API 키", type="password")

if "plans" not in st.session_state:
    st.session_state.plans = []

if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_PROMPT = """
너는 업무 분배 및 마일스톤 설계 보조 AI다.

목표:
- 사용자가 입력한 태스크를 실행 가능한 작업 단위로 분해한다.
- 사용자가 언급한 역할, 인원, 마감일, 우선순위를 반영한다.
- 캘린더 등록은 하지 않는다.
- 외부 검색은 하지 않는다.
- 사용자가 제공하지 않은 정보는 합리적인 가정으로 처리하되, assumptions에 명시한다.

중요 규칙:
1. 반드시 JSON만 출력한다.
2. 마크다운을 출력하지 않는다.
3. 설명 문장을 JSON 밖에 쓰지 않는다.
4. 날짜가 불명확하면 "target_date"는 null로 둔다.
5. 담당자가 명확하지 않으면 역할 기반으로 owner를 배정한다.
6. 각 task는 너무 크지 않게 실행 가능한 단위로 쪼갠다.
7. milestone은 3~6개 정도로 생성한다.
8. risks에는 일정 지연 또는 품질 저하 가능성을 적는다.

JSON 스키마:
{
  "project_title": "string",
  "summary": "string",
  "assumptions": ["string"],
  "tasks": [
    {
      "task_name": "string",
      "owner": "string",
      "priority": "높음|중간|낮음",
      "estimated_days": number,
      "dependencies": ["string"],
      "output": "string"
    }
  ],
  "milestones": [
    {
      "milestone": "string",
      "target_date": "YYYY-MM-DD 또는 null",
      "deliverable": "string"
    }
  ],
  "risks": ["string"]
}
"""


def generate_plan(client, user_task):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
다음 태스크를 업무 분배 및 마일스톤 계획으로 변환해줘.

태스크:
{user_task}
"""
            }
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "project_title": "JSON 파싱 실패",
            "summary": "모델 응답을 JSON으로 변환하지 못했습니다.",
            "assumptions": ["모델이 JSON 외 텍스트를 포함했을 수 있습니다."],
            "tasks": [],
            "milestones": [],
            "risks": [content]
        }


def render_plan(plan):
    st.subheader(f"📌 프로젝트: {plan.get('project_title', '제목 없음')}")
    st.write(plan.get("summary", ""))

    if plan.get("assumptions"):
        with st.expander("가정 사항"):
            for item in plan["assumptions"]:
                st.write(f"- {item}")

    tasks = plan.get("tasks", [])
    milestones = plan.get("milestones", [])
    risks = plan.get("risks", [])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ 업무 분배")
        if tasks:
            st.dataframe(tasks, use_container_width=True)
        else:
            st.info("생성된 업무가 없습니다.")

    with col2:
        st.markdown("### 🏁 마일스톤")
        if milestones:
            st.dataframe(milestones, use_container_width=True)
        else:
            st.info("생성된 마일스톤이 없습니다.")

    if risks:
        st.markdown("### ⚠️ 리스크")
        for risk in risks:
            st.write(f"- {risk}")


if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    st.markdown("### 입력 예시")
    st.code(
        "다음 주 금요일까지 게임 UX 분석 리포트를 완성해야 해. "
        "기획자 1명, 분석가 1명, 디자이너 1명이 있고, "
        "분석 대상은 모바일 RPG 3개야.",
        language="text"
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("태스크를 입력하세요. 예: 다음 주까지 게임 UX 분석 리포트 작성해야 해.")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("업무 분배와 마일스톤을 생성하는 중입니다."):
                plan = generate_plan(client, prompt)
                st.session_state.plans.append(plan)

                response_text = f"'{plan.get('project_title', '프로젝트')}'에 대한 업무 분배와 마일스톤을 생성했습니다."
                st.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

    st.divider()

    st.markdown("## 생성된 계획")

    if st.session_state.plans:
        latest_plan = st.session_state.plans[-1]
        render_plan(latest_plan)
    else:
        st.info("아직 생성된 계획이 없습니다.")
