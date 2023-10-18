from kcu import kjson
from reddit_scraper.reddit_scraper import RedditScraper
import json

sub = 'soccer'

posts = RedditScraper.get_posts(sub, max_count=10, fake_useragent=True)

print(len(posts))
kjson.save(sub + '.json', [post.json for post in posts])

# id_ = 'hyuiqg'
# post = RedditScraper.get_post(id_, comments_min_score=250)

# j = post.json
# del j['post_dict']
# del j['comments_dict']

# kjson.save(id_ + '.json', j)