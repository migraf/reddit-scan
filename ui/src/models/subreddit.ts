
export interface Subreddit {
    _id: string;
    display_name: string;
    subscribers: number;
    public_description: string;
    icon_img: string;
    "over18": boolean;
}

export interface SubredditList {
    created?: string;
    subreddits: Array<Subreddit>;
}

