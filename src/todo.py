from .db import supabase
from datetime import datetime

def show_todos():
    response = supabase.table("emails")\
        .select("title, deadline")\
        .not_.is_("deadline", "null")\
        .order("deadline")\
        .execute()
    
    for task in response.data:
        deadline = datetime.fromisoformat(task['deadline'])
        formatted = deadline.strftime("%b %d, %Y %I:%M %p")
        print(f"{formatted} - {task['title']}")

