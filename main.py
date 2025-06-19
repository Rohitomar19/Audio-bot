import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiprocess(command):
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, that song is not in the music library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for arti in articles[:5]:
                speak(arti['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiprocess(c)
        speak(output) 

if __name__ == "__main__":
    speak("Initializing Jarvis")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            wake_word = recognizer.recognize_google(audio)
            if wake_word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis is listening...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processcommand(command)
        except Exception as e:
            print(f"Error: {e}")
