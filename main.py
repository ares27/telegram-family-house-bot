# Entry point: Handlers and Bot setup
import os
import uvicorn
from fastapi import FastAPI
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from brain import ask_brain
from config import TELEGRAM_TOKEN, FAMILY_IDS

app = FastAPI()

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
    
    # Call the isolated brain
    response = ask_brain(update.message.text)
    await update.message.reply_text(response)

if __name__ == '__main__':

    # Start FastAPI in a separate thread
    Thread(target=run_fastapi, daemon=True).start()

    # Start Telegram Bot
    bot_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    bot_app.add_handler(CommandHandler("ping", ping))
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is thinking... (Polling)")
    bot_app.run_polling()
