# FirstNews News Information System (FirstNews News Platform)

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Vue](https://img.shields.io/badge/Vue-3-42b883)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479a1)
![Redis](https://img.shields.io/badge/Redis-Cache-dc382d)


FirstNews is a news information project that provides news categories, news lists, detail pages, user authentication, favorites, browsing history, Redis cache, and AI Q&A capabilities.

## Introduction

News applications usually need to handle content display, user status, favorite records, browsing history, and API performance at the same time. FirstNews combines frontend mobile pages, FastAPI backend APIs, MySQL data storage, and Redis cache in one development project, making it convenient to learn and verify a complete Web application flow.

The project is currently aimed at the local development environment and is suitable for comprehensive practice with FastAPI, SQLAlchemy ORM, Vue 3, Pinia, Vant, Redis cache, and third-party AI API proxy calls.

## Core Capabilities

- 📰 News Browsing: Supports news categories, paginated lists, news details, and related news.
- 👤 User System: Supports registration, login, Token authentication, user information retrieval, and profile updates.
- ⭐ Favorites: Supports checking favorite status, adding favorites, removing favorites, favorite list, and clearing favorites.
- 🕘 Browsing History: Supports recording news browsing, history list, deleting a single record, and clearing history.
- ⚡ Cache and AI: Uses Redis to cache category/list data and calls the Gemini API through a backend proxy.

## Quick Start

### Prerequisites

The local machine needs to have:

- Python 3.13
- Node.js and npm
- MySQL, the default database name of this project is `news_app`
- Redis, the default address is `localhost:6379`
- Gemini API key, only needed when using AI Q&A

### Backend

```bash
cd /Users/yuqian_chen/PycharmProjects/FirstNews
source .venv/bin/activate
export GEMINI_API_KEY="your-gemini-api-key"
uvicorn main:app --reload
```

Default backend address:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

If AI Q&A is not used, `GEMINI_API_KEY` does not need to be set, and other business APIs can still run.

### Frontend

```bash
cd /Users/yuqian_chen/PycharmProjects/FirstNews/frontend
npm install
npm run dev
```

Default frontend address:

```text
http://127.0.0.1:5173
```

## Project Structure

```text
FirstNews/
├── cache/                         # Redis cache helpers
│   └── news_cache.py
├── config/                        # Backend configuration
│   ├── cache_conf.py              # Redis connection and cache helpers
│   └── db_conf.py                 # MySQL async SQLAlchemy configuration
├── crud/                          # Database and cache access layer
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   ├── news_cache.py
│   └── users.py
├── frontend/                      # Vue 3 frontend
│   ├── src/
│   │   ├── components/            # Shared UI components
│   │   ├── config/                # Frontend API config
│   │   ├── router/                # Vue Router config
│   │   ├── store/                 # Pinia stores
│   │   └── views/                 # Page views
│   ├── package.json
│   └── vite.config.js
├── models/                        # SQLAlchemy ORM models
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
├── routers/                       # FastAPI routers
│   ├── ai.py
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
├── schemas/                       # Pydantic request/response schemas
├── utils/                         # Auth, response, security helpers
├── main.py                        # FastAPI application entry point
├── test_main.http                 # HTTP request examples
└── README.md
```

## Usage Guide

### Common Pages

| Page | Route | Description |
|---|---|---|
| Home | `/` | Category news list and pull-down loading |
| News Detail | `/news/detail/:id` | News content, views, related news, and favorite entry |
| Profile Home | `/my` | User entry, favorites, history, settings |
| Favorites | `/favorite` | Current user's favorite list |
| History | `/history` | Current user's news browsing history |
| AI Chat | `/aichat` | Calls Gemini through a backend proxy |

### Backend APIs

| Module | Path | Capability |
|---|---|---|
| News | `/api/news/categories` | Gets news categories, supports Redis cache |
| News | `/api/news/list` | Gets paginated category news list |
| News | `/api/news/detail` | Gets news details and increases views |
| User | `/api/user/register` | User registration |
| User | `/api/user/login` | User login and Token generation |
| User | `/api/user/info` | Gets current user information |
| Favorite | `/api/favorite/*` | Favorite check, add, delete, list, clear |
| History | `/api/history/*` | Add browsing record, list, delete, clear |
| AI | `/api/ai/chat` | Backend proxy call to Gemini API |

### Redis Cache Keys

| Key | Data | Description |
|---|---|---|
| `news:categories` | News category list | Category data is relatively stable and has a longer cache time |
| `news_list:{categoryId}:{page}:{pageSize}` | News paginated list | Category, page number, and page size together determine cache uniqueness |

## Tech Stack

### Backend

- FastAPI: API routing and request handling
- SQLAlchemy Async ORM: MySQL asynchronous ORM queries
- aiomysql / PyMySQL: MySQL asynchronous connection
- Pydantic: Request parameters and response data structures
- Redis Async: Category and news list cache
- bcrypt: Password hashing
- Uvicorn: ASGI development server

### Frontend

- Vue 3: Page and component development
- Vite: Frontend build tool
- Vue Router: Frontend routing
- Pinia: State management
- Vant: Mobile UI components
- Axios / Fetch: HTTP requests
- Marked + DOMPurify: AI message Markdown rendering and HTML cleaning

## Data Sources / Design Principles

Project data mainly comes from the local MySQL database. The core tables include users, user Tokens, news categories, news, favorites, and browsing history. Redis is used to cache read-heavy and write-light data, reducing the frequency of repeated database queries.

The design is layered by responsibility:

```text
routers/  Receives HTTP requests and handles parameters and response formats
crud/     Encapsulates database and cache reads/writes
models/   Defines database ORM table structures
schemas/  Defines Pydantic data models
utils/    Places common logic such as authentication, response, and security
frontend/ Calls backend APIs and displays pages
```

AI Q&A uses a backend proxy mode:

```text
Frontend -> FastAPI /api/ai/chat -> Gemini API
```

This can avoid browser CORS restrictions and avoid exposing the API key in frontend build artifacts.

## Benchmarks

The current project does not configure automated test benchmarks. It is recommended to use the following standards for local checks:

| Check | Method |
|---|---|
| Backend Import Check | `python -m compileall main.py routers crud models schemas utils config cache` |
| Frontend Build Check | `npm run build` |
| Redis Connectivity | `redis-cli ping` returns `PONG` |
| MySQL Connectivity | Visit `/docs` and then call any database API |
| Cache Hit | Continuously visit `/api/news/categories` and observe the `Redis cache hit` log |
| AI Proxy | Set `GEMINI_API_KEY` and then call `/api/ai/chat` |
