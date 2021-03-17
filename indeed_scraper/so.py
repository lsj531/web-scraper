import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&sort=i"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    # company, location = html.find("div", {"class": "fl1"}).find("h3").find_all("span", reculsive=False)
    if html.find("h3", {"class": "mb4"}).find("span", {"class": "s-tag"}) is not None:
        company, via, location = html.find("h3", {"class": "mb4"}).find_all("span", reculsive=False)  # <span>영역이 3개인 경우
    else:
        company, location = html.find("h3", {"class": "mb4"}).find_all("span", reculsive=False)  # <span>영역이 2개인 경우도 있음
    company = company.get_text(strip=True)
    company = company.replace('via', ' via ')
    location = location.get_text(strip=True).strip("-").strip(" \r").strip("\n")
    job_id = html['data-jobid']
    return {'title': title, 'company': company, 'location': location,
            "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scraping SO: Page: {page}")
        result = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
