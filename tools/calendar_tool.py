import re
from datetime import datetime

def check_birthdays(knowledge_text):
    """
    Parses the knowledge text for birthdays and returns information about
    today's birthdays and upcoming birthdays.
    """
    # Regex to find names and dates (DD-MM-YYYY or DD/MM/YYYY)
    # Looking for patterns like "Name's birthday is DD-MM-YYYY"
    pattern = r"([A-Za-z\s'\(]+) birthday is (\d{2})[-/](\d{2})[-/](\d{4})"
    matches = re.findall(pattern, knowledge_text)
    
    if not matches:
        return None

    today = datetime.now()
    today_birthdays = []
    upcoming_birthdays = []

    for name_raw, day, month, year in matches:
        name = name_raw.strip().replace("'s", "")
        try:
            bday_this_year = datetime(today.year, int(month), int(day))
        except ValueError:
            continue # Invalid date

        # If birthday already passed this year, look at next year
        if bday_this_year.date() < today.date():
            bday_next = datetime(today.year + 1, int(month), int(day))
        else:
            bday_next = bday_this_year

        days_until = (bday_next.date() - today.date()).days
        
        # Format the date nicely
        day_int = int(day)
        suffix = 'th' if 11 <= day_int <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day_int % 10, 'th')
        formatted_date = bday_next.strftime(f"%B {day_int}{suffix}")

        entry = {
            "name": name,
            "date": formatted_date,
            "days_until": days_until,
            "original_year": year
        }

        if days_until == 0:
            today_birthdays.append(entry)
        elif days_until <= 30: # Look ahead 30 days
            upcoming_birthdays.append(entry)

    lines = []
    if today_birthdays:
        for b in today_birthdays:
            lines.append(f"🎉 Today is {b['name']}'s birthday ({b['date']})!")
    
    if upcoming_birthdays:
        # Sort by closest
        upcoming_birthdays.sort(key=lambda x: x['days_until'])
        for b in upcoming_birthdays:
            lines.append(f"🎂 Upcoming: {b['name']} on the {b['date']} (in {b['days_until']} days).")

    return "\n".join(lines) if lines else "No upcoming birthdays in the next 30 days."

def get_birthday_info(name, knowledge_text):
    """Specific lookup for a person's birthday."""
    pattern = r"([A-Za-z\s'\(]*" + re.escape(name) + r"[A-Za-z\s'\(]*) birthday is (\d{2})[-/](\d{2})[-/](\d{4})"
    match = re.search(pattern, knowledge_text, re.IGNORECASE)
    
    if match:
        full_name, day, month, year = match.groups()
        day_int = int(day)
        suffix = 'th' if 11 <= day_int <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day_int % 10, 'th')
        month_name = datetime(2000, int(month), 1).strftime("%B")
        clean_name = full_name.strip().replace("'s", "")
        return f"{clean_name} was born on the {day_int}{suffix} of {month_name}, {year}."
    
    return f"I couldn't find a birthday for {name} in my records."
