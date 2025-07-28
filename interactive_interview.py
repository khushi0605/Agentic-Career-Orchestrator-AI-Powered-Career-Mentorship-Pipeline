# # score: This is the confidence score associated with the prediction. It is a probability indicating how confident the model is in its prediction.
# # label: This is the predicted sentiment label, which can be either 'POSITIVE' or 'NEGATIVE'.
# # confidence score: from 0 to 1, where 1 indicates high confidence in the prediction.(float)

#integrated 
import speech_recognition as sr
import cv2
from transformers import pipeline
import time
import streamlit as st
from deepface import DeepFace  # Import DeepFace for emotion recognition
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Initialize HuggingFace sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Function to analyze text responses
def analyze_text_response(text):
    sentiment = sentiment_pipeline(text)[0]
    return sentiment

# Function to capture voice input and convert it to text
def capture_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        print("Please speak your answer...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        # Convert speech to text using Google's speech recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Error with the speech recognition service.")
        return ""

# Function to capture webcam input and perform real-time facial emotion analysis using DeepFace
# def capture_webcam_input():
#     cap = cv2.VideoCapture(0)  # 0 is the default camera
#     print("Press 'q' to stop capturing webcam.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Detect facial emotions using DeepFace
#         try:
#             analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
#             dominant_emotion = analysis[0]['dominant_emotion']
#             print(f"Detected Emotion: {dominant_emotion}")
            
#             # Display the webcam feed with the emotion detected
#             cv2.putText(frame, f"Emotion: {dominant_emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#             cv2.imshow('Webcam', frame)
        
#         except Exception as e:
#             print(f"Error in emotion analysis: {e}")
#             # Display the webcam feed without emotion text
#             cv2.imshow('Webcam', frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     # Return the detected emotion from DeepFace
#     return {"emotion": dominant_emotion}  # Returns the emotion detected

# Function to capture webcam input and detect emotion using DeepFace
def capture_webcam_input():
    cap = cv2.VideoCapture(0)  # Use the default camera
    emotion = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect emotion using DeepFace on the current frame
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']

            # Convert the frame from BGR to RGB for Streamlit (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display the webcam feed with the emotion detected using Streamlit
            st.image(frame_rgb, channels="RGB", use_container_width=True)

            # Overlay the detected emotion on the frame
            cv2.putText(frame, f"Emotion: {emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Convert the frame to RGB and display in the browser
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display continuously updated video frame in Streamlit
            st.image(frame_rgb, channels="RGB", use_container_width=True)

        except Exception as e:
            st.write(f"Error in emotion analysis: {e}")
        
        # Press 'q' to stop the webcam feed in OpenCV
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam
    return {"emotion": emotion}

# Function to analyze the similarity of responses and dataset answers 
def calculate_similarity(user_answers, dataset_answer):
    # Initialize the vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    
    # Transform both answers into tf-idf vectors
    # tfidf_matrix = tfidf_vectorizer.fit_transform([user_answers, dataset_answer])
    # Combine the user answer and dataset answer into a list
    answers = [user_answers, dataset_answer]
    
    # Transform the answers into vector form
    tfidf_matrix = tfidf_vectorizer.fit_transform(answers)
    
    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return cosine_sim[0][0]  # Return the similarity score (0 to 1)

# Function to ask questions and gather responses (text, voice, and webcam)
def ask_questions_and_assess(questions: list):
    # results = {}
    results = {
        "text_answers": {},
        "voice_answers": {},
        "webcam_answers": {}
    }

    for question in questions:
        print(f"\nQuestion: {question}")
        
        # Text input collection
        text_response = input("Your text answer: ")
        if text_response:
            results["text"] = analyze_text_response(text_response)
        
        # Voice input collection
        voice_response = input("Would you like to answer via Voice? (yes/no): ")
        if voice_response.lower() == "yes":
            voice_response = capture_voice_input()
            if voice_response:
                results["voice"] = analyze_text_response(voice_response)
        
        # Webcam input collection
        webcam_response = input("Would you like to answer via Webcam? (yes/no): ")
        if webcam_response.lower() == "yes":
            webcam_response = capture_webcam_input()
            results["webcam"] = webcam_response  # Store the dynamic emotion

        # Provide feedback based on text/voice/webcam responses
        if "text" in results:
            print("Text Answer Sentiment:", results["text"])
        if "voice" in results:
            print("Voice Answer Sentiment:", results["voice"])
        if "webcam" in results:
            print(f"Webcam Emotion Detected: {results['webcam']['emotion']}")

        time.sleep(2)  # Add a short delay before the next question

    return results

# Main function to run the interviewer and collect results
def run_interview(state):
    print("Welcome to the AI-powered interview!")
    print("Answer the questions using text, voice, or webcam.")
    input("Press Enter to start the interview...")

    # Fetch dynamic questions from the state (which is populated by backend)
    if "relevant_interview_questions" in state:
        questions = state["relevant_interview_questions"]
    else:
        print("No questions found in state.")
        return

    results = ask_questions_and_assess(questions)

    # Save the results to a file
    with open("interview_results.txt", "w") as file:
        file.write("Interview Results:\n")
        file.write("----------------------\n")
        for key, value in results.items():
            file.write(f"{key.capitalize()} Response: {value}\n")
    
    print("\nInterview Complete! The results have been saved to 'interview_results.txt'.")

