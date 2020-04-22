import requests
from flask import Flask, render_template, request


base_url = "http://hn.algolia.com/api/v1"
new = f"{base_url}/search_by_date?tags=story"
popular = f"{base_url}/search?tags=story"
news_db, comment_db = {}, {}

app = Flask("DayNine")

def make_detail_url(id):
    return f"{base_url}/items/{id}"


@app.route("/")
def index():
  orderBy = request.args.get("order_by", default="popular")

  try:
    if orderBy not in news_db.keys():
      if orderBy == "popular":
          response = requests.get(popular)

      elif orderBy == "new":
          response = requests.get(new)

      news = response.json()["hits"]
      news_db[orderBy] = news
      print(news_db[orderBy])
    else:
      news = news_db[orderBy]

    return render_template("index.html", orderBy=orderBy, news=news)
  except Exception:
    error = f"Can't get {orderBy} news."

    return render_template("index.html", orderBy=orderBy, error=error)


@app.route("/<news_id>")
def detail(news_id):
  print(news_id)
  try:
    print(news_id)
    if news_id not in comment_db.keys():
      detail_url = make_detail_url(news_id)
      response = requests.get(detail_url)
      data = response.json()
      comment_db[news_id] = data

    else:
      data = comment_db[news_id]

    return render_template("detail.html", news_id=news_id, data=data)

  except Exception:
    error = f"Can't get detail information."

  return render_template("detail.html", news_id=news_id, error=error)


app.run(host="0.0.0.0")