import re
from datetime import datetime, timedelta

def parse_seconds(text):
    # Define patterns to match the duration mentioned in the text
    time_patterns = {
        'seconds': r'(\d+)\s*(seconds?|sec|s\b)',
        'minutes': r'(\d+)\s*(minutes?|min|m\b)',
        'hours': r'(\d+)\s*(hours?|hr|h\b)',
        'days': r'(\d+)\s*(days?|d\b)'
    }
    total_seconds = 0
    # Search for hours, minutes, and seconds in the text and convert them to seconds
    for unit, pattern in time_patterns.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            value = int(match[0])
            if unit == 'seconds':
                total_seconds += value
            elif unit == 'minutes':
                total_seconds += value * 60
            elif unit == 'hours':
                total_seconds += value * 3600
            elif unit == 'days':
                total_seconds += value * 86400
    return total_seconds

# Date patterns
create_event = r"\bcreate an event\b"
add_to = r"\badd to calendar\b"
relative_date_pattern = r'(tomorrow)'
all_day_pattern = r'\ball day\b'
recurring_pattern = r'\b(weekly|monthly|bimonthly|quarterly|annually|yearly)\b'
day_of_week_pattern2 = r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b'
day_of_week_pattern1 = r'every (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
date_pattern1 = r'on ((January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(st|nd|rd|th)?)'
date_pattern5 = r"\b(?:at )?(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)\b to"
date_pattern6 = r"\b(?:at )?(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)\b"
date_pattern2 = r"from ((January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(st|nd|rd|th)?) to ((January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(st|nd|rd|th)?)"
date_pattern3 = r'from ((January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(st|nd|rd|th)?)'
date_pattern4 = r'to ((January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(st|nd|rd|th)?)'

date_patterns = [create_event, relative_date_pattern, all_day_pattern, recurring_pattern, day_of_week_pattern1, day_of_week_pattern2, date_pattern1,
                 date_pattern5, date_pattern6, date_pattern2,date_pattern3, date_pattern4]

def parse_date_details(text):
    # Dictionary to hold the results
    dates_found = {
        "start_dates": [],
        "end_dates": [],
        "date_ranges": [],
        "days_of_week": [],
        "recurring_events": [],
        "relative_dates": []
    }

    # Search for specific dates
    matches = re.finditer(date_pattern1, text, flags=re.IGNORECASE)
    for match in matches:
        # Extract month and day
        full_date, month, suffix = match.groups()
        day = re.search(r'\d{1,2}', full_date).group()  # Extract the day number only
        formatted_date = f"{month} {day}"  # Format: "March 15"
        dates_found['start_dates'].append(formatted_date)

    # Adjust capturing for the simplified patterns
    matches = re.finditer(date_pattern3, text, re.IGNORECASE)
    for match in matches:
        full_date = match.group(1)
        month = match.group(2)
        day = re.search(r'\d{1,2}', full_date).group()  # Extract the day number only
        formatted_date = f"{month} {day}"  # Format: "March 15"
        dates_found['start_dates'].append(formatted_date)

    matches = re.finditer(date_pattern4, text, re.IGNORECASE)
    for match in matches:
        full_date = match.group(1)
        month = match.group(2)
        day = re.search(r'\d{1,2}', full_date).group()  # Extract the day number only
        formatted_date = f"{month} {day}"  # Format: "March 15"
        dates_found['end_dates'].append(formatted_date)

    # Search for days of the week
    days_of_week = re.findall(day_of_week_pattern1, text, flags=re.IGNORECASE)
    if days_of_week:
        dates_found['days_of_week'].extend(days_of_week)

    days_of_week = re.findall(day_of_week_pattern2, text, flags=re.IGNORECASE)
    if days_of_week:
        dates_found['days_of_week'].extend(days_of_week)

    # Search for relative dates
    relative_dates = re.findall(relative_date_pattern, text, flags=re.IGNORECASE)
    if relative_dates:
        dates_found['relative_dates'].extend(relative_dates)

    # Search for recurring events
    recurring_events = re.findall(recurring_pattern, text, flags=re.IGNORECASE)
    if recurring_events:
        dates_found['recurring_events'].extend(recurring_events)

    return dates_found

# Time patterns
single_time_pattern = r'\b(?:at )?(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)\b'
time_range_pattern2 = r"\sfrom\s\d{1,2}:\d{2}\s(AM|PM)\s+to\s\d{1,2}:\d{2}\s(AM|PM)\son\s[A-Za-z]+\s\d{1,2}(st|nd|rd|th)?"
time_range_pattern1 = r'from (\d{1,2}:\d{2}\s*(AM|PM|am|pm)?) to (\d{1,2}:\d{2}\s*(AM|PM|am|pm)?)'
all_day_pattern = r'\ball day\b'
time_patterns = [single_time_pattern, time_range_pattern2, time_range_pattern1, all_day_pattern]

def parse_time_details(text):
    time_details = {
        'Start_Time': None,
        'Stop_Time': None,
        'All_Day': None
    }

    # Check for all-day events
    if re.search(all_day_pattern, text, flags=re.IGNORECASE):
        time_details['All_Day'] = True
        return time_details

    # First, check for time ranges
    time_range_matches = re.search(time_range_pattern1, text, flags=re.IGNORECASE)
    if time_range_matches:
        time_details['Start_Time'] = time_range_matches.group(1)
        time_details['Stop_Time'] = time_range_matches.group(3)
    else:
        # If no range, look for a single time
        single_time_matches = re.search(single_time_pattern, text, flags=re.IGNORECASE)
        if single_time_matches:
            start_time_str = single_time_matches.group(1)
            time_details['Start_Time'] = start_time_str
            # Try parsing with minutes and without separately
            try:
                start_time_dt = datetime.strptime(start_time_str, '%I:%M %p')
            except ValueError:
                try:
                    start_time_dt = datetime.strptime(start_time_str, '%I %p')
                except ValueError:
                    return time_details  # If parsing fails, return current details
            # Add one hour to start time for end time
            end_time_dt = start_time_dt + timedelta(hours=1)
            time_details['Stop_Time'] = end_time_dt.strftime('%I:%M %p').lstrip('0')  # Remove leading zero

    return time_details

def extract_summaries(text):
    # Process the event description
    for pattern in date_patterns:
        text = re.sub(r'\.', '', text)
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r',\s*$', '', text)
    # text = re.sub(r'\.\s*$', '', text)

    if text:
        text = text[0].upper() + text[1:]

    return {'summary': text or 'No event description provided'}