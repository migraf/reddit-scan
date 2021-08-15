import mongita
import praw
import os
import pymongo


def reddit_client():
    reddit_client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PW"),
    )
    return reddit_client


def mongita_client():
    client = mongita.MongitaClientDisk(host=os.getenv("MONGITA_HOST"))
    return client


def mongo_client():
    client = pymongo.MongoClient(
        username=os.getenv("MONGODB_USER"),
        password=os.getenv("MONGODB_PW")
    )
    return client
