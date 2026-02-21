
import json
import pandas as pd
from typing import List, Dict

# Function to load job descriptions from a JSON file
def load_job_descriptions(filepath: str = "job_descriptions.json") -> List[Dict]:
    try:
        with open(filepath, "r") as f:
            job_descriptions = json.load(f)
        return job_descriptions
    except Exception as e:
        print(f"Error loading job descriptions: {e}")
        return []

# Function to load interview questions dataset
def load_interview_questions(filepath: str = "Software_Questions.csv") -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath, encoding='ISO-8859-1')
        print("Dataset loaded successfully")
        return df
    except Exception as e:
        print(f"Error loading interview questions: {e}")
        return pd.DataFrame()

# Extract keywords from job descriptions
def extract_keywords_from_job_description(job_description: str) -> List[str]:
    predefined_keywords = [
        "Python", "Java", "SQL", "Machine Learning", "Cloud", "AWS", "Docker", 
        "React", "CI/CD", "Debugging", "Git", "APIs", "Data Structures",
        "Algorithms", "System Design", "OOP", "Agile", "Scrum", "Kubernetes",
        "DevOps", "Cybersecurity", "Frontend", "Backend",
        "Full Stack", "Software Development", "Testing", "Deployment","database", "SQL", "NoSQL", "REST", "GraphQL", "Microservices", "Performance Optimization",
    ]
    
    # Extract keywords from the job description based on predefined list
    keywords = [keyword for keyword in predefined_keywords if keyword.lower() in job_description.lower()]
    print("Extracted Keywords from Job Description:", keywords)
    return keywords
