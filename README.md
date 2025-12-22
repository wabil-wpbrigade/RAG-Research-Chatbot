# 🚀 RAG-Based Document Chatbot (Production-Oriented)

*A full-stack Retrieval-Augmented Generation (RAG) chatbot with passwordless magic link authentication, email automation, and Dockerized services.*

---

## 📌 Overview

This project is a **production-oriented RAG (Retrieval-Augmented Generation) chatbot** designed to answer user queries based on **private documents** such as PDFs.

Unlike generic chatbots, this system:

* Retrieves relevant document chunks using vector similarity
* Grounds all answers strictly in retrieved context
* Prevents hallucinations
* Supports secure **passwordless authentication via magic links**
* Is fully **containerized** for deployment

The project was developed during a **software house internship**, focusing on **clean architecture, real-world auth flows, and scalable backend design**.

> ⚠️ Note: This version implements **standard RAG**. Advanced techniques (Adaptive RAG, CRAG, query rewriting, etc.) are planned but **not yet implemented**.

---

## ✨ Key Features

### 🔍 Retrieval-Augmented Generation (RAG)

* PDF ingestion and chunking
* Vector embeddings using OpenAI
* Similarity-based document retrieval
* Context-grounded LLM responses

### 🔐 Magic Link Authentication (Passwordless)

* Email-based login links
* Token hashing & expiry
* Anti-enumeration security
* One-time-use tokens
* Secure verification flow

### 📧 Email Bot (Daemon Service)

* Watches an email outbox directory
* Processes `.eml` files
* Sends emails via SMTP (Gmail)
* Runs independently as a background service

### 🧱 Clean Backend Architecture

* FastAPI backend
* Modular services (auth, RAG, email)
* SQLAlchemy ORM
* Token-based authentication

### 🖥️ React Frontend

* Login with magic link
* RAG chat interface
* Admin dashboard (role-based)
* Clean, minimal UI

### 🐳 Fully Dockerized

* Backend service
* Frontend service
* Email bot service
* Shared volumes
* Environment-based configuration

---

## 🧠 System Architecture

```
┌────────────┐
│   Frontend │  (React)
└─────┬──────┘
      │ HTTP
┌─────▼──────┐
│   Backend  │  (FastAPI)
│            │
│ ┌────────┐ │
│ │  Auth  │ │  Magic Link Tokens
│ └────────┘ │
│ ┌────────┐ │
│ │  RAG   │ │  Retrieval + LLM
│ └────────┘ │
└─────┬──────┘
      │
      ▼
┌──────────────┐
│ ChromaDB     │  Vector Store
└──────────────┘

┌──────────────┐
│  Email Bot   │  (Daemon)
│  (Docker)   │
└─────┬────────┘
      │
  SMTP (Gmail)
```

---

## 🛠 Tech Stack

### Backend

* Python 3.12
* FastAPI
* LangChain
* ChromaDB
* OpenAI GPT-4o
* SQLAlchemy
* Jinja2
* python-dotenv

### Frontend

* React
* JavaScript
* Vite

### Email

* SMTP (Gmail App Password)
* `.eml` file-based outbox
* Background daemon

### DevOps

* Docker
* Docker Compose

---

## 🔄 How the Magic Link Flow Works

1. User enters email on frontend
2. Backend generates a secure token
3. Token is hashed and stored in DB with expiry
4. Backend writes an `.eml` file to shared volume
5. Email bot detects the file and sends the email
6. User clicks the magic link
7. Backend verifies:

   * token validity
   * expiry
   * single-use
8. JWT token is issued
9. User is logged in

---

## 📄 RAG Flow (Current Version)

1. PDFs are loaded and parsed
2. Text is split into overlapping chunks
3. Chunks are embedded using OpenAI embeddings
4. Vectors are stored in ChromaDB
5. User query is embedded
6. Top-K similar chunks are retrieved
7. Context is injected into a structured prompt
8. GPT-4o generates a grounded response

---

## 📁 Project Structure

```
RAG-Research-Chatbot/
│
├── backend/
│   └── app/
│       ├── auth/              # Magic link auth
│       ├── data/              # DB storage
│       ├── db/                # Models & DB creation
│       ├── rag/               # RAG pipeline and Prompt
│       ├── email/             # EML writer
│       ├── users/             # User/Admin endpoints
│       └── main.py            # FASTAPI 
│
├── frontend/
│   └── src/
│       ├── api/               # API functions
│       ├── components/        # Admin dashboard, RagChat etc
│       ├── pages/             # MagicLink Login
│       ├── styles/            # CSS files
│       ├── App.jsx            
│       └── Main.jsx             
│
├── email_bot/
│   ├── config.py               
│   ├── eml_parser.py
│   ├── main.py                 # Daemon loop
│   ├── smtp_client.py
│   └── worker.py
│
├── vector_database/
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🐳 Running the Project (Docker)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/wabil-wpbrigade/RAG-Research-Chatbot.git
cd RAG-Research-Chatbot
```

### 2️⃣ Create `.env`

```env
OPENAI_API_KEY=your_key
FRONTEND_URL=http://localhost:4173

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_gmail@gmail.com
```

### 3️⃣ Start All Services

```bash
docker compose up --build
```

* Frontend → [http://localhost:4173](http://localhost:4173)
* Backend → [http://localhost:8000](http://localhost:8000)

---

## 🚧 Current Limitations

* Uses **standard RAG only**
* No adaptive retrieval
* No query rewriting
* No feedback loops

These were intentionally deferred per review instructions.

---

## 🔮 Future Improvements

* Adaptive RAG
* Corrective RAG
* Query rewriting
* Reranking
* Streaming responses
* Role-based permissions
* Observability & logging

---

## 🎯 Why This Project Matters

This project demonstrates:

* Real-world authentication patterns
* Background worker design
* Clean API architecture
* Practical RAG implementation
* Production-ready containerization

It is suitable for:

* Internal knowledge bases
* Research assistants
* Corporate document search
* SaaS-style AI products

---
