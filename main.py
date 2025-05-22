import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import time
import threading

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed percent
engine.setProperty('volume', 1.0)  # Volume 0-1

# Speak function
def speak(text):
    print(f"Jarves: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen to user
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
    except Exception as e:
        speak("Sorry, I didn't catch that. Can you repeat?")
        return ""
    return query.lower()

# Greet user
def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I'm Jarves 2025. How can I assist you today?")

# Get weather info
def get_weather(city="Delhi"):
    API_KEY = "your_openweather_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url).json()
        if res["cod"] != 200:
            speak("City not found.")
        else:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}.")
    except:
        speak("Failed to get weather information.")

# Set a reminder
def set_reminder(minutes, message):
    def reminder_task():
        time.sleep(minutes * 60)
        speak(f"Reminder: {message}")
    threading.Thread(target=reminder_task).start()
    speak(f"Reminder set for {minutes} minutes.")

# Perform a web search
def search_web(query):
    speak(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Main logic
def run_jarves():
    greet()
    while True:
        query = listen()
        if "weather" in query:
            speak("Which city?")
            city = listen()
            if city:
                get_weather(city)

        elif "remind me" in query:
            speak("After how many minutes?")
            try:
                mins = int(listen())
                speak("What should I remind you about?")
                msg = listen()
                set_reminder(mins, msg)
            except:
                speak("Sorry, I couldn’t understand the time.")

        elif "search" in query:
            speak("What should I search?")
            term = listen()
            if term:
                search_web(term)

        elif "exit" in query or "bye" in query:
            speak("Goodbye, Priyanshu. Have a great day!")
            break

        elif query:
            speak("Sorry, I don't recognize that command yet.")

if __name__ == "__main__":
    run_jarves()
