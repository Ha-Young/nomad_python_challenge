import requests
from flask import Flask, render_template, request, redirect

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new_url = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular_url = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

def get_storys(order_by):
  print("get_storys", order_by)
  try:
    request_url = None
    if order_by == "popular":
      request_url = popular_url
    elif order_by == "new":
      request_url = new_url
    else:
      raise Exception()
    
    print(request_url)
    res = requests.get(request_url)
    
    if res.status_code != 200:
      return None

    data = res.json()
    data = data['hits']

    print(data)
    return data
  except:
    return None

def render_story(order_by):
  if order_by not in db:
    storys = get_storys(order_by)
    storys = list(map(lambda story: {'title':story['title'], 'author':story['author'], 'points': story['points'], 'url': story['url'], 'id': story['objectID'], 'comments': story['num_comments']}, storys))
    db[order_by] = storys

  print(db[order_by])
  return render_template("index.html", storys = db[order_by], order_by = order_by)

def render_detail(id):
  detail_url = make_detail_url(id)
  try:
    res = requests.get(detail_url)
    data = res.json()
    print(data)
    return render_template("detail.html", story = data)
  except:
    raise Exception()

db = {}
app = Flask("DayNine")

@app.route("/")
def home():
  order_by = request.args.get('order_by')
  if order_by:
    return render_story(order_by)
  else:
    return render_story("popular")

@app.route("/<id>")
def detail(id):
  return render_detail(id)

app.run(host="0.0.0.0")