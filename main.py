import logging

from fastapi import FastAPI
from routers import ai, news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Allowed origins. Allow all origins in development; specify origins in production
    allow_credentials=True, #Allow cookies
    allow_methods=["*"],#Allowed request methods
    allow_headers=["*"],#Allowed request headers
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#attach router/register router
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
app.include_router(ai.router)
