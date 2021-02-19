# reddit_scraper
![python_version](https://img.shields.io/static/v1?label=Python&message=3.5%20|%203.6%20|%203.7&color=blue) [![PyPI downloads/month](https://img.shields.io/pypi/dm/reddit_scraper?logo=pypi&logoColor=white)](https://pypi.python.org/pypi/reddit_scraper)

## Description


## Install
~~~~bash
pip install reddit_scraper
# or
pip3 install reddit_scraper
~~~~

## Usage
~~~~python
from kcu import kjson
from reddit_scraper.reddit_scraper import RedditScraper

# posts = RedditScraper.get_posts('askreddit', max_count=10)

# print(len(posts))

id_ = 'hyuiqg'
post = RedditScraper.get_post(id_, comments_min_score=250)

j = post.json
del j['post_dict']
del j['comments_dict']

kjson.save(id_ + '.json', j)
~~~~
##