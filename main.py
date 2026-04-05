# Entry point: Handlers and Bot setup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from brain import ask_brain
from config import TELEGRAM_TOKEN, FAMILY_IDS

# The Ping Command
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
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is thinking... (Polling)")
    app.run_polling()
