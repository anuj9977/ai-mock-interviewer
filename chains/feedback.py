from langchain_core.messages import SystemMessage, HumanMessage

def generate_feedback(llm, state):
    history_text = ""

    for i, (q, a) in enumerate(state.history(), start=1):
        history_text += f"\nQ{i}: {q}\nA{i}: {a}\n"

    system = SystemMessage(
        content="""
You are a senior technical interviewer.

Based on the full interview, generate a realistic interview feedback.

Rules:
- Be honest and professional
- Do not sugarcoat
- Give actionable advice
"""
    )

    human = HumanMessage(
        content=f"""
Interview role: {state.role}
Difficulty level: {state.difficulty}
Final depth reached: {state.depth}
Final score: {state.score}

Interview transcript:
{history_text}

Provide:
1. Overall performance summary
2. Strengths
3. Weaknesses
4. Improvement suggestions
"""
    )

    response = llm.invoke([system, human])
    return response.content
