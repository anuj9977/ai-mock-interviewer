def score_answer(state, evaluation):
    """
    evaluation: Strong | Partial | Weak
    """

    if "Strong" in evaluation:
        state.update_score(2)
    elif "Partial" in evaluation:
        state.update_score(1)
    else:
        state.update_score(0)
