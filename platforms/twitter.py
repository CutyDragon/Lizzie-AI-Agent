import tweepy
import os
from dotenv import load_dotenv
from utils.logger import log_message
from content_generator import generate_content
import time
from datetime import datetime, timedelta

load_dotenv()

t_api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
# user_id = os.getenv("USER_ID")

REPLIED_IDS_FILE = "replied_mentions.txt"

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=t_api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
# Get current time
end_time = datetime.utcnow()
# Get time 7 days ago
start_time = end_time - timedelta(days=1)

# Format dates in ISO 8601 format as required by Twitter API
start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
print(f"Start time: {start_time}, End time: {end_time}")

def load_replied_ids():
    if os.path.exists(REPLIED_IDS_FILE):
        with open(REPLIED_IDS_FILE, "r") as file:
            return set(line.strip() for line in file)
    return set()

def save_replied_id(mention_id):
    with open(REPLIED_IDS_FILE, "a") as file:
        file.write(f"{mention_id}\n")

def reply_to_mentions():
    try:
        replied_ids = load_replied_ids()
        print(f"Here are the replied IDs: {replied_ids}")
        my_user = client.get_me()
        user_id = my_user.data.id
        mentions = client.get_users_mentions(
            id=user_id, 
            tweet_fields=["text", "author_id", "created_at", "public_metrics"],
            start_time=start_time,
            end_time=end_time
        )
        print(f"Here are the replied IDs: {mentions}")

        if mentions.data:
            for mention in mentions.data:
                mention_id = mention.id
                author_id = mention.author_id
                mention_text = mention.text
                if str(mention_id) in replied_ids:
                    print(f"Already replied to mention ID: {mention_id}")
                    log_message("INFO", f"Skipped replying to already processed mention ID: {mention_id}")
                    continue

                prompt = f"Reply to this tweet: '{mention_text}'"
                print(f"Generating prompt for mention ID: {prompt}")
                response_text = generate_content(prompt)
                print(f"Generated reply for {mention_id} : {response_text}")
                client.create_tweet(
                    text=response_text,
                    in_reply_to_tweet_id=mention_id
                )
                print(f"Replied to mention ID: {mention_id}")
                log_message("SUCCESS", f"Successfully replied to mention ID: {mention_id}, Author ID: {author_id}, Reply: {response_text}")
                save_replied_id(str(mention_id))
        else:
            print("No mentions found.")

    except tweepy.TweepyException as e:
        print(f"Tweepy API Error: {e}")
        log_message("ERROR", f"Tweepy API Error: {e}")

def post_to_twitter(content):
    try:
        # my_user = client.get_me()
        # user_id = my_user.data.id
        response = client.create_tweet(text=content)
        log_message("SUCCESS", f"Successfully posted to Twitter\t: Twitter ID: {response.data['id']} : Twitter Content: {content}")
        time.sleep(60)
        reply_to_mentions()
    except tweepy.TweepyException as e:
        print(f"Error: {e}")
        log_message("ERROR", f"Error posting to Twitter: {e}")
