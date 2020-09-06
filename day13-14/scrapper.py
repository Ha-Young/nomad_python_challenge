import requests
from bs4 import BeautifulSoup

WEWORK_REMOTELY_URL = "https://weworkremotely.com/remote-jobs/search?term={}"
STACK_OVERFLOW_URL = "https://stackoverflow.com/jobs?r=true&q={}"
REMOTE_OK_URL = "https://remoteok.io/remote-dev+{}-jobs"


def get_text_response(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception

        return response.text

    except Exception:
        return None


def create_job_dict(url, company, title):
    return {"url": url, "company": company, "title": title}


def scrap_weworkremote(searching_by):
    text = get_text_response(WEWORK_REMOTELY_URL.format(searching_by))
    html = BeautifulSoup(text, "html.parser")
    features = html.find_all("li", {"class": "feature"})

    result = []

    for feature in features:
        detail = feature.find_all("a")

        if len(detail) > 1:
            detail = detail[1]
        else:
            detail = detail[0]

        url = "https://weworkremotely.com" + detail["href"].strip()
        company = feature.find(
            "span", {"class": "company"}).get_text(strip=True)
        title = feature.find("span", {"class": "title"}).get_text(strip=True)

        result.append(create_job_dict(url, company, title))

    return result


def scrap_stackoverflow(searching_by):
    text = get_text_response(STACK_OVERFLOW_URL.format(searching_by))
    html = BeautifulSoup(text, "html.parser")
    list_results = html.find("div", {"class": "listResults"})
    grids = list_results.find_all("div", {"class": "grid"})

    result = []

    for grid in grids:
        a_tag = grid.find("a", {"class": "s-link stretched-link"})

        if not a_tag:
            continue

        url = "https://stackoverflow.com" + a_tag["href"].strip()
        title = a_tag["title"].strip()
        company = (
            grid.find("h3", {"class": "fc-black-700 fs-body1 mb4"})
            .find("span")
            .get_text(strip=True)
        )

        result.append(create_job_dict(url, company, title))

    return result


def scrap_remoteok(searching_by):
    text = get_text_response(REMOTE_OK_URL.format(searching_by))
    html = BeautifulSoup(text, "html.parser")
    table = html.find("table", {"id": "jobsboard"})
    jobs = table.find_all(
        "td", {"class": "company position company_and_position"}
    )

    result = []

    for job in jobs:
        link = job.find("a", {"class": "preventLink"})
        if link != None:
            url = "https://remoteok.io" + link["href"]
        else:
            url = "/"
        prev_title = job.find("h2", {"itemprop": "title"})
        if prev_title != None:
            title = prev_title.get_text(strip=True)
        else:
            continue
        company = job.find("h3", {"itemprop": "name"}).get_text(strip=True)

        result.append(create_job_dict(url, company, title))

    return result


def scrap_remote_jobs(searching_by):
    weworkremotely_jobs = scrap_weworkremote(searching_by)
    print(weworkremotely_jobs)
    stackoverflow_jobs = scrap_stackoverflow(searching_by)
    print(stackoverflow_jobs)
    remoteok_jobs = scrap_remoteok(searching_by)
    print(remoteok_jobs)

    return weworkremotely_jobs + stackoverflow_jobs + remoteok_jobs
