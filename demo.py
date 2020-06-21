from kcu import kjson, strings
import string

from reddit_scraper.reddit_scraper import RedditScraper

posts = RedditScraper.get_posts('askreddit', max_count=10)

print(len(posts))

id_ = 'hckkcp'
post = RedditScraper.get_post(id_, comments_min_score=5000)

j = post.json
del j['post_dict']
del j['comments_dict']

kjson.save(id_ + '.json', j)