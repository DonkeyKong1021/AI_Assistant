import pyttsx3
import speech_recognition as sr

TF_ENABLE_ONEDNN_OPTS=0

engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
        engine.setProperty('rate', 175)
        return True
    except:
        t = "Sorry I couldn't understand and handle this input"
        print(t)
        return False

def listen_to_speech():
    try:
        r = sr.Recognizer()
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        with sr.Microphone() as source:
            print("Listening...")
            r.energy_threshold = 4000
            audio = r.listen(source)
        try:
            print("Recognizing...")
            text = r.recognize_google(audio, language="en-in")
            print(f'You said: {text}')

        except Exception as e:
            speak("Please say that again")
            return text 
        
    except Exception as e: 
        print(e)
        return False
