# Entry point: Handlers and Bot setup
import os
import uvicorn
from groq import Groq
from fastapi import FastAPI
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from brain import ask_brain
from config import GROQ_API_KEY, TELEGRAM_TOKEN, FAMILY_IDS, FAMILY_GROUP_ID
from datetime import time
import pytz # Recommended for handling your local timezone
from tools.weather_tool import get_weather

app = FastAPI()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = Groq(api_key=GROQ_API_KEY)

# ensure this is in the .env
HOME_LAT = os.getenv("HOME_LAT", "-25.806207") 
HOME_LON = os.getenv("HOME_LON", "28.148774")  



@app.get("/")
def home():
    return {"status": "Family Bot is live on FastAPI"}

def run_fastapi():
    # Render provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the bot is alive."""
    if update.effective_user.id not in FAMILY_IDS:
        return
    await update.message.reply_text("🏓 Pong! I'm online and ready to help.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Family Bot is online! Ask me anything about the house.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in FAMILY_IDS:
        return
    
    # Show "typing..." in Telegram while the AI thinks
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Call the isolated brain with chat_id for memory
    chat_id = update.effective_chat.id
    response = ask_brain(update.message.text, chat_id=chat_id)
    await update.message.reply_text(response)


async def morning_briefing(context):
    """Background task to send a daily summary including weather."""
    # 1. Fetch live weather
    weather_data = get_weather(HOME_LAT, HOME_LON)
    
    # 2. Build the prompt for the AI
    brief_query = f"""
    Context: Today's weather is {weather_data}. 
    Based on this and our family knowledge, give me a warm, 3-bullet point morning briefing. 
    If it's rainy, remind the family to take umbrellas!
    """
    
    ai_response = ask_brain(brief_query)
    
    # 3. Send to family group
    await context.bot.send_message(
        chat_id=FAMILY_GROUP_ID, 
        text=f"☀️ **Good Morning Family!**\n\n{ai_response}"
    )

async def handle_voice(update, context):
    """Transcribe voice memos sent to the bot."""
    if update.effective_user.id not in FAMILY_IDS:
        return

    await update.message.reply_text("✨ I'm listening...")
    
    # 1. Download the voice file from Telegram
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    file_path = "temp_voice.ogg"
    await voice_file.download_to_drive(file_path)
    
    # 2. Send to Groq Whisper for transcription
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
            response_format="text",
        )
    
    # 3. Process the transcribed text through your 'brain'
    ai_response = ask_brain(f"The user sent a voice message saying: '{transcription}'. Please respond.")
    await update.message.reply_text(f"📝 Transcribed: \"{transcription}\"\n\n🤖 {ai_response}")
    
    # Cleanup
    os.remove(file_path)


if __name__ == '__main__':

    # Start FastAPI in a separate thread
    Thread(target=run_fastapi, daemon=True).start()

    # Start Telegram Bot
    bot_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Schedule the morning briefing task
    job_queue = bot_app.job_queue
    sa_tz = pytz.timezone('Africa/Johannesburg')
    # Run every day at 5:00 AM in your timezone
    job_queue.run_daily(
        morning_briefing, 
        time=time(hour=5, minute=0, tzinfo=sa_tz)
    )


    # Register handlers
    bot_app.add_handler(CommandHandler("ping", ping))
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot is thinking... (Polling)")
    bot_app.run_polling()
