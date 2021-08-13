import os

import mongita
from fastapi import FastAPI
from typing import List
from dotenv import load_dotenv, find_dotenv
import praw
from starlette.middleware.cors import CORSMiddleware

from models import SubredditModel
from scraper.scanners.subreddits import SubredditsScraper

load_dotenv(find_dotenv())
app = FastAPI()

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


@app.get("/subreddits/default", response_description="Get the stats for the default subreddits",
         response_model=List[SubredditModel])
async def get_default_subreddits():
    client = mongita.MongitaClientDisk(host=os.getenv("MONGITA_HOST"))
    reddit_client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PW"),
    )
    sel_vars = ["_path", "display_name", "subscribers", "over18", "icon_img"]
    sub_parser = SubredditsScraper(reddit_client, mongo_client=client, default=True,
                                   name="default_subreddit_scraper", variables=sel_vars)

    default_subreddits = sub_parser.get_stored_data()
    return default_subreddits
