# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Tuple, Optional
import traceback

# Pip
from kcu import request

# Local
from .models.time_interval import TimeInterval
from .models.sorting_type import SortingType
from .models.post import Post
from .models.comment import Comment
from .models.image import Image
from .models.video import Video
from .models.post_type import PostType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: RedditScraper --------------------------------------------------------- #

class RedditScraper:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def get_posts(
        cls,
        sub: str,
        time_interval: Optional[TimeInterval] = TimeInterval.DAY,
        sorting_type: Optional[SortingType] = SortingType.TOP,
        ignored_post_ids: List[str] = [],
        min_score: int = 50,
        max_count: int = 50,
        ignored_flairs: List[str] = [],
        include_nsfw: bool = False,
        post_types: List[PostType] = [PostType.TitleOnly, PostType.Text, PostType.Image, PostType.Video],
        include_pinned: bool = False,
        min_upvote_ratio: float = 0.75,
        min_ts: int = 0,
        fake_useragent: bool = True
    ) -> List[Post]:
        posts = []
        after = None

        while True:
            new_posts, after = cls.__get_posts(sub, time_interval, sorting_type, after, fake_useragent=fake_useragent)

            if new_posts is None:
                return posts

            for post in cls.__filtered_posts(
                posts=new_posts,
                ignored_post_ids=ignored_post_ids or [],
                min_score=min_score,
                ignored_flairs=ignored_flairs or [],
                include_nsfw=include_nsfw,
                post_types=post_types,
                include_pinned=include_pinned,
                min_upvote_ratio=min_upvote_ratio,
                min_ts=min_ts
            ):
                posts.append(post)

                if len(posts) >= max_count:
                    return posts

            if (
                (after is None)
                or
                (sorting_type == SortingType.TOP and (len(new_posts) > 0 and new_posts[-1].score < min_score))
                or
                (sorting_type == SortingType.NEW and (len(new_posts) > 0 and new_posts[-1].ts < min_ts))
            ):
                return posts

    @classmethod
    def get_post(
        cls,
        post_id: str,
        sorting_type: SortingType = SortingType.TOP,
        comments_min_score: int = 50,
        comments_include_stickied: bool = False,
        comments_min_ts: int = 0,
        fake_useragent: bool = True
    ) -> Optional[Post]:
        url = cls.__post_url(post_id, sorting_type)

        try:
            import json

            j = json.loads(request.get(url, debug=True, fake_useragent=fake_useragent).text)

            post = Post(j[0]['data']['children'][0]['data'], j[1]['data']['children'])
            post.comments = cls.__filtered_comments(post.comments, comments_min_score, comments_include_stickied, comments_min_ts)

            return post
        except:
            traceback.print_exc()

            return None


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @classmethod
    def __get_posts(
        cls,
        sub: str,
        time_interval: Optional[TimeInterval],
        sorting_type: Optional[SortingType],
        after: Optional[str],
        fake_useragent: bool
    ) -> Tuple[Optional[List[Post]], Optional[str]]:
        url = cls.__sub_url(sub, time_interval, sorting_type, after)

        try:
            import json

            j = json.loads(request.get(url, fake_useragent=fake_useragent).text)

            return [Post(post_json['data']) for post_json in j['data']['children']], j['data']['after']
        except:
            traceback.print_exc()

            return None, None

    @classmethod
    def __filtered_comments(
        cls,
        comments: List[Comment],
        min_score: int,
        include_stickied: bool,
        mit_ts: int
    ) -> List[Comment]:
        filtered = []

        for comment in comments:
            if comment.score < min_score:
                continue

            if comment.stickied and not include_stickied:
                continue

            if comment.ts < mit_ts:
                continue

            comment.comments = cls.__filtered_comments(comment.comments, min_score, include_stickied, mit_ts)
            filtered.append(comment)

        return filtered

    @staticmethod
    def __filtered_posts(
        posts: List[Post],
        ignored_post_ids: List[str],
        min_score: int,
        ignored_flairs: List[str],
        include_nsfw: bool,
        post_types: List[PostType],
        include_pinned: bool,
        min_upvote_ratio: float,
        min_ts: int
    ) -> List[Post]:
        filtered = []

        for post in posts:
            if post.id in ignored_post_ids:
                # print('post.id in ignored_post_ids', post.id)
                continue

            if post.score < min_score:
                # print('post.score < min_score', post.score, min_score)
                continue

            if post.nsfw and not include_nsfw:
                # print('post.nsfw', post.nsfw)
                continue

            if post.type not in post_types:
                # print('post.type', post.type)
                continue

            if post.pinned and not include_pinned:
                # print('post.pinned', post.pinned)
                continue

            if post.upvote_ratio < min_upvote_ratio:
                # print('post.upvote_ratio < min_upvote_ratio', post.upvote_ratio, min_upvote_ratio)
                continue

            if post.ts < min_ts:
                # print('post.ts < min_ts', post.ts, min_ts)
                continue

            if post.flair_text is not None:
                flair_text = post.flair_text.lower()
                should_continue = False

                for flair in ignored_flairs:
                    if flair.lower() in flair_text:
                        should_continue = True
                        # print('has ignored flair:', flair.lower())

                        break

                if should_continue:
                    continue

            filtered.append(post)

        return filtered

    @staticmethod
    def __sub_url(
        sub: str,
        time_interval: Optional[TimeInterval],
        sorting_type: Optional[SortingType],
        after: Optional[str]
    ) -> str:
        url = 'https://www.reddit.com/r/' + sub

        if sorting_type is not None:
            url += '/' + sorting_type.value

        url += '.json'

        if sorting_type == SortingType.TOP:
            url += '?t=' + time_interval.value

            if after is not None:
                url += '&after=' + after
        elif after is not None:
            url += '?after=' + after

        return url

    @staticmethod
    def __post_url(post_id: str, sorting_type: SortingType) -> str:
        return 'https://www.reddit.com/comments/' + post_id + '.json?sort=' + sorting_type.value


# ---------------------------------------------------------------------------------------------------------------------------------------- #