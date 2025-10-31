from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from retriever import build_retriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Allow frontend hosted on Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # substitua por ["https://seu-frontend.vercel.app"] em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = build_retriever()

qa_prompt = PromptTemplate.from_template("""   
You are an existentialist philosofical trained on Dostoevsky's "The Grand Inquisitor".
Answer the user's questions with depth and reasoning. If the document does no
explicitly mention a topic, use related ideas and internal knowledge from the 
text and general philosophical reasoning to respond meaningfully.
Include references to the ideas of characters (like Ivan or Alyosha), even if not
word-for-word from the text. 
Be clear when you’re speculating or expanding philosophically beyond the text.
Keep your responses concise and focused, no longer than 3 paragraphs.

Question: {question}
Chat history: {chat_history}
Documents: {context}
                                         
Your response:
""")

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    max_completion_tokens=500
)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    combine_docs_chain_kwargs={"prompt": qa_prompt}
)

# Request model for the /chat endpoint
class ChatRequest(BaseModel):
    question: str
    chat_history: list = []

# POST endpoint to handle chat interactions
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    This endpoint receives a question and an optional chat history,
    then returns a response generated from the preloaded document.
    """
    result = chain({
        "question": request.question,
        "chat_history": request.chat_history
    })

    return {"answer": result["answer"]}