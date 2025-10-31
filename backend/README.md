# Philosophy Chatbot - Backend Usage Guide

This guide explains how to set up, test, and use the backend API for the Philosophy Chatbot, which is designed to answer questions about Dostoevsky's "The Grand Inquisitor" and his broader existential phisolophy.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Setup Instructions

### 1. Install Dependencies

Navigate to the project root and install the required packages:

```bash
pip install -r ./backend/requirements.txt
```

### 2. Activate Virtual Environment (if using one)

```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

## Running the Backend

### Start the API Server

Navigate to the backend directory and start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000` with auto-reload enabled for development.

## Testing the API

### 1. Access Interactive Documentation

Visit the automatically generated Swagger UI documentation:

```
http://127.0.0.1:8000/docs
```

This provides an interactive interface to test all API endpoints.

### 2. Alternative Documentation

You can also access the ReDoc documentation:

```
http://127.0.0.1:8000/redoc
```

## Using the Chat Endpoint

### Endpoint Information

- **URL**: `POST /chat`
- **Content-Type**: `application/json`

### Request Format

Send a POST request with the following JSON structure:

```json
{
  "question": "What does Ivan say about suffering?",
  "chat_history": []
}
```

### Request Parameters

- `question` (string, required): The philosophical question you want to ask
- `chat_history` (array, optional): Previous conversation history for context

### Example Questions

Here are some sample questions you can test with:

```json
{
  "question": "What does Ivan say about suffering?",
  "chat_history": []
}
```

```json
{
  "question": "Explain the Grand Inquisitor's argument about freedom",
  "chat_history": []
}
```

```json
{
  "question": "What is the relationship between faith and doubt in the text?",
  "chat_history": []
}
```

### Testing in Swagger UI

1. Navigate to `http://127.0.0.1:8000/docs`
2. Click on the `/chat` endpoint
3. Click "Try it out"
4. Replace the example JSON with your question:
   ```json
   {
     "question": "What does Ivan say about suffering?",
     "chat_history": []
   }
   ```
5. Click "Execute"
6. View the response in the "Response body" section

### Expected Response Format

The API will return a JSON response containing the chatbot's answer based on the Dostoevsky text.

## Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure all dependencies are installed with `pip install -r ./backend/requirements.txt`
2. **Port already in use**: If port 8000 is busy, specify a different port: `uvicorn main:app --reload --port 8001`
3. **Import errors**: Make sure you're running the command from the backend directory

### Server Logs

The server provides detailed logs in the terminal, including:
- Request information
- Processing steps
- Error messages (if any)

## Development Notes

- The `--reload` flag enables automatic server restart when code changes
- The API is built with FastAPI and includes automatic OpenAPI documentation
- The chatbot uses RAG (Retrieval-Augmented Generation) to answer questions based on "The Grand Inquisitor" text

For frontend integration, refer to the frontend documentation in the respective directory.
