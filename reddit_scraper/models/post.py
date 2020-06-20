# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict, List, Optional

# Pip
from jsoncodable import JSONCodable

# Local
from .comment import Comment

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Post -------------------------------------------------------------- #

class Post(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        post_json: Dict,
        comments_json: Optional[List[Dict]] = None
    ):
        self.sub            = post_json['subreddit']
        self.title          = post_json['title']
        self.content        = post_json['selftext']
        self.nsfw           = post_json['over_18']
        self.pinned         = post_json['pinned']
        self.id             = post_json['id']
        self.score          = post_json['score']
        self.upvote_ratio   = post_json['upvote_ratio']
        self.flair_text     = post_json['link_flair_text']
        self.url            = post_json['url'].strip('/')
        self.ts             = int(post_json['created_utc'])
        self.author         = post_json['author']
        self.distinguished  = post_json['distinguished']

        self.post_dict      = post_json
        self.comments_dict  = comments_json

        self.comments = []

        if comments_json is None:
            return

        for comment_json in comments_json:
            try:
                self.comments.append(Comment(comment_json['data']))
            except Exception as e:
                print('comment_e', e)

                pass


# ---------------------------------------------------------------------------------------------------------------------------------------- #