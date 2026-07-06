# Docker AI Agent

A FastAPI backend that runs a multi-agent AI system (built with LangGraph + LangChain) behind a simple chat API, containerized with Docker Compose. The agents can read your Gmail inbox, draft emails, and send them on your behalf, using either **Docker Model Runner** (local models) or an OpenAI-compatible API.

> ⚠️ **Status:** the backend is deployed on [Railway](https://railway.com/), but the live deployment is currently down. Run it locally with Docker Compose in the meantime — see [Getting started](#getting-started). See also [Known Issues](#known-issues).

## How it works

```
Client
  │  POST /api/chats
  ▼
FastAPI (backend/src/main.py)
  │
  ▼
Supervisor agent (LangGraph)
  │
  ├── email_agent    → send_me_email, get_unread_emails
  └── research_agent → research_email (drafts email content via LLM)
```

- **`app`** — the FastAPI backend (`backend/`). Exposes a chat endpoint that hands off each message to a LangGraph **supervisor** agent, which routes work to two sub-agents:
  - **`email_agent`** — sends emails via SMTP and reads unread messages from a Gmail inbox via IMAP.
  - **`research_agent`** — uses an LLM to draft email subject/content for a given topic.
- **`db_service`** — a Postgres 15 container used to persist chat messages (via SQLModel).
- **`static_html`** — a minimal static file server (commented out in `compose.yaml` by default).
- The LLM is configured through `langchain-openai`'s `ChatOpenAI` client, pointed by default at **Docker Model Runner** (`http://model-runner.docker.internal/engines/v1/`), so it can run fully local models — or you can point it at OpenAI/any OpenAI-compatible endpoint.

## Project structure

```
backend/
  src/
    main.py                       # FastAPI app entrypoint
    api/
      db.py                       # SQLModel engine / session setup
      chat/
        routing.py                # POST /api/chats -> invokes the supervisor agent
        models.py                 # ChatMessage SQLModel table
      ai/
        llm.py                    # ChatOpenAI client factory (model/base_url/key from env)
        agents.py                 # Supervisor + email_agent + research_agent (LangGraph)
        tools.py                  # LangChain tools: send_me_email, get_unread_emails, research_email
        services.py               # generate_email() - structured LLM output
        schemas.py                # Pydantic response schemas
        myemailer/
          sender.py               # SMTP email sending
          inbox_reader.py         # IMAP inbox reading
          gmail_imap_parser.py    # Gmail IMAP parsing helper
  Dockerfile
  requirements.txt
  railway.json                    # Railway.com deployment config
static_html/
  src/index.html, abc.html        # placeholder static site
  Dockerfile
compose.yaml                      # app + db_service (+ optional static_html)
.env.sample                       # example environment variables
.devcontainer/                    # VS Code Dev Containers config
```

## What this project covers

This was built as a hands-on learning project to go from Docker fundamentals to deploying a multi-agent AI system. Topics covered:

**Docker & containerization**
- Docker fundamentals and writing a custom `Dockerfile`
- Building custom Docker images and pushing to Docker Hub
- Using Docker Compose to orchestrate multiple services
- Docker Compose Watch mode for live-reload development
- Serving static HTML through Docker
- Using public open-source containers (Postgres, Redis, etc.)
- `.dockerignore` and why it matters
- Mounting and persisting data with volumes
- Injecting runtime environment variables with env files

**Backend & API**
- "Hello World" with Docker and FastAPI
- Nesting API routes in FastAPI
- Integrating Postgres with FastAPI through Docker
- Running open-source LLMs locally via Docker Model Runner (Docker Desktop)
- Testing production-level API calls across Docker, FastAPI, OpenAI, and LangGraph

**AI agents**
- Integrating LangChain with FastAPI
- Defining and manually invoking tools with LangChain-based models
- Using LangGraph to let an agent select and run tools automatically
- Building a multi-agent system with a LangGraph supervisor
- Sending email through Gmail and Python's standard library
- Reading a Gmail inbox with Python

**Deployment**
- Deploying a Dockerfile-based app to Railway
- Deploying the same Dockerfile-based app to DigitalOcean



- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose) or Docker Engine + Compose plugin
- Docker Model Runner enabled in Docker Desktop, **or** an OpenAI API key if you'd rather use a hosted model
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) if you want to use the email-reading/sending tools

## Getting started

1. **Clone the repo**

   ```bash
   git clone https://github.com/monisakhtar/docker-ai-agent.git
   cd docker-ai-agent
   ```

2. **Configure environment variables**

   Copy the sample file and fill in your own values:

   ```bash
   cp .env.sample .env
   ```

   | Variable | Description | Default in `.env.sample` |
   |---|---|---|
   | `API_KEY` | Placeholder app API key (not currently enforced anywhere in the code) | `abc123` |
   | `DATABASE_URL` | Postgres connection string | `postgresql+psycopg://postgres:password@db_service:5432/postgres` |
   | `OPENAI_BASE_URL` | Base URL for the OpenAI-compatible LLM endpoint | Docker Model Runner (`http://model-runner.docker.internal/engines/v1/`) |
   | `OPENAI_API_KEY` | API key for the LLM endpoint. **Required** — the app raises an error at import time if this is unset | *(empty)* |
   | `OPENAI_MODEL` | Model name/tag to use | `ai/gemma3:270M-F16` |
   | `EMAIL_ADDRESS` | Gmail address used to send/read mail | *(empty)* |
   | `EMAIL_PASSWORD` | Gmail App Password (not your normal password) | *(empty)* |
   | `EMAIL_HOST` | SMTP host | `smtp.gmail.com` |
   | `EMAIL_PORT` | SMTP port | `465` |

   > `compose.yaml` currently loads env vars from `.env.sample` directly via `env_file`. For real use, either edit `.env.sample` in place or update `compose.yaml` to point at your own `.env` file.

3. **Run with Docker Compose**

   ```bash
   docker compose up --build
   ```

   This starts:
   - `app` — FastAPI backend at [http://localhost:8080](http://localhost:8080) (container port `8000`, mapped to host `8080`)
   - `db_service` — Postgres at `localhost:5432`

   Compose Watch is configured, so editing files under `backend/src` restarts the app, and changes to `requirements.txt` or the `Dockerfile` trigger a rebuild.

4. **Try the API**

   ```bash
   # Health check
   curl http://localhost:8080/

   # Chat root
   curl http://localhost:8080/api/chats/

   # Send a message to the agent supervisor
   curl -X POST http://localhost:8080/api/chats/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Summarize my unread emails from the last 24 hours"}'
   ```

   Interactive API docs are available at [http://localhost:8080/docs](http://localhost:8080/docs) (FastAPI's built-in Swagger UI).

## API reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Basic health check |
| `GET` | `/api/chats/` | Chat API welcome message |
| `GET` | `/api/chats/recent` | Returns up to 10 stored chat messages |
| `POST` | `/api/chats/` | Sends a message to the supervisor agent, persists it, and returns the agent's final reply |

## Using the static site (optional)

`static_html` is defined but commented out in `compose.yaml`. To enable it, uncomment its block and adjust the port mapping so it doesn't collide with `app` (both default to host access via `8000`/`8080`), then run `docker compose up` again.

## Known issues

This is an evolving personal project — a few things to be aware of before using it as-is:

- `backend/src/api/chat/routing.py` references a `thread_id` variable in the `POST /api/chats/` handler that is never defined, so this endpoint currently raises a `NameError`.
- `OPENAI_API_KEY` must be set even when using Docker Model Runner locally — the code path in `llm.py` raises a `ValueError` if it's empty. Set it to any non-empty placeholder value if you're not calling a real OpenAI endpoint.
- Credentials in `.env.sample` (including a real-looking Gmail address) are placeholders meant to be replaced — don't commit real secrets to this file.
- `db_service`'s Postgres password is hardcoded in `compose.yaml` for local development only; don't reuse this setup as-is for anything internet-facing.

## Deployment

The backend is deployed to [Railway](https://railway.com/) using the included `backend/railway.json`, which points Railway at the backend `Dockerfile` and sets the start command to:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**The live Railway deployment is currently down.** If you hit a dead URL, that's why — use the local Docker Compose setup above instead. To redeploy:

1. Connect this repo to a Railway project (or run `railway up` from the repo root with the Railway CLI).
2. Set the environment variables from the [Configure environment variables](#getting-started) table in the Railway project's variables tab (Railway won't read `.env.sample` automatically).
3. Provision a Postgres instance on Railway (or point `DATABASE_URL` at an external one) — the bundled `db_service` container is for local Compose use only.
4. Trigger a redeploy from the Railway dashboard.

## License

No license file is currently included in this repository. Add one (e.g. MIT, Apache-2.0) if you intend for others to reuse this code.
