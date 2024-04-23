import pyttsx3
import re
import keyboard
import webbrowser as wb
from time import sleep
from voice_recognition import listen_to_speech, speak
from initializtion_sequence import initializtion
from nlp_processing import *
from task_manager import *

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Specify the path to Chrome
chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"  # Update this path as necessary

def main():
    initializtion()
    while True:
        try:
            if keyboard.read_key() == 'space':  # Waits for space key press
                text = listen_to_speech()
                print(f"Received: {text}")

                if re.search(r"\bstop\b", text, re.IGNORECASE):
                    print("Voice Assistant Deactivated.")
                    speak("Voice Assistant Deactivated.")
                    break
                elif re.search(r"set a timer", text, re.IGNORECASE):
                    response = set_timer(text)
                elif re.search(r"\btime\b", text, re.IGNORECASE):
                    response = time_()
                elif re.search(r"\bdate\b", text, re.IGNORECASE):
                    response = date_()
                elif re.search(r"open google", text, re.IGNORECASE):
                    wb.get(chrome_path).open("https://google.com")
                    response = "Opening Google in Chrome"
                elif re.search(r"open youtube", text, re.IGNORECASE):
                    wb.get(chrome_path).open("youtube.com")
                    response = "Opening YouTube in Chrome"
                elif re.search(r"open X", text, re.IGNORECASE):
                    wb.get(chrome_path).open("twitter.com")
                    response = "Opening X in Chrome"
                elif re.search(r"open twitter", text, re.IGNORECASE):
                    wb.get(chrome_path).open("twitter.com")
                    response = "Opening X in Chrome"    
                else:
                    response = process_command(text)

                print(f"Response: {response}")
                speak(response)
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, I didn't catch that. Please try again.")
        sleep(0.1)  # Short delay to prevent high CPU usage

if __name__ == "__main__":
    main()
                                                    