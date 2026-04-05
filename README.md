# 🏠 Family Brain: Telegram AI Assistant

A lightweight, private Telegram bot designed to act as a central "knowledge hub" for a household. It uses **RAG (Retrieval-Augmented Generation)** to answer questions about family schedules, home maintenance, and internal FAQs using **Groq (Llama 3)** for near-instant AI responses.

## 🚀 Features

- **Private Access:** Only users with whitelisted Telegram IDs can interact with the bot.
- **Family Knowledge (RAG):** Answers questions based on a local `knowledge.txt` file (Wi-Fi, birthdays, house rules).
- **AI Brain:** Powered by Groq/Llama 3 for natural, helpful conversations.
- **Asynchronous:** Built on `python-telegram-bot` for fast, non-blocking performance.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** [python-telegram-bot](https://github.com)
- **LLM Provider:** [Groq Cloud](https://groq.com) (Llama 3)
- **Environment:** `python-dotenv` for secret management

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd family-house-brain-bot
   ```
