# services/planner_ai.py

import json


SYSTEM_PROMPT = """
너는 업무 분배 및 마일스톤 설계 보조 AI다.

규칙:
1. 사용자가 입력한 태스크를 실행 가능한 작업 단위로 분해한다.
2. 담당자, 역할, 마감일, 우선순위를 반영한다.
3. 캘린더 등록은 하지 않는다.
4. 외부 검색은 하지 않는다.
5. 반드시 JSON만 출력한다.
"""


def generate_plan(client, user_task: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"다음 태스크를 업무 분배 및 마일스톤 계획으로 변환해줘:\n{user_task}",
            },
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
            "assumptions": [],
            "tasks": [],
            "milestones": [],
            "risks": [content],
        }
