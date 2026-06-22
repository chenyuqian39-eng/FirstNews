# FirstNews

## Project Structure
FirstNews_backend/
├── crud/                              # Database CRUD operations
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
│
├── models/                            # Data model definitions
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
│
├── routers/                           # API routing layer, organized by module
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
│
├── schemas/                           # Pydantic schemas for data validation
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── users.py
│
├── utils/                             # Utility functions
│
├── config/                            # Configuration files
│   ├── db_conf.py                     # Database configuration
│   ├── cache_conf.py                  # Redis cache configuration
│
├── main.py                            # Application entry point
└── test_main.http                     # HTTP API test file

## Run Project
1. Terminal 1 (back end)
```bash
cd /Users/yuqian_chen/PycharmProjects/FirstNews
source .venv/bin/activate
uvicorn main:app --reload
```
If success, will show:
Uvicorn running on http://127.0.0.1:8000

2. Terminal 2( front end)
   (install dependence:
npm install
npm run dev
   )
``` bash
cd /Users/yuqian_chen/PycharmProjects/FirstNews/frontend
npm run dev
```
open: http://127.0.0.1:5173/
