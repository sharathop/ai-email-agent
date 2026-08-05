# 🤖 AI Email Agent

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Queue-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-7B2CBF?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3-00A67E?style=for-the-badge)

</p>

<p align="center">

An AI-powered Email Agent that automatically analyzes recruiter emails, retrieves relevant information from a personal knowledge base using Retrieval-Augmented Generation (RAG), and generates professional response drafts.

</p>

---

# 📌 Project Overview

AI Email Agent is an intelligent recruitment email automation system designed to demonstrate how Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Vector Databases, and Background Workers can be combined to automate professional email communication.

Instead of relying on predefined templates, the system understands recruiter intent, retrieves relevant information from a semantic knowledge base built from resumes, technical skills, project documentation, GitHub, LinkedIn, and personal profile information, and generates personalized, context-aware email drafts.

The project follows a modular architecture using FastAPI, Redis, ChromaDB, Groq LLM, SQLite, and Streamlit.

---

# 🎯 Key Features

- 🤖 AI-powered email classification
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic search using ChromaDB
- ⚡ Asynchronous background processing with Redis
- 📄 Resume-aware response generation
- 📂 Knowledge base built from Markdown documents
- 🔄 Modular Agent Architecture
- 📊 Interactive Streamlit dashboard
- 💾 SQLite-based email storage

---

# 🏗️ System Architecture

```text
                        Streamlit Dashboard
                                │
                                ▼
                         FastAPI Backend
                                │
                       Store Email in SQLite
                                │
                                ▼
                           Redis Queue
                                │
                                ▼
                      Background Worker
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
        Email Classification             Agent Router
                                                 │
                            ┌────────────────────┴──────────────────┐
                            ▼                                       ▼
                     RAG Retriever                           Utility Tools
                            │
                            ▼
                  ChromaDB Vector Database
                            │
                            ▼
                     Groq Llama 3.3 70B
                            │
                            ▼
                   AI Generated Email Draft
                            │
                            ▼
                       SQLite Database
                            │
                            ▼
                     Streamlit Dashboard
```

---

# 🧠 AI Workflow

Every email passes through the following stages:

1. User submits a recruiter email from the Streamlit dashboard.
2. FastAPI stores the email in SQLite.
3. Email ID is pushed into a Redis queue.
4. A background worker continuously monitors the queue.
5. The email is classified based on its intent.
6. The Agent Router selects the appropriate workflow.
7. Relevant information is retrieved from ChromaDB.
8. Retrieved context is combined with the email.
9. Groq Llama 3.3 generates a professional response draft.
10. The generated draft is stored in the database and displayed on the dashboard.

---

# 📚 Knowledge Base

The Retrieval-Augmented Generation pipeline uses a semantic knowledge base built from structured Markdown documents and resume content.

Knowledge sources include:

- Resume
- Technical Skills
- Education
- Personal Profile
- GitHub Profile
- LinkedIn Profile
- Project Documentation

Each document is chunked, embedded using Sentence Transformers, and indexed into ChromaDB for semantic retrieval.

---

# 🔍 Retrieval-Augmented Generation (RAG)

Instead of relying solely on the LLM's internal knowledge, the system retrieves relevant information from a personal knowledge base before generating a response.

This approach:

- Produces personalized responses
- Reduces hallucinations
- Improves factual accuracy
- Keeps answers grounded in real project experience

The retrieved context is injected into the LLM prompt, enabling the model to generate accurate and context-aware email drafts.

---

# 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI, SQLAlchemy |
| AI | Groq Llama 3.3, Prompt Engineering |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Queue | Redis |
| Database | SQLite |
| Frontend | Streamlit |

---

# 📂 Project Structure
```text
AI-Email-Agent/
│
├── agent/
│   ├── classifier.py         # Email classification
│   ├── router.py             # Agent routing logic
│   └── tools.py              # Utility tools
│
├── rag/
│   ├── ingest.py             # Knowledge base indexing
│   ├── retriever.py          # ChromaDB retrieval
│   └── prompt_builder.py     # Prompt construction
│
├── knowledge/                
│   ├── profile.md
│   ├── education.md
│   ├── skills.md
│   ├── github.md
│   ├── linkedin.md
│   ├── projects/
│   └── resume.pdf
│
├── agent/
├── rag/
├── app.py                    # FastAPI application
├── worker.py                 # Background worker
├── streamlit_app.py          # Dashboard
├── llm.py                    # Groq LLM integration
├── database.py               # Database configuration
├── model.py                  # SQLAlchemy models
├── schemas.py                # Pydantic schemas
├── queue_service.py          # Redis queue
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

# 📊 Streamlit Dashboard

The interactive dashboard allows users to:

- Submit recruiter emails
- Monitor processing status
- View email history
- Read AI-generated drafts
- Test the complete AI pipeline from a single interface

> *(Add screenshots here)*

```
images/
├── dashboard.png
├── compose-email.png
└── generated-draft.png
```

---

# 📨 Example Workflow

### Recruiter Email

```
Subject:
Questions About Your RAG Project

Body:

Hi Sharath,

I was impressed by your Self-Correcting RAG Pipeline.

Could you explain its architecture, technologies used, and the challenges you faced while building it?

Regards,
Technical Recruiter
```

↓

### AI Processing

- Email Classification
- Agent Routing
- Semantic Retrieval
- Prompt Construction
- LLM Response Generation

↓

### Output

A professional, personalized response draft generated using relevant information from the knowledge base.

---

# 🚀 Future Enhancements

- Gmail API Integration
- Outlook Integration
- Automatic Inbox Monitoring
- Conversation Memory
- Metadata-based Retrieval
- Human Approval Workflow
- Docker Deployment
- PostgreSQL Support
- Cloud Deployment

---

# 👨‍💻 Author

**Sharath M**

**AI | Machine Learning | Generative AI**

📧 Email: sharathparajji@gmail.com

🔗 GitHub: https://github.com/sharathop

🔗 LinkedIn: https://www.linkedin.com/in/sharath-m-62791a257

---

# ⭐ If you found this project interesting, consider giving it a star!
