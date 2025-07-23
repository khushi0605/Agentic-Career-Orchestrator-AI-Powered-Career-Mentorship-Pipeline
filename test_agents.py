from scraper_agent import fetch_scraped_data
from agent_testing import fetch_interview_questions
from agent_testing import web_scraping_node

# ✅ Test Web Scraper Agent
print("🔍 Testing Web Scraper Agent...\n")
scraped = fetch_scraped_data(
    role="machine learning engineer",
    location="India",
    topic="deep learning"
)
print("🧠 Interview Questions from Scraper:")
print(scraped["interview_questions"])
print("\n💼 Job Listings from Indeed:")
print(scraped["jobs"])
print("\n📚 Courses from Coursera:")
print(scraped["courses"])

# ✅ Test API Agent
print("\n🌐 Testing API-based Interview Fetcher (SerpAPI + Gemini)...\n")
questions = fetch_interview_questions("machine learning engineer")
print("🧪 Fetched Questions via API:")
for q in questions:
    print("-", q)

# Simulate a small version of the LangGraph state
test_state = {
    "target_role": "software engineer",
    "location": "India",
    "onboarding_answers": {
        "interest": "machine learning"
    }
}

# Call the web scraping node directly
output_state = web_scraping_node(test_state)

# Print the results clearly
print("\n✅ WEB SCRAPING AGENT OUTPUT\n")
print("📄 JOBS:\n", output_state.get("jobs"))
print("\n🧠 INTERVIEW QUESTIONS:\n", output_state.get("interview_questions"))
print("\n🎓 COURSES:\n", output_state.get("courses"))