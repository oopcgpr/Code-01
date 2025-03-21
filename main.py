import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime

# Set up Gemini API Key
API_KEY = "AIzaSyAh_3-jQoSh7EIDxHBw7_lJDMmt4Sh4D00"
genai.configure(api_key=API_KEY)

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Try a slower rate (120-150 is optimal)
engine.setProperty("rate", 200)

# Try a different voice (Use 'Daniel' or 'Samantha' for better quality on Mac)
voices = engine.getProperty("voices")
for voice in voices:
    if "Daniel" in voice.name:  # Daniel (Male) or Samantha (Female)
        engine.setProperty("voice", voice.id)
        break

# Conversation Memory
memory = []

# Function to make AI speak
def say(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User: {query}")
            return query.lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# Function to process AI response with memory
def ask_ai(query):
    global memory
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        
        # Add conversation history to the query
        full_context = "\n".join(memory[-10:])  # Use last 10 messages to limit size
        prompt = f"Previous conversation:\n{full_context}\n\nUser: {query}\nAI:"

        response = model.generate_content(prompt)
        response_text = response.text
        print(f"Jarvis: {response_text}")
        say(response_text)

        # Save conversation to memory
        memory.append(f"User: {query}")
        memory.append(f"AI: {response_text}")

        return response_text
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't process that."

# Main function
if __name__ == "__main__":
    say("Hello! I am Alex. How can I assist you today?")
    
    while True:
        query = take_command()

        # Open Websites
        if "open youtube" in query:
            say("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            say("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open wikipedia" in query:
            say("Opening Wikipedia")
            webbrowser.open("https://www.wikipedia.org")

        elif "open whatsapp" in query:
            say("Opening Whatsapp")
            webbrowser.open("https://web.whatsapp.com/")

        # Check Time
        elif "the time" in query:
            now = datetime.datetime.now()
            time_str = now.strftime("%H:%M")
            say(f"The time is {time_str}")

        # Play Music
        elif "play music" in query:
            os.system("open /path/to/your/music.mp3")

        # Chat with AI
        elif "using artificial intelligence" in query:
            ask_ai(query)

        # Exit Command
        elif "jarvis quit" in query or "exit" in query:
            say("Goodbye! Have a great day.")
            break

        # AI Chat Mode (with memory)
        else:
            ask_ai(query)
