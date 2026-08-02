# FirstNews News Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![React](https://img.shields.io/badge/React-Frontend-61dafb)
![Vite](https://img.shields.io/badge/Vite-Build-646cff)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479a1)
![Redis](https://img.shields.io/badge/Redis-Cache-dc382d)

FirstNews is a news information web project that provides news categories, news lists, news details, user authentication, favorites, browsing history, Redis cache, and AI Q&A.

## Introduction

News applications usually need to handle content display, user state, favorite records, browsing history, and API performance at the same time. FirstNews combines a React frontend, FastAPI backend, MySQL data storage, and Redis cache in one development project. It is suitable for learning and verifying a complete web application flow.

The project is designed for local development and practice. It is suitable for learning FastAPI, SQLAlchemy Async ORM, React, Vite, Redis cache, third-party news API integration, and backend AI API proxy calls.

## Core Capabilities

- News Browsing: Supports news categories, paginated lists, news details, and third-party news display.
- User System: Supports registration, login, token authentication, user information retrieval, and profile updates.
- Favorites: Supports checking favorite status, adding favorites, removing favorites, favorite lists, and clearing favorites.
- Browsing History: Supports recording news browsing, history lists, deleting a single record, and clearing history.
- Cache and AI: Uses Redis to cache category/list data and calls the Gemini API through a backend proxy.

## Quick Start

### Prerequisites

The local environment needs:

- Python 3.13
- Node.js and npm
- MySQL, with the default database name `news_app`
- Redis, with the default address `localhost:6379`
- Gemini API key, only required when using AI Q&A

### Backend

```bash
cd /Users/yuqian_chen/PycharmProjects/FirstNews
source .venv/bin/activate
export GEMINI_API_KEY="your-gemini-api-key"
uvicorn main:app --reload
```

Default backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

If AI Q&A is not used, `GEMINI_API_KEY` does not need to be set. Other business APIs can still run.

### Frontend

```bash
cd /Users/yuqian_chen/PycharmProjects/FirstNews/frontend
npm install
npm run dev
```

Default frontend URL:

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
├── frontend/                      # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx                # React page and state logic
│   │   ├── main.jsx               # React application entry
│   │   ├── style.css              # Frontend styles
│   │   ├── config/                # Frontend API config
│   │   └── assets/                # Frontend images
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
| Home | `/` or `/home` | News categories, three-image carousel, third-party news list, and paginated loading |
| News Detail | `/news/detail/:id` | News content, source, favorite entry, and original article link |
| Profile Home | `/my` | User entry, favorites, history, profile, and settings |
| Favorites | `/favorite` | Current user's favorite list |
| History | `/history` | Current user's news browsing history |
| AI Chat | `/aichat` | Calls Gemini through a backend proxy |
| Login/Register | `/login`, `/register` | User login and registration |

### Backend APIs

| Module | Path | Capability |
|---|---|---|
| News | `/api/news/categories` | Gets news categories and supports Redis cache |
| News | `/api/news/list` | Gets paginated database news list |
| News | `/api/news/detail` | Gets news details and increases views |
| User | `/api/user/register` | User registration |
| User | `/api/user/login` | User login and token generation |
| User | `/api/user/info` | Gets current user information |
| Favorite | `/api/favorite/*` | Favorite check, add, delete, list, and clear |
| History | `/api/history/*` | Add browsing record, list, delete, and clear |
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

- React: Page and interaction development
- React DOM: Browser rendering
- Vite: Frontend development server and build tool
- Fetch API: HTTP requests
- CSS: Responsive web page styling
- LocalStorage: Fallback storage for third-party news details, local favorites, and local browsing history

## Data Sources / Design Principles

Project data mainly comes from the local MySQL database. The core tables include users, user tokens, news categories, news, favorites, and browsing history. Redis is used to cache read-heavy and write-light data, reducing repeated database queries.

The frontend news list first requests the third-party NewsAPI. If the third-party API is unavailable or returns an empty list, it falls back to the backend database news API. If the backend is also unavailable, mock data is used to keep the page displayable.

The project is layered by responsibility:

```text
routers/  Receives HTTP requests and handles parameters and response formats
crud/     Encapsulates database and cache reads/writes
models/   Defines database ORM table structures
schemas/  Defines Pydantic data models
utils/    Places common logic such as authentication, response, and security
frontend/ Calls backend APIs and displays React pages
```

AI Q&A uses a backend proxy mode:

```text
Frontend -> FastAPI /api/ai/chat -> Gemini API
```

This approach can avoid browser CORS restrictions and reduce the risk of exposing the API key in frontend build artifacts.

## Benchmarks

The current project does not configure automated test benchmarks. The following checks are recommended for local verification:

| Check | Method |
|---|---|
| Backend Import Check | `python -m compileall main.py routers crud models schemas utils config cache` |
| Frontend Build Check | `npm run build` |
| Redis Connectivity | `redis-cli ping` returns `PONG` |
| MySQL Connectivity | Visit `/docs` and then call any database API |
| Cache Hit | Continuously visit `/api/news/categories` and observe the `Redis cache hit` log |
| AI Proxy | Set `GEMINI_API_KEY` and then call `/api/ai/chat` |

