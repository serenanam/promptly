from googleapiclient.errors import HttpError

def add_to_calendar(calendar_service, email: dict):
    event = {
        "summary": email["title"],
        "description": email["link"],
        "start": {
            "dateTime": email["deadline"],
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": email["deadline"],
            "timeZone": "UTC",
        },
    }
    
    try:
        created_event = calendar_service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")
    