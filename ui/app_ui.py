import streamlit as st
import requests
import base64




BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Mock Interviewer", layout="centered")

st.title("🎯 AI Mock Interviewer")

# -------- SIDEBAR --------
st.sidebar.header("Interview Setup")

role = st.sidebar.selectbox(
    "Select Role",
    ["Data Scientist", "Backend Developer", "Web Developer", "DSA"]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

# -------- SESSION STATE --------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "interview_active" not in st.session_state:
    st.session_state.interview_active = False


# -------- START INTERVIEW --------
if st.sidebar.button("Start Interview"):
    response = requests.post(
        f"{BACKEND_URL}/start-interview",
        params={"role": role, "difficulty": difficulty}
    )

    question = response.json()["question"]

    st.session_state.messages = [
        {"role": "interviewer", "content": question}
    ]
    st.session_state.interview_active = True


# -------- CHAT WINDOW --------
st.subheader("Interview")

for msg in st.session_state.messages:
    if msg["role"] == "interviewer":
        st.markdown(f"**🧑‍💼 Interviewer:** {msg['content']}")
    else:
        st.markdown(f"**🙋 You:** {msg['content']}")


# -------- USER ANSWER --------
if st.session_state.interview_active:
    user_answer = st.text_input("Your answer:")

    if st.button("Submit Answer"):
        st.session_state.messages.append(
            {"role": "user", "content": user_answer}
        )

        response = requests.post(
            f"{BACKEND_URL}/answer",
            params={"answer": user_answer}
        ).json()

        if "next_question" in response:
            st.session_state.messages.append(
                {"role": "interviewer", "content": response["next_question"]}
            )
        else:
            st.session_state.interview_active = False
            st.info(response["message"])


# -------- END INTERVIEW --------
if st.sidebar.button("End Interview"):
    response = requests.post(f"{BACKEND_URL}/end-interview").json()

    st.subheader("📋 Interview Feedback")
    st.markdown(response["feedback"])

# -------- VOICE ANSWER --------
st.subheader("🎙️ Answer with Voice")

if "voice_key" not in st.session_state:
    st.session_state.voice_key = 0

audio_file = st.audio_input(
    "Speak your answer",
    key=f"voice_{st.session_state.voice_key}"
)

if audio_file and st.button("Submit Voice Answer"):
    files = {"file": audio_file.getvalue()}

    try:
        response = requests.post(
            f"{BACKEND_URL}/answer-audio",
            files=files,
            timeout=120
        )
    except Exception:
        st.error("❌ Backend not reachable")
        st.stop()

    if response.status_code != 200:
        st.error("❌ Backend error during audio processing")
        st.code(response.text)
        st.stop()

    data = response.json()

    st.session_state.messages.append(
        {"role": "user", "content": data.get("transcript", "")}
    )

    st.session_state.messages.append(
        {"role": "interviewer", "content": data["next_question"]}
    )

    if "audio_reply" in data:
        audio_bytes = bytes.fromhex(data["audio_reply"])
        st.audio(audio_bytes, format="audio/mp3")

    # 🔥 RESET MIC FOR NEXT QUESTION
    st.session_state.voice_key += 1
    st.rerun()

