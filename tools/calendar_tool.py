from datetime import datetime

def check_birthdays(knowledge_text):
    today = datetime.now().strftime("%B %d")
    # Simple logic to see if today's date exists in the text
    if today in knowledge_text:
        return f"Found a birthday today for: {today}!" 
    return None
