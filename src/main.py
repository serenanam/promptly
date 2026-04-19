from .auth import connect_gmail_auth
from .extractor import extract_emails
from .db import insert_email
from .todo import show_todos
from dateparser.search import search_dates
from email.utils import parsedate_to_datetime

def main():
    print("connecting gmail auth...")
    service = connect_gmail_auth()
    print("successfully connected gmail")
    print("extracting emails...")
    emails = extract_emails(service)
    print("finished extracting emails")
    for email in emails:
        insert_email(email)
    
    show_todos()
            
if __name__ == "__main__":
    main()