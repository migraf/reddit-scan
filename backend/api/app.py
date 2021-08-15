from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
from starlette.middleware.cors import CORSMiddleware

from backend.api.routers.subreddits import router as subreddits_router


load_dotenv(find_dotenv())
app = FastAPI()


app.include_router(subreddits_router, prefix="/subreddits", tags=["Subreddits"])


origins = [
    "*",
    "http://localhost",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

