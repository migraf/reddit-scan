from typing import List

import praw
import uuid
from pymongo import MongoClient


class Scraper:
    def __init__(self, reddit: praw.Reddit, name: str = None, mongo_client: MongoClient = None,
                 store_results: bool = True, variables: List[str] = None):
        self.reddit = reddit
        self.mongo_client = mongo_client
        self.variables = variables
        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())
        self.store_results = store_results

        # TODO maybe initialize connection lazily
        if mongo_client:
            self.db = mongo_client[self.name]

    def scrape(self):
        pass

    def save_results(self, results):
        pass
