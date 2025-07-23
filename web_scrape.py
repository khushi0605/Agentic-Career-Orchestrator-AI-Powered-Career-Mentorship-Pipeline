import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
url = "https://www.naukri.com/software-engineer-jobs-in-kolkata?k=software%20engineer&l=kolkata&experience=0&nignbevent_src=jobsearchDeskGNB"

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())  # Debugging line to see the HTML structure

job_titles = []
print(soup.find_all("div", class_="srp-jobtuple-wrapper"))
# for job_card in soup.find_all("div", class_="srp-jobtuple-wrapper"):
    # print(job_card.prettify())  # Debugging line to see the job card structure
    # title_tag = job_card.select_one("h2.jobTitle span")
    # if title_tag:
    #     job_titles.append(title_tag.get_text(strip=True))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get(url)

# Wait for JS to load
driver.implicitly_wait(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
print(soup.prettify())  # Debugging line to see the HTML structure
jobs = soup.select("div.jobTuple")  # Example job card class

for job in jobs:
    title = job.select_one("a.title").text.strip()
    company = job.select_one("a.subTitle").text.strip()
    print(f"{title} at {company}")

driver.quit()

