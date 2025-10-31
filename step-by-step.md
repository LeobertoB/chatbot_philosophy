# Step-by-step

## 1. Create FastAPI skeleton = main.py
## 2. Define input model for / chat endpoint = ChatRequest
## 3. Load and chunk the document
## 4. Generate embeddings and store in vector index
## 5. Create ConversationalRetrievalChain with LangChain
## 6. Call the chain inside your / chat endpoint
## 7. Hook up frontend