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

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables:**

   ```
   Create a .env file in the root directory:

   TELEGRAM_TOKEN=your_telegram_bot_token
   GROQ_API_KEY=your_groq_api_key
   FAMILY_IDS=12345678,87654321
   ```

5. **Initialize Knowledge:**

   ```
   edit  **knowledge.txt**  to include your family-specific information.
   ```

6. **Run the Bot:**
   ```
   python main.py
   ```
