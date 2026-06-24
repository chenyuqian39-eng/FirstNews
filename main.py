from fastapi import FastAPI
from routers import news, users
from fastapi.middleware.cors import CORSMiddleware
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