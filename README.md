# Reddit Bot Setup Guide

## Requirements

* Python 3.7+
* An OpenAI API key
* Reddit API credentials (client ID, secret, username, password, user agent)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mananpatelll/Reddit-Bot.git
   cd Reddit-Bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the root directory based on the `.env.example` file:**

   ```bash
   cp .env.example .env
   ```

   Then open `.env` and fill in your credentials:

   ```env
   OPENAI_API_KEY=your_openai_key
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   ```

4. **Run the bot:**

   ```bash
   python main.py
   ```

## Notes

* Ensure your Reddit account has API access via [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
