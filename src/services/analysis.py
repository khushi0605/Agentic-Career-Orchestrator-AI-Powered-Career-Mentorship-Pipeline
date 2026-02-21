
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# Initialize HuggingFace sentiment analysis pipeline
# Lazy loading to avoid startup delay if not used immediately
_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline("sentiment-analysis")
    return _sentiment_pipeline

def analyze_text_response(text):
    pipeline = get_sentiment_pipeline()
    sentiment = pipeline(text)[0]
    return sentiment

def calculate_similarity(user_answers, dataset_answer):
    if not user_answers or not dataset_answer:
        return 0.0
        
    # Initialize the vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    
    # Combine the user answer and dataset answer into a list
    answers = [user_answers, dataset_answer]
    
    try:
        # Transform the answers into vector form
        tfidf_matrix = tfidf_vectorizer.fit_transform(answers)
        
        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return cosine_sim[0][0]  # Return the similarity score (0 to 1)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0
