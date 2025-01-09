from openai import OpenAI
import base64
import logging
import praw
import time
# Initialize OpenAI Client
client = OpenAI(api_key="")

# Reddit Bot Credentials
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
    username="",
    password=""
)
logging.basicConfig(
    filename="reddit_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# Subreddits to monitor
subreddits_to_monitor = ["Fitness_India", "Fitness", "careerguidance"]
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
                "content": (
                    "You are a cool bro who helps people with their fitness, career, and life advice. "
                    "Your replies are short (1-2 sentences, max_token = 150), funny, and sarcastic sometimes. "
                    "Sometimes you motivate users, sometimes you demotivate them while still being motivating, "
                    "and sometimes you're brutally honest to give them a reality check if they're being unrealistic. "
                    "You can be rude, angry, or kind depending on the situation, but you always deliver advice like a chill, confident bro."
                )
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
                logging.error(f"Error generating response: {e}")
                break

            logging.error(f"Error generating response: {e}")

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
