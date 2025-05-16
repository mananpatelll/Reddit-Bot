# Reddit Bot Setup Guide

## Requirements

* Python 3.7+
* An OpenAI API key
* Reddit API credentials (client ID, secret, username, password, user agent)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/reddit-bot.git
   cd reddit-bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Open the Python file** (e.g., `main.py`) and fill in your credentials in the respective fields:

   ```python
   client = OpenAI(api_key="your_openai_key")

   reddit = praw.Reddit(
       client_id="your_client_id",
       client_secret="your_client_secret",
       user_agent="your_user_agent",
       username="your_reddit_username",
       password="your_reddit_password"
   )
   ```

4. **Run the bot:**

   ```bash
   python main.py
   ```


* Ensure your Reddit account has API access via [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
