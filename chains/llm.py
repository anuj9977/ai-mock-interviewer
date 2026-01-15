from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-70B-Instruct",
        task="text-generation",
        max_new_tokens=220,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.05,
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
    )

    llm = ChatHuggingFace(llm=endpoint)
    return llm
