# Physiotherapy AI Receptionist

A production-oriented AI receptionist: conversational booking, RAG-backed FAQ
answering, voice + WhatsApp channels, and an admin dashboard — built to be
re-skinned later for dentists, salons, vets, and other appointment-based
businesses.

Built in phases. Each phase is runnable and tested on its own before the next
one starts.

## Phase roadmap

| # | Phase | What it delivers |
|---|-------|-------------------|
| 1 | **Project Foundation** ✅ | Repo layout, Docker Compose, FastAPI skeleton, async DB connection, config/logging, Alembic wired up |
| 2 | **Database Models** ✅ | SQLAlchemy models for every entity (Patients, Appointments, Conversations, Messages, KnowledgeDocuments, Doctors, ClinicSettings, Users, Notifications) + first migration |
| 3 | Auth & Security | JWT auth, role-based access (admin/staff), password hashing, rate limiting, input validation |
| 4 | Core AI Agent (LangGraph) | Agent graph, system prompt, conversation state, LLM wrapper — no tools yet, just a receptionist that talks |
| 5 | RAG System | Document upload (PDF/DOCX/TXT), chunking, embeddings, ChromaDB, "search knowledge base" tool |
| 6 | Appointment Tools | Google Calendar integration, availability checking, book/cancel/reschedule tools, double-booking prevention |
| 7 | Patient Intake & Memory | Structured intake flow, patient records, returning-patient recall |
| 8 | Chat API | `/chat` endpoint wiring the agent + all tools together end-to-end |
| 9 | Voice Channel | Vapi/Deepgram/ElevenLabs webhook handlers reusing the same agent |
| 10 | WhatsApp Channel | Twilio webhook, WhatsApp booking/FAQ/reminders reusing the same agent |
| 11 | Frontend: Chat + Booking UI | Next.js chat widget, appointment calendar |
| 12 | Frontend: Admin Dashboard | Patients, conversations, analytics, knowledge base management |
| 13 | Deployment | Production Docker images, Railway/Azure config, CI |

Every phase after this one plugs into the structure below without breaking
what came before — that's the point of the placeholder folders and the
already-declared (but currently unused) settings in `.env.example`.

## Architecture

```
                         ┌─────────────────────┐
                         │   Next.js Frontend    │
                         │ (chat / calendar /    │
                         │  admin dashboard)      │
                         └──────────┬────────────┘
                                    │ REST (JWT)
                         ┌──────────▼────────────┐
                         │     FastAPI Backend    │
                         │  routes → services      │
                         └─────┬──────┬──────┬────┘
                               │      │      │
                 ┌─────────────┘      │      └─────────────┐
                 ▼                    ▼                    ▼
        ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐
        │  LangGraph      │  │   PostgreSQL     │  │   ChromaDB        │
        │  Receptionist   │  │ (patients, appts,│  │ (clinic docs /    │
        │  Agent + Tools  │  │  conversations)  │  │  FAQ embeddings)  │
        └───┬─────┬───┬───┘  └─────────────────┘  └──────────────────┘
            │     │   │
            ▼     ▼   ▼
      Google   Twilio  Vapi/Deepgram/
      Calendar WhatsApp ElevenLabs (voice)
```

## Repository layout

```
backend/
  app/
    agents/      # LangGraph graphs (Phase 4)
    tools/       # Agent tools: booking, RAG search, etc. (Phases 5-7)
    rag/         # Document ingestion + retrieval (Phase 5)
    models/      # SQLAlchemy ORM models (Phase 2)
    routes/      # FastAPI routers (Phase 8+)
    services/    # Business logic layer
    schemas/     # Pydantic request/response schemas
    prompts/     # System prompts / templates
    utils/       # Shared helpers
    config.py    # Settings (env-driven)
    database.py  # Async engine/session/Base
    logging_config.py
    main.py      # FastAPI app
  alembic/       # DB migrations
  tests/
  requirements.txt
  Dockerfile
  .env.example
frontend/
  app/
    dashboard/     # Admin dashboard routes (Phase 12)
    receptionist/  # Chat + booking UI (Phase 11)
    admin/         # Admin-only pages (Phase 12)
  components/
  hooks/
  services/
docker-compose.yml
```

## Running locally

**Option A — Docker (recommended):**

```bash
cp backend/.env.example backend/.env
docker compose up --build
```

Backend will be live at `http://localhost:8000`. Check:
- `GET http://localhost:8000/` → `{"message": "...", "status": "ok"}`
- `GET http://localhost:8000/health` → `{"status": "healthy", "env": "development"}`
- Interactive API docs: `http://localhost:8000/docs`

**Option B — Local Python (no Docker):**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Make sure Postgres is running locally and DATABASE_URL in .env points to it
uvicorn app.main:app --reload
```

**Run tests:**

```bash
cd backend
pytest
```

**Database migrations (Phase 2):**

```bash
cd backend
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

This creates all tables: `patients`, `appointments`, `conversations`, `messages`,
`doctors`, `clinic_settings`, `knowledge_documents`, `embeddings`, `users`,
and `notifications`.

## Notes on the frontend scaffold

The `frontend/` folder in this phase is structural only (Next.js 15 + TS +
Tailwind config, one placeholder page). Real screens land in Phases 11-12.
To run it as-is:

```bash
cd frontend
npm install
npm run dev
```
