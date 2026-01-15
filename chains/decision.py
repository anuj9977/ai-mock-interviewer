def decide_next_step(evaluation, state):
    quality = evaluation["quality"]

    # update depth
    if "Strong" in quality:
        state.depth = "deep"
    elif "Partial" in quality:
        state.depth = "intermediate"
    else:
        state.depth = "basic"

    # update personality (NEW)
    if state.score >= 6:
        state.personality = "pressure"
    elif state.score >= 3:
        state.personality = "strict"
    else:
        state.personality = "neutral"

    return state.depth
