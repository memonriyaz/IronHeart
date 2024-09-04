import webbrowser
import pyttsx3
import time
import pygame
import google.generativeai as genai
from transformers import pipeline
import re
import speech_recognition as sr
from googleapiclient.discovery import build

pygame.mixer.init()
engine = pyttsx3.init()
engine.setProperty('rate', 200)

start = 'C:\\Users\\riyaz\\Desktop\\Riyaz\\Python\\MegaProject\\Assets\\aistart.mp3'
error = 'C:\\Users\\riyaz\\Desktop\\Riyaz\\Python\\MegaProject\\Assets\\aierror.mp3'
complete = 'C:\\Users\\riyaz\\Desktop\\Riyaz\\Python\\MegaProject\\Assets\\aicomplete.mp3'
end = 'C:\\Users\\riyaz\\Desktop\\Riyaz\\Python\\MegaProject\\Assets\\aiend.mp3'

# Initialize sound effects
start_sound = pygame.mixer.Sound(start)
error_sound = pygame.mixer.Sound(error)
complete_sound = pygame.mixer.Sound(complete)
end_sound = pygame.mixer.Sound(end)

# Initialize API clients
api_key_youtube = 'AIzaSyD1HbFdoJmfEdocWYohsDqfqEB_hSE8SYg'
youtube = build('youtube', 'v3', developerKey=api_key_youtube)

gemini_api_key = 'AIzaSyAqWrWlVWBRGR85Dts2Q4SQpFFGpTq2gqI'
genai.configure(api_key=gemini_api_key)

# Lazy loading models
def load_models():
    global summarizer, model
    summarizer = pipeline("summarization")
    model = genai.GenerativeModel("gemini-1.5-flash")

def youtube_search(query):
    request = youtube.search().list(part='snippet', maxResults=1, q=query)
    response = request.execute()
    if response['items']:
        item = response['items'][0]
        video_id = item['id'].get('videoId')
        playlist_id = item['id'].get('playlistId')
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        elif playlist_id:
            playlist_items = youtube.playlistItems().list(
                part='snippet', playlistId=playlist_id, maxResults=1
            ).execute()
            if playlist_items['items']:
                first_video_id = playlist_items['items'][0]['snippet']['resourceId']['videoId']
                return f"https://www.youtube.com/watch?v={first_video_id}"
    return None

def speak(text):
    engine.say(text)
    engine.runAndWait()

def sanitize_text(text):
    return re.sub(r'\*+', '', text)

def summarize_text(text, max_length=50):
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def process_command(command):
    command = command.lower()
    if "open" in command:
        website = command.partition("open ")[2].strip()
        url = f"https://{website}" if "." in website else f"https://www.google.com/search?q={website.replace(' ', '+')}"
        try:
            webbrowser.open(url)
            end_sound.play()
            time.sleep(end_sound.get_length())
        except Exception as e:
            print(f"Failed to open {url}: {e}")

    elif "play" in command and "youtube" in command:
        words = command.split()
        search_term = " ".join(words[words.index("play") + 1:words.index("on")])
        first_video_url = youtube_search(search_term.replace(" ", "+"))
        if first_video_url:
            speak(f"Playing {search_term} on YouTube")
            webbrowser.open(first_video_url)
        else:
            speak(f"Could not find {search_term} on YouTube")
            end_sound.play()
            time.sleep(end_sound.get_length())
    
    else:
        question = command.replace("ask", "").strip()
        response = model.generate_content(question)
        summary_text = summarize_text(response.text, max_length=50)
        clean_summary_text = sanitize_text(summary_text)
        speak(clean_summary_text)
        end_sound.play()
        time.sleep(end_sound.get_length())
        
        speak("Would you like more details? Say 'sure' for more details or 'no' to continue.")
        with sr.Microphone() as source:
            audio_data = recognizer.listen(source, timeout=15)
            try:
                user_response = recognizer.recognize_google(audio_data).lower()
                if 'sure' in user_response:
                    detailed_response_text = response.text
                    speak(sanitize_text(detailed_response_text))
                    end_sound.play()
                    time.sleep(end_sound.get_length())
                else:
                    speak("Okay, moving on.")
                    end_sound.play()
                    time.sleep(end_sound.get_length())
            except sr.UnknownValueError:
                print("Sorry, I did not understand your response.")
            except sr.RequestError:
                error_sound.play()
                time.sleep(error_sound.get_length())
                speak("Currently we are facing issues, please try later")
            except Exception as e:
                error_sound.play()
                time.sleep(end_sound.get_length())
                print(f"Error: {e}")

if __name__ == "__main__":
    speak("Initializing Ironheart")
    recognizer = sr.Recognizer()
    load_models()

    while True:
        print("Listening")
        with sr.Microphone() as source:
            audio_data = recognizer.listen(source, phrase_time_limit=1.5)
            try:
                text = recognizer.recognize_google(audio_data)
                if text.lower().replace(" ", "") == "ironheart":
                    start_sound.play()
                    time.sleep(start_sound.get_length())
                    speak("Yes Sir,")
                    print("IronHeart Active")
                    with sr.Microphone() as source:
                        audio_data = recognizer.listen(source, timeout=15)
                        complete_sound.play()
                        time.sleep(complete_sound.get_length())
                        command = recognizer.recognize_google(audio_data)
                        process_command(command)
                
            except sr.UnknownValueError:
                print("Sorry, could not understand audio.")
            except sr.RequestError:
                error_sound.play()
                time.sleep(error_sound.get_length())
                speak("Currently we are facing issues, please try later")
            except Exception as e:
                error_sound.play()
                time.sleep(end_sound.get_length())
                print(f"Error: {e}")
