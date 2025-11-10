from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from retriever import build_retriever
from langchain_openai import ChatOpenAI
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, AIMessage
from langdetect import detect
from drive_loader import download_missing_files
from db import AsyncSessionLocal
from models import ChatHistory
import os
import json

load_dotenv()

app = FastAPI()

# Allow frontend hosted on Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download text files and build retriever
download_missing_files()
retriever = build_retriever()

system_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template=
"""
You are a philosophical assistant specializing in Fyodor Dostoevsky's works and existentialist philosophy.

RESPONSE GUIDELINES:
1. Answer directly and naturally - don't always start with greetings
2. For questions about Dostoevsky's texts (Brothers Karamazov, Crime and Punishment, etc.), use the Context below to provide accurate quotes and references
3. For general philosophical questions, draw on philosophical knowledge while connecting to Dostoevskian themes when appropriate
4. Keep responses CONCISE - 2-3 short paragraphs (150-200 words maximum)
5. Be thoughtful and conversational, adapting your tone to the question

Context from Dostoevsky's texts (use when relevant):
{context}

If the user shows signs of crisis, recommend professional help."""
    ),
    HumanMessagePromptTemplate.from_template("{question}")
])

llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4o-mini",
    max_completion_tokens=250
)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    combine_docs_chain_kwargs={"prompt": system_prompt}
)

# Request model for the /chat endpoint
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: str
    question: str
    chat_history: list = []

# Agent's "brain"
def run_philosophy_agent(question: str, chat_history: list):
    formatted_history = []
    for role, content in chat_history:
        if role == "user":
            formatted_history.append(HumanMessage(content=content))
        elif role == "assistant":
            formatted_history.append(AIMessage(content=content))
        
    language = detect(question)
    language_map = {
        "en": "English",
        "pt": "Portuguese",
        "it": "Italian",
    }
    language_name = language_map.get(language, "English")

    full_question = f"Please respond in {language_name}. {question}"

    return chain.invoke({
        "question": full_question,
        "chat_history": formatted_history
    })

# Chat history
CHAT_HISTORY_DIR = "chat_sessions"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)


def load_session_history(session_id: str) -> list:
    path = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="uft-8") as f:
            return json.load(f)
    return []


def save_session_history(session_id: str, chat_history: list):
    path = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

# Request handling
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    This endpoint receives a question and an optional chat history,
    then returns a response generated from the preloaded document.
    """
    session_id = request.session_id

    result = run_philosophy_agent(request.question, request.chat_history)

    async with AsyncSessionLocal() as session:
        session.add(ChatHistory(
            session_id=session_id,
            user_message=request.question,
            bot_response = result["answer"]
        ))
        await session.commit()

    return {"answer": result["answer"]}