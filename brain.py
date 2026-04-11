import os
import json
from groq import Groq
from datetime import datetime
from config import GROQ_API_KEY, KNOWLEDGE_FILE
from tools.weather_tool import get_weather

client = Groq(api_key=GROQ_API_KEY)

# Simple in-memory storage for chat history
# Format: {chat_id: [messages]}
chat_histories = {}

def get_family_knowledge():
    """Reads the latest facts from the text file."""
    try:
        with open(KNOWLEDGE_FILE, "r") as f:
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
    }
]

def ask_brain(user_query, chat_id="default"):
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
    - Be mindful of the current time. If a user asks a general "how are things" or "what's up", use the time of day to give relevant updates.
    - You have access to tools. Use them when needed (e.g., for live weather).
    """

    # Build message list
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history (last 10 messages to keep context window small)
    messages.extend(chat_histories[chat_id][-10:])
    
    # Add current user message
    messages.append({"role": "user", "content": user_query})

    try:
        # Initial request to Groq
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Handle tool calls if any
        if tool_calls:
            # Add assistant's tool call message to context
            messages.append(response_message)
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "get_weather":
                    function_response = get_weather(
                        lat=function_args.get("lat"),
                        lon=function_args.get("lon")
                    )
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })

            # Get final response from LLM after tool outputs
            second_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )
            final_content = second_response.choices[0].message.content
        else:
            final_content = response_message.content

        # Update history with user query and final response
        chat_histories[chat_id].append({"role": "user", "content": user_query})
        chat_histories[chat_id].append({"role": "assistant", "content": final_content})
        
        return final_content

    except Exception as e:
        print(f"Error in brain: {e}")
        return "Sorry, I encountered an error while processing your request."
