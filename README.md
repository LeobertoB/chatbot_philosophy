# Dostoevsky AI Philosopher

An AI-powered chatbot for philosophical conversations based on the works of Fyodor Dostoevsky. The application uses retrieval-augmented generation to provide contextually accurate responses grounded in texts such as "The Brothers Karamazov", "Crime and Punishment", "White Nights", and "The Grand Inquisitor".

![Dostoevsky AI Philosopher](https://img.shields.io/badge/Philosophy-AI%20Powered-purple?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-green?style=for-the-badge&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-blue?style=for-the-badge&logo=openai)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Styling-blue?style=for-the-badge&logo=tailwindcss)

## Overview

This application enables users to explore existential themes through AI-driven dialogue. Topics include suffering, freedom, faith, doubt, and human nature. The system maintains conversation history across sessions and provides responses in multiple languages including English, Portuguese, and Italian.

**Live Application:** [https://dostoevksyaiphilosopher.com/](https://dostoevksyaiphilosopher.com/)

## Features

- Context-aware conversations using retrieval-augmented generation
- Session-based chat history with PostgreSQL persistence
- Multi-language support with automatic detection
- Real-time document retrieval from Google Drive
- Responsive web interface with dark mode support
- Safety measures for harmful content detection

## Prerequisites

- Node.js 18+ and npm or yarn
- Python 3.8+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- PostgreSQL database (optional for local development)
- Google Drive API credentials (for document loading)
- LangChain API Key (optional, for tracing) ([Get one here](https://smith.langchain.com/))

## Installation

### Clone the Repository

```bash
git clone https://github.com/LeobertoB/chatbot_philosophy.git
cd chatbot_philosophy
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `backend/.env` with your credentials:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Optional
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
OPENAI_PROJECT=your_project_id_here
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_CREDENTIALS_JSON={"type": "service_account", ...}
```

### Database Setup

```bash
# Run migrations
cd backend
alembic upgrade head
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

Update the API endpoint in `frontend/lib/api.ts` if needed.

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload
```

The backend API will be available at `http://127.0.0.1:8000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Documentation

Access the interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Main Endpoint

**POST** `/chat`

Request body:
```json
{
  "session_id": "unique_session_identifier",
  "question": "What does Ivan say about suffering?",
  "chat_history": []
}
```

Response:
```json
{
  "answer": "Ivan Karamazov presents a profound challenge to traditional theodicy..."
}
```

## Project Structure

```
chatbot_philosophy/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── retriever.py         # RAG implementation
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── drive_loader.py      # Google Drive integration
│   ├── requirements.txt     # Python dependencies
│   ├── alembic/             # Database migrations
│   └── data/                # Document storage
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main chat interface
│   │   ├── layout.tsx       # Application layout
│   │   └── globals.css      # Styles and animations
│   ├── lib/
│   │   └── api.ts           # API client
│   └── package.json         # Node.js dependencies
└── README.md
```

## Technology Stack

### Backend

- FastAPI: Web framework for building APIs
- LangChain: Framework for LLM applications
- OpenAI GPT-4: Language model
- FAISS: Vector database for document retrieval
- SQLAlchemy: ORM for database operations
- PostgreSQL: Relational database
- Alembic: Database migration tool
- Python-dotenv: Environment variable management

### Frontend

- Next.js 14: React framework with App Router
- TypeScript: Type-safe JavaScript
- Tailwind CSS: Utility-first CSS framework
- React Hooks: State and effect management

## Configuration

### Environment Variables

Backend (`backend/.env`):
```env
OPENAI_API_KEY=required
LANGCHAIN_API_KEY=optional
DATABASE_URL=postgresql+asyncpg://...
GOOGLE_DRIVE_FOLDER_ID=optional
GOOGLE_CREDENTIALS_JSON=optional
```

### CORS Settings

The backend accepts requests from all origins by default. Update `backend/main.py` to restrict origins in production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    ...
)
```

## Deployment

### Backend (Railway)

1. Connect your repository to Railway
2. Set environment variables in the Railway dashboard
3. Deploy automatically from the main branch

### Frontend (Vercel)

1. Connect your repository to Vercel
2. Configure build settings:
   - Build command: `npm run build`
   - Output directory: `.next`
3. Deploy automatically from the main branch

### Production Environment Variables

Ensure these are configured in your hosting platform:

- `OPENAI_API_KEY`
- `DATABASE_URL`
- `LANGCHAIN_API_KEY` (optional)
- `GOOGLE_DRIVE_FOLDER_ID` (optional)
- `GOOGLE_CREDENTIALS_JSON` (optional)

Update the API endpoint in `frontend/lib/api.ts` to point to your production backend URL.

## Example Questions

- What does Ivan say about suffering?
- Explain the Grand Inquisitor's argument about freedom
- What is the relationship between faith and doubt?
- How does Dostoevsky view human nature?
- Why does the Grand Inquisitor reject Christ?
- What is the significance of the kiss at the end?

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Fyodor Dostoevsky for the philosophical works
- OpenAI for GPT models
- LangChain for the LLM application framework
- Vercel for Next.js and deployment platform
- Railway for backend hosting
