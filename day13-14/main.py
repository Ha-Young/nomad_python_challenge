"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, Response
from scrapper import scrap_remote_jobs
from csv_extract import csv_extract

app = Flask("Gruding's remote jobs")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    searching_by = request.args.get("searching-by", "").lower()
    if searching_by == "":
        redirect("/")

    print("search", searching_by)

    if searching_by not in db:
        db[searching_by] = scrap_remote_jobs(searching_by)

    print(db[searching_by])

    return render_template("search.html", searching_by=searching_by, jobs=db[searching_by])


@app.route("/csv")
def csv():
    export_job = request.args.get("export_job", "").lower()
    if export_job == "":
        redirect("/")

    print("export", export_job)

    if export_job in db:
        return csv_extract(db[export_job], Response, export_job)
    else:
        redirect("/")


app.run(host="0.0.0.0")
