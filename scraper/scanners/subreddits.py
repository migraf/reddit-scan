import mongita
import praw
from pymongo import MongoClient
from typing import List, Tuple, Union
from praw import models
import os
from dotenv import load_dotenv, find_dotenv
from pprint import pprint
import pendulum

from scraper.logging import logger
from scraper.scanners.base import Scraper


class SubredditsScraper(Scraper):

    def __init__(self, reddit: praw.Reddit, subreddits: List[str] = None, name: str = None,
                 mongo_client: Union[MongoClient, mongita.MongitaClientDisk, mongita.MongitaClientMemory] = None,
                 store_results: bool = True, new: bool = False, default: bool = False,
                 popular: bool = False, variables: List[str] = None):

        super().__init__(reddit, name=name, mongo_client=mongo_client, store_results=store_results, variables=variables)

        self.popular = popular
        self.default = default
        self.new = new
        self.subreddits = subreddits

        if not (self.popular or self.default or self.new or self.subreddits):
            raise ValueError("No subreddits given to scrape.")

        self.subreddits_collection = self.db["default_subreddits"]

    def scrape(self):

        results = []
        if self.subreddits:
            results.extend(self._scrape_list_of_subreddits())
        if self.popular:
            results.extend(self._scrape_popular())
        if self.new:
            results.extend(self._scrape_new())
        if self.default:
            results.extend(self._scrape_default())

        if self.store_results:
            self.save_results(results)

    def save_results(self, results):
        super().save_results(results=results)
        # self.default_subreddits_collection.create_index({"display_name": 1}, {"unique": True})

        for subreddit_info in results:
            subreddit_document = self.subreddits_collection.find_one(
                {"display_name": subreddit_info["display_name"]})

            if subreddit_document:
                logger.info("Subrreddit {} already in collection.", subreddit_info["display_name"])
                subscriber_counts = subreddit_document.get("subscriber_counts", None)
                if subscriber_counts:
                    subscriber_counts.append(
                        {
                            "timestamp": pendulum.now().to_iso8601_string(),
                            "subscribers": subreddit_document["subscribers"]
                        }
                    )
                else:
                    subscriber_counts = [{
                        "timestamp": pendulum.now().to_iso8601_string(),
                        "subscribers": subreddit_document["subscribers"]
                    }]

                self.subreddits_collection.update_one(
                    {"display_name": subreddit_info["display_name"]},
                    {"$set": {"subscriber_counts": subscriber_counts}}
                )
            else:
                res = self.subreddits_collection.insert_one(subreddit_info)
                logger.info("Added subreddit {} \n at: {}", subreddit_info["display_name"], res)

    def get_subreddit_info(self, subreddit: praw.models.Subreddit) -> Tuple[dict, dict]:
        # Also init lazy loading
        logger.info("Getting subreddit info for {}", subreddit.display_name)
        all_vars = vars(subreddit)
        del all_vars["_reddit"]
        if self.variables:
            selected_vars = {var: all_vars[var] for var in self.variables}
            return all_vars, selected_vars

        return all_vars, {}

    def get_stored_data(self):
        logger.info("Getting stored subreddit data.")
        results = self.subreddits_collection.find({})
        print(len(list(results)))
        subreddits = []
        for subreddit in results:
            print(subreddit)
            subreddits.append(subreddit)
        return subreddits

    def _scrape_list_of_subreddits(self) -> List[dict]:
        pass

    def _scrape_popular(self, n: int = 1000) -> List[dict]:
        subreddits = self.reddit.subreddits.popular(limit=n)
        results = []
        for sub_r in subreddits:
            info, vars = self.get_subreddit_info(sub_r)
            results.append(info)
        return results

    def _scrape_new(self) -> List[dict]:
        pass

    def _scrape_default(self) -> List[dict]:
        subreddits = self.reddit.subreddits.default()
        results = []
        for sub_r in subreddits:
            info, vars = self.get_subreddit_info(sub_r)
            results.append(info)
        return results


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    mongita_client = mongita.MongitaClientDisk(host=os.getenv("MONGITA_HOST"))
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

    sub_parser = SubredditsScraper(reddit_client, mongo_client=mongita_client, default=True, popular=True,
                                   name="main_subreddit_scraper", variables=sel_vars, store_results=True)
    # sub_parser.scrape()
    pprint(sub_parser.get_stored_data())
