from .auth import connect_gmail_auth
from .extractor import extract_emails, insert_email
from .todo import show_todos

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