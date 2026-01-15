from langchain_core.messages import SystemMessage, HumanMessage

def ask_question(llm, state, last_answer=None):
    system = SystemMessage(
        content=open("prompts/interviewer.txt").read().format(
            role=state.role,
            difficulty=state.difficulty,
            depth=state.depth,
            personality=state.personality
        )
    )

    if last_answer:
        human = HumanMessage(
            content=f"""
Candidate answered:
{last_answer}

Ask the next interview question.
"""
        )
    else:
        human = HumanMessage(
            content="Start the interview with the first question."
        )

    response = llm.invoke([system, human])
    return response.content
