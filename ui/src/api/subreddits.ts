import type {SubredditList} from "../models/subreddit";

export async function getDefaultSubreddits(): Promise<SubredditList> {
    return fetch("http://localhost:8000/subreddits/default")
        .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText)
                }
                let jsonResponse = response.json();
                console.log(jsonResponse);
                return jsonResponse
            }
        )
}
