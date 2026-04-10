import os.path
import json
from .auth import connect_gmail_auth
from .db import insert_email
import base64
from email.utils import parsedate_to_datetime

def get_header(headers, name):
    for header in headers:
        if header["name"] == name:
            return header["value"]
    return None

def get_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
    elif "body" in payload and "data" in payload["body"]:
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
    return None

def extract_emails(service):
    email_list = []
    results = service.users().messages().list(userId="me", q="subject:assessment OR subject:hackerrank").execute()
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
        return

    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        headers = msg["payload"]["headers"]

        email_list.append(
            {
        "id": message["id"],
        "thread_id": message["threadId"],
        "subject": get_header(headers, "Subject"),
        "sender": get_header(headers, "From"),
        "date": parsedate_to_datetime(get_header(headers, "Date")).isoformat(),
        "snippet": msg["snippet"],
        "body": get_body(msg["payload"]),
        "labels": msg["labelIds"],
        }   
        )
    
    return email_list
    
def main():
    service = connect_gmail_auth()
    emails = extract_emails(service)
    for email in emails:
        insert_email(email)
    

            
if __name__ == "__main__":
    main()