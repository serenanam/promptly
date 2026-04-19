from dateparser.search import search_dates
from datetime import datetime
from datetime import timedelta
import re

def parse_relative_deadline(body, send_date):
    match = re.search(r"within\s+(\d+)\s+(day|hour|week)", body, re.IGNORECASE)
    if match:
        amount = int(match.group(1))
        unit = match.group(2).lower()
        if unit == "day":
            return send_date + timedelta(days=amount)
        elif unit == "hour":
            return send_date + timedelta(hours=amount)
        elif unit == "week":
            return send_date + timedelta(weeks=amount)
    return None

def parse_deadline(body: str, send_date):
    if not body:
        return None
    
    relative = parse_relative_deadline(body, send_date)
    if relative:
        return relative
    
    dates = search_dates(
        body, 
        settings={"RELATIVE_BASE": send_date}
    )
    print("Dates found:", dates)

    if dates:
        future_dates = [
            date for text, date in dates
            if date.replace(tzinfo=None) > send_date.replace(tzinfo=None)
            and date.replace(tzinfo=None) < send_date.replace(tzinfo=None) + timedelta(days=365)
            and len(text.strip()) > 5
        ]
        if future_dates:
            return min(future_dates, key=lambda d: d.replace(tzinfo=None))
        
    return None

def get_task_title(subject: str) -> str:
    noise = ["your hackerrank", "invitation to", "reminder", "- powered by hackerrank"]
    title = subject.lower()
    for phrase in noise:
        title = title.replace(phrase, "")
    return title.strip().title()

