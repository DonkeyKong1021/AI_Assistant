from datetime import datetime, timedelta
from num2words import num2words
from nlp_processing import parse_seconds
import playsound
import tkinter as tk
from threading import Timer, Thread
import time

def time_():
    current_time = datetime.now()
    hours = current_time.strftime("%I")  # Hour in 12-hour format (01 to 12)
    minutes = current_time.strftime("%M")  # Minute (00 to 59)
    am_pm = current_time.strftime("%p")  # AM or PM
    hours = hours.lstrip('0')
    if minutes == "00":  # If exactly on the hour
        time = f"It is {num2words(hours)} o'clock {am_pm.lower()}"
    else:
        time = f"It is {hours}:{minutes} {am_pm.lower()}"
    return time

def date_():
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    date = f"Today is {month_names[month]} {num2words(day, to='ordinal')}, {str(year)}"
    print(date)
    return date

def countdown(time_sec):
    def run():
        for t in range(time_sec, -1, -1):
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r', flush=True)
            time.sleep(1)
        print("Time's up!")

    Thread(target=run).start()

def set_timer(text):
    try:
        seconds = parse_seconds(text)
        if seconds == 0:
            return "Please specify a valid time to set the timer."
        if seconds < 0:
            return "Cannot set a timer for negative duration"

        print(f"Timer set for {seconds} seconds. Countdown starting...")
        countdown(seconds)  # Start the countdown
        return "Timer is running..."

    except Exception as e:
        return f"Something went wrong while setting the timer: {str(e)}"
    

