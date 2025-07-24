import pandas as pd

# Load the dataset
def load_interview_questions(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        print("Dataset loaded successfully")
        print(df.head())  # Print the first few rows to inspect the structure
        return df
    except Exception as e:
        print(f"Error loading interview questions: {e}")
        return pd.DataFrame()

# Example usage
file_path="Software_Questions.csv"
interview_questions_df = load_interview_questions(file_path)
