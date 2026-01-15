from langchain_core.runnables import RunnableParallel

def evaluate_answer(llm, answer):
    result = RunnableParallel(
        quality=lambda _: llm.invoke(
            f"Classify the following answer as Strong, Partial, or Weak:\n{answer}"
        ).content,

        feedback=lambda _: llm.invoke(
            f"In one line, say what was missing or good in this answer:\n{answer}"
        ).content
    ).invoke({})

    return result
