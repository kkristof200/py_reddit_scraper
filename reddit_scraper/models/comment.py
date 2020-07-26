# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict

# Pip
from jsoncodable import JSONCodable

# Local
from .common_utils import clean_text

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Comment ------------------------------------------------------------ #

class Comment(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        json: Dict
    ):
        self.id             = json['id']
        self.author         = json['author']
        self.ts             = json['created_utc']
        self.score          = json['score']
        self.content        = clean_text(json['body'])
        self.stickied       = json['stickied']
        self.distinguished  = json['distinguished']
        self.depth          = json['depth']
        self.sub            = json['subreddit']

        self.comments = []

        try:
            for child in json['replies']['data']['children']:
                try:
                    self.comments.append(Comment(child['data']))
                except:
                    pass
        except:
            pass


# ---------------------------------------------------------------------------------------------------------------------------------------- #