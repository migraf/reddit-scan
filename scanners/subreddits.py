import praw
from pymongo import MongoClient

from .base import Scraper
from typing import List, Tuple, Union
from praw import models
import os
from dotenv import load_dotenv, find_dotenv
import pprint


class SubredditsScraper(Scraper):

    def __init__(self, reddit: praw.Reddit, subreddits: List[str] = None, name: str = None,
                 mongo_client: MongoClient = None, store_results: bool = True, new: bool = False, default: bool = False,
                 popular: bool = False, variables: List[str] = None):

        super().__init__(reddit, name=name, mongo_client=mongo_client, store_results=store_results, variables=variables)

        self.popular = popular
        self.default = default
        self.new = new
        self.subreddits = subreddits

        if not (self.popular or self.default or self.new or self.subreddits):
            raise ValueError("No subreddits given to scrape.")

        self.subreddits_collection = self.db["subreddits"]

    def scrape(self):
        if self.subreddits:
            results = self._scrape_list_of_subreddits()

        if self.popular:
            results = self._scrape_popular()

        if self.new:
            results = self._scrape_new()

        if self.default:
            results = self._scrape_default()

        if self.store_results:
            self.save_results(results)

    def save_results(self, results):
        super().save_results(results=results)
        res = self.subreddits_collection.insert_many(results)
        self.subreddits_collection.create_index("display_name")

    def get_subreddit_info(self, subreddit: praw.models.Subreddit) -> Union[Tuple[dict, dict], dict]:
        # Also init lazy loading
        print("Getting subreddit info for: ", subreddit.display_name)
        all_vars = vars(subreddit)
        del all_vars["_reddit"]
        if self.variables:
            selected_vars = {var: all_vars[var] for var in self.variables}
            return all_vars, selected_vars

        return all_vars

    def get_stored_data(self):
        results = self.subreddits_collection.find({})
        subreddits = []
        for subreddit in results:
            subreddits.append(subreddit)
        return subreddits

    def _scrape_list_of_subreddits(self) -> List[dict]:
        pass

    def _scrape_popular(self) -> List[dict]:
        pass

    def _scrape_new(self) -> List[dict]:
        pass

    def _scrape_default(self) -> List[dict]:
        subreddits = self.reddit.subreddits.default()
        results = []
        for sub_r in subreddits:
            info, vars = self.get_subreddit_info(sub_r)
            print(info)
            results.append(info)
        return results


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    mongo_client = MongoClient(username="admin", password="admin")
    reddit_client = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PW"),
    )
    # db = mongo_client["default_subreddit_scraper"]
    # coll = db["subreddits"]
    # coll.drop()
    sel_vars = ["_path", "display_name", "subscribers", "over18", "icon_img"]

    sub_parser = SubredditsScraper(reddit_client, mongo_client=mongo_client, default=True,
                                   name="default_subreddit_scraper", variables=sel_vars)
    # sub_parser.scrape()
    sub_parser.get_stored_data()