import speech_recognition as sr
import pyttsx3
import requests
import json

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Gemini API endpoint and your API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = "XYZ"  # Replace with your actual Gemini API key

# Memory to store past conversations
memory = []

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's voice and convert it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

def call_gemini_api(prompt):
    """Call the Gemini API with the user's prompt and memory."""
    headers = {
        "Content-Type": "application/json"
    }
    # Include memory in the API request
    data = {
        "contents": [
            *memory,  # Include past conversations
            {
                "role": "user",  # Correct role for the current prompt
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={API_KEY}",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            response_json = response.json()
            # Extract the generated text from the response
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return generated_text
        else:
            print(f"API Error: {response.status_code}, {response.text}")
            return "Sorry, I encountered an error."
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an error."

def perform_calculation(expression):
    """Perform basic calculations."""
    try:
        result = eval(expression)
        return f"The result is {result}"
    except Exception as e:
        return f"Sorry, I couldn't calculate that. Error: {e}"

def main():
    speak("Hello! I am your AI assistant. How can I help you today?")
    while True:
        user_input = listen()
        if user_input:
            if "calculate" in user_input.lower():
                # Handle calculations separately
                expression = user_input.lower().replace("calculate", "").strip()
                result = perform_calculation(expression)
                speak(result)
            else:
                # Call Gemini API for general queries
                response = call_gemini_api(user_input)
                # Update memory with the latest conversation
                memory.append({
                    "role": "user",  # Correct role for user input
                    "parts": [{"text": user_input}]
                })
                memory.append({
                    "role": "model",  # Correct role for AI response
                    "parts": [{"text": response}]
                })
                speak(response)

if __name__ == "__main__":
    main()
