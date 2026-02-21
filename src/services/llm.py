
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.config import GOOGLE_API_KEY

# Initialize Gemini model
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, google_api_key=GOOGLE_API_KEY)
