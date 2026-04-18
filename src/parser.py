from dateparser.search import search_dates
from datetime import datetime
from datetime import timedelta
import re

def parse_deadline(body: str, send_date):
    if not body:
        return None
    
    match = re.search(r"(\d+)[-\s]hour", body, re.IGNORECASE)
    if match:
        hours = int(match.group(1))
        return send_date + timedelta(hours=hours)
    
    dates = search_dates(
        body, 
        settings={"RELATIVE_BASE": send_date}
    )
    if dates:
        future_dates = [
            date for text, date in dates 
            if date.replace(tzinfo=None) > send_date.replace(tzinfo=None)
            and date.replace(tzinfo=None) < send_date.replace(tzinfo=None) + timedelta(days=365)
        ]
        if future_dates:
            return max(future_dates, key=lambda d: d.replace(tzinfo=None))
    return None

def get_task_title(subject: str) -> str:
    noise = ["your hackerrank", "invitation to", "reminder", "- powered by hackerrank"]
    title = subject.lower()
    for phrase in noise:
        title = title.replace(phrase, "")
    return title.strip().title()

