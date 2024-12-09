import tweepy
import os
from dotenv import load_dotenv
from utils.logger import log_message
from content_generator import generate_content
import time

load_dotenv

t_api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
user_id = os.getenv("USER_ID")

REPLIED_IDS_FILE = "replied_mentions.txt"
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=t_api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
#Load replied IDs from a file.
def load_replied_ids():
    if os.path.exists(REPLIED_IDS_FILE):
        with open(REPLIED_IDS_FILE, "r") as file:
            return set(line.strip() for line in file)
    return set()

#Save a replied ID to a file.
def save_replied_id(mention_id):
    with open(REPLIED_IDS_FILE, "a") as file:
        file.write(f"{mention_id}\n")

#Fetch mentions, check for unreplied ones, and reply.
def reply_to_mentions():
    try:
        replied_ids = load_replied_ids()
        print(f"here is replied ids: {replied_ids}")
        mentions = client.get_users_mentions(id=user_id, tweet_fields=["text", "author_id"])
        if mentions.data:
            for mention in mentions.data:
                mention_id = mention.id
                author_id = mention.author_id
                mention_text = mention.text
                if mention_id in replied_ids:
                    print(f"Already replied to mention ID: {mention_id}")
                    log_message(f"Skipped replying to already processed mention ID: {mention_id}")
                    continue

                prompt = f"Reply to this tweet: '{mention_text}'"
                response_text = generate_content(prompt)
                print(f"Generated reply: {response_text}")
                client.create_tweet(
                    text=response_text,
                    in_reply_to_tweet_id=mention_id
                )
                print(f"Replied to mention ID: {mention_id}")
                log_message(f"Successfully replied to mention ID: {mention_id}, Author ID: {author_id}, " f"Reply: {response_text}")
                save_replied_id(mention_id)
        else:
            print("No mentions found.")
            log_message("No mentions found to reply to.")
    
    except tweepy.TweepyException as e:
        print(f"Tweepy API Error: {e}")
        log_message(f"Tweepy API Error: {e}")

def post_to_twitter(content):
    try:
        response = client.create_tweet(text=content)
        log_message(f"Successfully posted to Twitter : {response.data['id']}")
        time.sleep(900)  # Wait for 60 seconds
        reply_to_mentions()
        print(f"reply_to_mentions() function is called")
    except tweepy.TweepyException as e:
        print(f"Error: {e}")
        log_message(f"Error posting to Twitter: {e}")
