from fastapi import FastAPI
from chains.llm import get_llm
from chains.interview_flow import ask_question
from chains.evaluation import evaluate_answer
from chains.decision import decide_next_step
from chains.scoring import score_answer
from chains.state import InterviewState
from chains.feedback import generate_feedback
from fastapi import UploadFile, File
from audio.stt import speech_to_text
from audio.tts import text_to_speech


app = FastAPI(title="AI Mock Interviewer")

llm = get_llm()
state: InterviewState | None = None


@app.get("/")
def health():
    return {"status": "Server running"}


@app.post("/start-interview")
def start_interview(role: str, difficulty: str):
    global state

    # Initialize interview state
    state = InterviewState(role=role, difficulty=difficulty)

    # Ask first question
    first_question = ask_question(llm, state)
    state.questions_asked.append(first_question)

    return {
        "question": first_question,
        "role": role,
        "difficulty": difficulty
    }


@app.post("/answer")
def answer(answer: str):
    global state

    if state is None:
        return {"error": "Interview not started"}

    # 1️⃣ Evaluate the answer
    evaluation = evaluate_answer(llm, answer)

    # 2️⃣ Update score
    score_answer(state, evaluation["quality"])

    # 3️⃣ Update depth & personality
    decide_next_step(evaluation, state)

    # 4️⃣ Store last Q&A
    last_question = state.questions_asked[-1]
    state.add_turn(last_question, answer)

    # 🔥 STEP 1.6 — INTERVIEW END CONDITION
    if state.is_interview_complete():
        return {
            "message": "Interview completed. Please call /end-interview to view feedback.",
            "final_score": state.score,
            "final_depth": state.depth
        }

    # 5️⃣ Ask next question
    next_question = ask_question(
        llm,
        state,
        last_answer=answer
    )

    state.questions_asked.append(next_question)

    return {
        "evaluation": evaluation["quality"],
        "score": state.score,
        "depth": state.depth,
        "personality": state.personality,
        "next_question": next_question
    }


@app.post("/end-interview")
def end_interview():
    global state

    if state is None:
        return {"error": "No interview in progress"}

    # Generate final feedback
    feedback = generate_feedback(llm, state)

    result = {
        "role": state.role,
        "difficulty": state.difficulty,
        "final_score": state.score,
        "final_depth": state.depth,
        "final_personality": state.personality,
        "feedback": feedback
    }

    # Reset interview
    state = None
    return result
@app.post("/answer-audio")
async def answer_audio(file: UploadFile = File(...)):
    global state

    if state is None:
        return {"error": "Interview not started"}

    audio_bytes = await file.read()

    # 1️⃣ Speech → Text
    text_answer = speech_to_text(audio_bytes)

    # 2️⃣ Reuse existing logic
    evaluation = evaluate_answer(llm, text_answer)
    score_answer(state, evaluation["quality"])
    decide_next_step(evaluation, state)

    last_question = state.questions_asked[-1]
    state.add_turn(last_question, text_answer)

    if state.is_interview_complete():
        return {"message": "Interview completed. Please end interview."}

    next_question = ask_question(llm, state, last_answer=text_answer)
    state.questions_asked.append(next_question)

    # 3️⃣ Text → Speech
    audio_reply = text_to_speech(next_question)

    return {
        "transcript": text_answer,
        "next_question": next_question,
        "audio_reply": audio_reply.hex()  # send as hex
    }
