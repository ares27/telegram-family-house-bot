import os
import json
from groq import Groq
from datetime import datetime
from config import GROQ_API_KEY, KNOWLEDGE_FILE
from tools.weather_tool import get_weather
from tools.inventory_tool import get_inventory

client = Groq(api_key=GROQ_API_KEY)

# Simple in-memory storage for chat history
# Format: {chat_id: [messages]}
chat_histories = {}

def get_family_knowledge():
    """Reads the latest facts from the text file."""
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No family knowledge found."

# Define tools for Groq
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for the family home.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "string", "description": "Latitude of the location"},
                    "lon": {"type": "string", "description": "Longitude of the location"}
                },
                "required": ["lat", "lon"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Schedule a reminder for the family.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reminder_text": {"type": "string", "description": "The content of the reminder"},
                    "time_delta_minutes": {"type": "string", "description": "Minutes from now (e.g. '5')"}
                },
                "required": ["reminder_text", "time_delta_minutes"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_inventory",
            "description": "Get the current list of household food items and their quantities.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

def ask_brain(user_query, chat_id="default", context_data=None):
    now = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    knowledge = get_family_knowledge()
    
    # Initialize history for new chats
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
        
    system_prompt = f"""
    You are a helpful Family Assistant. Use the context below to answer.
    Today's Date and Time: {now}
    
    Family Knowledge:
    {knowledge}
    
    Instructions:
    - Respond in a warm, concise manner.
    - Use short paragraphs and bullet points for readability. Avoid long walls of text.
    - DO NOT mention birthdays or personal info unless specifically asked.
    - Be mindful of the current time for relevant updates.
    - You have access to tools. Use them when needed.
    - If a user asks for a reminder, use the 'set_reminder' tool.
    
    General Intelligence:
    - If a user asks a question that is NOT related to family knowledge (e.g., career advice, money-making ideas, general facts), answer using your broad training data as an AI. 
    - You are not limited to the 'Family Knowledge' context for general questions, but always maintain the helpful, warm Family Assistant persona.
    """

    # Build message list
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history
    messages.extend(chat_histories[chat_id][-10:])
    
    # Add current user message
    messages.append({"role": "user", "content": user_query})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = "Tool not found."
                
                if function_name == "get_weather":
                    function_response = get_weather(
                        lat=function_args.get("lat"),
                        lon=function_args.get("lon")
                    )
                elif function_name == "set_reminder":
                    # We return a structured string that main.py can intercept if needed, 
                    # or just acknowledge the intent.
                    text = function_args.get("reminder_text")
                    try:
                        mins = int(function_args.get("time_delta_minutes", 0))
                    except (ValueError, TypeError):
                        mins = 0
                    
                    print(f"DEBUG: Setting reminder for '{text}' in {mins} minutes.")
                    function_response = f"SUCCESS: Reminder set for '{text}' in {mins} minutes."
                    
                    # Store tool execution details in context_data for main.py
                    if context_data is not None:
                        context_data['reminder'] = {"text": text, "minutes": mins}
                    else:
                        print("DEBUG: context_data was None, cannot set reminder callback.")
                
                elif function_name == "get_inventory":
                    function_response = get_inventory()
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

            second_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            final_content = second_response.choices[0].message.content
        else:
            final_content = response_message.content

        chat_histories[chat_id].append({"role": "user", "content": user_query})
        chat_histories[chat_id].append({"role": "assistant", "content": final_content})
        
        return final_content


    except Exception as e:
        print(f"Error in brain: {e}")
        return "Sorry, I encountered an error while processing your request."
