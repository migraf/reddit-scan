<script lang="ts">
    import type {Subreddit, SubredditList} from "../models/subreddit";
    import {onMount} from "svelte";
    import {getDefaultSubreddits} from "../api/subreddits";

    let subredditList: Promise<SubredditList>;



    export let name: string;

    onMount(() => {
        fetchSubreddits();
    })

    async function fetchSubreddits() {
        subredditList = getDefaultSubreddits();
        subredditList.then(

        )

    }


</script>

<main>
    <h1>Hello {name}!</h1>
    <p>Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn how to build Svelte apps.</p>
    {#await subredditList}
        <p>...waiting</p>
    {:then data}

        <p>{typeof data}</p>
        <p> {data}</p>

        <!--        <ul>-->
        <!--            {#each data.subreddits as subreddit}-->
        <!--                <p>{subreddit.display_name}</p>-->
        <!--            {/each}-->
        <!--        </ul>-->


        <!--        <ul>-->
        <!--            {#each subreddits as subreddit}-->
        <!--                <li>-->
        <!--                    {subreddit.display_name}-->
        <!--                </li>-->
        <!--            {/each}-->
        <!--        </ul>-->
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>
