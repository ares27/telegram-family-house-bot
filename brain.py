# Logic for Groq calls and Prompt construction
import os
from groq import Groq
from datetime import datetime
from config import GROQ_API_KEY, KNOWLEDGE_FILE

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = Groq(api_key=GROQ_API_KEY)

def get_family_knowledge():
    """Reads the latest facts from the text file."""
    try:
        with open(KNOWLEDGE_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No family knowledge found. Please create knowledge.txt."

def ask_brain(user_query):
    now = datetime.now().strftime("%A, %B %d, %Y")
    knowledge = get_family_knowledge()
    
    prompt = f"""
    You are a helpful Family Assistant. Use the context below to answer.
    Today's Date: {now}
    
    Family Knowledge:
    {knowledge}
    
    User Question: {user_query}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, I encountered an error while processing your request."   