import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}
"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

sub_reddits = [
    "javascript", "reactjs", "reactnative", "programming", "css", "golang",
    "flutter", "rust", "django"
]

def extract_post(html, sub_reddit):
  upvotes = html.find("div", {"class":"_1rZYMD_4xY3gRcSS3p8ODO"}).get_text(strip=True)
  title = html.find("h3", {"class":"_eYtD2XCVieq6emjKBH3m"}).get_text(strip=True)
  sub_reddit = sub_reddit
  url_atag = None
  url_atag = html.find("a", {"class":"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
  url = "/"
  
  if url_atag and url_atag["href"]:
    url = url_atag["href"]
  else:
    url_atag = html.find("a", {"class":"_13svhQIUZqD9PVzFcLwOKT"})
    if url_atag and url_atag["href"]:
      url = url_atag["href"]

  if url[0:2] == '/r':
    url = 'https://www.reddit.com' + url
  
  return {
    'title': title,
    'upvotes' : upvotes,
    'url': url,
    'sub_reddit': sub_reddit
  }

def crawl_sub_reddit(sub_reddit):
    posts = []
    
    crawl_sub_redit_url = f"https://www.reddit.com/r/{sub_reddit}/top/?t=month"
    
    request = requests.get(crawl_sub_redit_url, headers=headers)
    soup = BeautifulSoup(request.text, "html.parser")
    post_container = soup.find("div", {"class":"rpBJOHq2PR60pnwJlUyP0"})

    post_list = post_container.select("._1oQyIsiPHYt6nx7VOmd1sz")

    for post_selector in post_list:
      post = extract_post(post_selector, sub_reddit)
      posts.append(post)
    
    return posts

app = Flask("DayEleven")


@app.route("/")
def home():
    return render_template("home.html", sub_reddits=sub_reddits)


@app.route("/read")
def read():
    reading_sub_reddits = []
    posts = []

    for sub_reddit in sub_reddits:
        if request.args.get(sub_reddit, 'off') == 'on':
            reading_sub_reddits.append(sub_reddit)

    for reading_sub_reddit in reading_sub_reddits:
        posts += crawl_sub_reddit(reading_sub_reddit)

    return render_template("read.html", reading_sub_reddits=reading_sub_reddits, posts=posts)


app.run(host="0.0.0.0")
