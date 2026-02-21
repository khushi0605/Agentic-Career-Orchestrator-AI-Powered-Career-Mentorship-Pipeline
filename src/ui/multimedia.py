
import streamlit as st
import speech_recognition as sr
import cv2
from deepface import DeepFace

# Function to capture voice input and convert it to text
def capture_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        st.info("Listening... Please speak now.")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.success("Audio captured. Processing...")
        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please try again.")
            return ""
        
    try:
        # Convert speech to text using Google's speech recognition
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        st.error("Error with the speech recognition service.")
        return ""

# Function to capture webcam input and detect emotion using DeepFace
def capture_webcam_input():
    # Use a unique key for the camera input to avoid conflicts
    img_file = st.camera_input("Take a snapshot for emotion analysis")
    
    if img_file is not None:
        try:
            # Save the uploaded file temporarily
            with open("temp_webcam.jpg", "wb") as f:
                f.write(img_file.getbuffer())
            
            # Analyze the image using DeepFace
            # enforce_detection=False allows analysis even if face is not perfectly clear
            analysis = DeepFace.analyze("temp_webcam.jpg", actions=['emotion'], enforce_detection=False)
            
            if isinstance(analysis, list):
                emotion = analysis[0]['dominant_emotion']
            else:
                emotion = analysis['dominant_emotion']
                
            return {"emotion": emotion}
        except Exception as e:
            st.error(f"Error in emotion analysis: {e}")
            return None
    return None
