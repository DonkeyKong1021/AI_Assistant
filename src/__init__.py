from voice_recognition import speak
from datetime import datetime

def greeting():
    hour = datetime.now().hour
    if hour >= 4 and hour < 12:
        return "Good Morning!"
    elif hour >= 12 and hour < 16:
        return "Good Afternoon!"
    elif hour >= 16 and hour < 24:
        return "Good Evening!"
    else:
        return "Hi Drunk, Im High!"
    
def tell_time():
    time = datetime.now()
    # Get the hour and minute with potential leading zero
    current_time = time.strftime('%I:%M %p')
    # Remove leading zero from the hour if it exists
    current_time = current_time.lstrip("0").replace(" 0", " ")
    return f"The current time is {current_time}"

def initializtion():
    greet = greeting()
    time = tell_time()
    speak("Initializing Jarvis")
    print("Initializing Jarvis")
    speak("Starting all systems applications")
    print("Starting all systems applications")
    speak("Installing and checking all drivers")
    print("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    print("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    print("Checking the internet connection")
    speak("Wait a moment sir")
    print("Wait a moment sir")
    speak("All drivers are up and running")
    print("All drivers are up and running")
    speak("All systems have been activated")
    print("All systems have been activated")
    speak("Now I am online")
    print("Now I am online")
    speak(greet)
    print(greet)
    speak(time)
    print(time)
    print("Press 'space' to start listening...")
    speak("Press 'space' to start listening...")
    print("How can I assist you today?")
    speak("How can I assist you today?")
