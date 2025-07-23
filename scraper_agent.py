import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

#agents to scrape web data for what api's are supposed to return 
#job listings
def scrape_indeed_jobs(role="software engineer", location="India"):

    # headers = {'User-Agent': UserAgent().random}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    role_query = role.replace(" ", "+")
    url = "https://www.naukri.com/software-engineer-jobs-in-kolkata?k=software%20engineer&l=kolkata&experience=0&nignbevent_src=jobsearchDeskGNB"

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.prettify())  # Debugging line to see the HTML structure

    job_titles = []
    for job_card in soup.select("li.css-1ac2h1w"):
        title_tag = job_card.select_one("h2.jobTitle span")
        if title_tag:
            job_titles.append(title_tag.get_text(strip=True))

    return job_titles or ["No jobs found"]


#https://www.naukri.com/ai-engineer-jobs?k=ai%20engineer&experience=0
#https://www.naukri.com/software-engineer-jobs-in-kolkata?k=software%20engineer&l=kolkata&experience=0&nignbevent_src=jobsearchDeskGNB

#interview questions
def scrape_gfg_questions():
    url = "https://www.geeksforgeeks.org/tag/placement-preparation/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    titles = []
    containers = soup.select("div.TagCategoryArticle_articleContainer__yJdy6")

    for container in containers:
        header = container.select_one("div.TagCategoryArticle_articleContainer_headerContainer-header__OVTzc")
        if header:
            titles.append(header.get_text(strip=True))

    return titles or ["No questions found"]

#courses 
def scrape_coursera_courses(query="ai engineer"):
    q = query.replace(" ", "%20")
    url = f"https://www.coursera.org/search?query={q}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    courses = []
    cards = soup.select("h3.cds-CommonCard-title")

    for card in cards:
        course_title = card.get_text(strip=True)
        if course_title:
            courses.append(course_title)

    return courses or ["No courses found"]

#combining all scrapers
def fetch_scraped_data(role="software engineer", location="India", topic="AI"):
    print("▶️ Running fetch_scraped_data...")
    jobs = scrape_indeed_jobs(role, location)
    print("📄 JOBS:", jobs[:3])  # Show first 3 jobs

    questions = scrape_gfg_questions()
    print("🧠 QUESTIONS:", questions[:3])

    courses = scrape_coursera_courses(topic)
    print("🎓 COURSES:", courses[:3])

    return {
        "jobs": jobs,
        "interview_questions": questions,
        "courses": courses
    }