from typing import List

from fastapi import APIRouter, Depends
from praw import Reddit
from pymongo import MongoClient

from scraper.scanners import SubredditsScraper
from ..dependencies import reddit_client, mongo_client, mongita_client
from ..schemas import Subreddit

router = APIRouter()


@router.get("/default", response_description="Get the default subreddits", response_model=List[Subreddit])
async def get_default_subreddits(reddit: Reddit = Depends(reddit_client),
                                 mongo: MongoClient = Depends(mongo_client)):
    sub_parser = SubredditsScraper(reddit, mongo_client=mongo, default=True,
                                   name="main_subreddit_scraper")
    default_subreddits = sub_parser.get_stored_data()
    return default_subreddits


@router.get("/popular", response_description="Get the popular subreddits", response_model=List[Subreddit])
async def get_popular_subreddits(reddit: Reddit = Depends(reddit_client),
                                 mongo: MongoClient = Depends(mongo_client)):
    pass


@router.get("/new", response_description="Get the newest subreddits", response_model=List[Subreddit])
async def get_new_subreddits(limit: int = 100, reddit: Reddit = Depends(reddit_client),
                             mongo: MongoClient = Depends(mongo_client)):
    pass


@router.get("/{subreddit_name}/details", response_description="All stored information about the given subreddit")
async def get_subreddit_details(subreddit_name: str, reddit: Reddit = Depends(reddit_client),
                                mongo: MongoClient = Depends(mongo_client)):
    pass
