from openai import OpenAI
import base64
import logging
import praw
import time
from dotenv import load_dotenv
import os

load_dotenv()
# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Reddit Bot Credentials
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

system_prompt = os.getenv("BOT_SYSTEM_PROMPT")
if not system_prompt:
    raise ValueError("BOT_SYSTEM_PROMPT is not set in the environment.")


logging.basicConfig(
    filename="reddit_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# Subreddits to monitor
subreddits_to_monitor = ["Fitness", "careerguidance"]  # add subreddits here
subreddit = reddit.subreddit("+".join(subreddits_to_monitor))


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to generate OpenAI responses


def generate_openai_response(prompt, image_url=None):
    try:
        # Prepare messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": system_prompt

            },
            {"role": "user", "content": prompt}
        ]

        # Add image to messages if available
        if image_url:
            messages.append(
                {
                    "role": "user",
                    "content": f"{image_url}"
                }
            )
        # Generate a response using OpenAI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return -1


# Monitor and reply to new posts
replied_posts = set()

for submission in subreddit.stream.submissions(skip_existing=True):
    if submission.id not in replied_posts:
        try:
            logging.info(
                f"New post found: Title: {submission.title} | Subreddit: {submission.subreddit.display_name}")

            # Check if the post contains an image
            image_url = None
            if submission.url and submission.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                image_url = submission.url

            # Create a prompt based on the post title and content
            word_count = len(submission.selftext.split())
            if word_count > 200:
                logging.info(
                    f"Skipping post due to length: {submission.title} ({word_count} words)")
                continue

            prompt = f"Respond to this Reddit post:\n\nTitle: {submission.title}\n\nContent: {submission.selftext}"

            # Generate a reply using OpenAI
            reply = generate_openai_response(prompt, image_url=image_url)
            if reply == -1:
                logging.error("OpenAI failed to generate a reply.")
                break

            # Post the reply on Reddit
            submission.reply(reply)
            logging.info(
                f"--------------------------------------------------------------------------------------------------------------")

            # Track replied posts
            replied_posts.add(submission.id)
        except Exception as e:
            logging.error(f"Error replying to post: {e}")

        # Avoid hitting Reddit's rate limits
    time.sleep(60)
