import os
import pickle
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dateutil.parser
from datetime import datetime, timedelta, timezone
from voice_parser import parse_date_details, parse_time_details, extract_summaries

# Define timezone
TIMEZONE = 'America/New_York'

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    """Authenticate and return Google Calendar service."""
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def list_events(service, days=7):
    """List upcoming events from Google Calendar within the next 'days' days."""
    import dateutil.parser

    # Calculate date range using timezone-aware datetime
    now = datetime.now(timezone.utc)  # Current time in UTC
    max_time = now + timedelta(days=days)  # Maximum time to get events

    now_iso = now.isoformat()  # Convert to ISO format
    max_time_iso = max_time.isoformat()  # Convert to ISO format

    print('Getting the upcoming events')
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now_iso,
        timeMax=max_time_iso,
        maxResults=10,  # You can change the maxResults to fetch more events
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start, event['summary'], f"End time: {end}")

    return events

def add_event(text, service):
    """Add event to Google Calendar."""
    date_details = parse_date_details(text)
    time_details = parse_time_details(text)
    summary = extract_summaries(text)['summary']

    event = {
        'summary': summary,
        'start': {
            'dateTime': f"{date_details['start_dates'][0]}T{time_details['Start_Time']}",
            'timeZone': TIMEZONE
        },
        'end': {
            'dateTime': f"{date_details['start_dates'][0]}T{time_details['Stop_Time']}",
            'timeZone': TIMEZONE
        },
        'reminders': {
            'useDefault': False,
            'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}]
        }
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")

if __name__ == '__main__':
    service = authenticate_google()
    text = "Reminder tomorrow at 9:00 AM to attend the meeting."  # Sample text
    add_event(text, service)
