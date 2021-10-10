
import requests
import re
from bs4 import BeautifulSoup
import json
import feedparser
from wordcloud import WordCloud, STOPWORDS
import os

# https://blog.feedspot.com/usa_news_rss_feeds/

f = open('feedlist.json',)

if not os.path.exists("out"):
    os.makedirs("out")
    
feedlist = json.load(f)

for feed in feedlist:
    NewsFeed = None
    try:
        response_code = requests.get(feedlist[feed],timeout=3)
        NewsFeed = feedparser.parse(feedlist[feed])
    except Exception as e:
        print(e)
    
    comment_words = ''
    stopwords = set(STOPWORDS)
    try:
        for item in NewsFeed.entries:
            try:
                title = re.sub(r'[^a-zA-Z0-9]', ' ', item["title"])
                tokens = title.split()

                # Converts each token into lowercase
                for i in range(len(tokens)):
                    tokens[i] = tokens[i].lower()
                    if len(tokens[i]) < 2:
                        tokens.remove(tokens[i])

                comment_words += " ".join(tokens)+" "
            except:
                pass

        try:
            print(feed,response_code)
            print(comment_words)
            print("\n")
        except:
            pass

        try:
            wordcloud = WordCloud(width=800, height=800,
                                background_color='white',
                                stopwords=stopwords,
                                min_font_size=10,max_words=5000).generate(comment_words)
            wordcloud.to_file(f'out/{feed}.png')
        except:
            pass
    except:
        pass
