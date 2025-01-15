import json
import os
import time
from datetime import datetime
import asyncio
from .openai_client import OpenAIClient
from .platforms.twitter_client import TwitterClient
# from .platforms.discord_client import DiscordClient
# from .platforms.telegram_client import TelegramClient
from .utils.logger import bot_logger

class SocialBot:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.twitter_client = TwitterClient()
        # self.discord_client = DiscordClient()
        # self.telegram_client = TelegramClient()
        
        self.reply_tracker_file = 'bot/data/reply_tracker.json'
        self.generated_contents_file = 'bot/data/generated_contents.json'
        self.load_trackers()

    def load_trackers(self):
        os.makedirs('bot/data', exist_ok=True)
        
        try:
            with open(self.reply_tracker_file, 'r') as f:
                content = f.read()
                # Check if file is empty
                self.replied_tweets = json.loads(content) if content else []
        except (FileNotFoundError, json.JSONDecodeError):
            self.replied_tweets = []
            self.save_reply_tracker()

        try:
            with open(self.generated_contents_file, 'r') as f:
                content = f.read()
                # Check if file is empty
                self.daily_contents = json.loads(content) if content else []
        except (FileNotFoundError, json.JSONDecodeError):
            self.daily_contents = []
            self.save_generated_contents()

    def save_reply_tracker(self):
        with open(self.reply_tracker_file, 'w') as f:
            json.dump(self.replied_tweets, f)

    def save_generated_contents(self):
        with open(self.generated_contents_file, 'w') as f:
            json.dump(self.daily_contents, f)

    def generate_daily_contents(self):
        try:
            self.daily_contents = self.openai_client.generate_daily_tweets()
            self.save_generated_contents()
            extra = {
                'tweet_id': 'N/A',
                'type': 'info',
                'content': 'Generated daily contents',
                'content_link': 'N/A'
            }
            bot_logger.info('Generated daily contents', extra=extra)
        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error generating daily contents: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Error generating daily contents', extra=extra)

    async def post_scheduled_content(self, index):
        try:
            if 0 <= index < len(self.daily_contents):
                content = self.daily_contents[index]
                
                # Add debug logging
                extra = {
                    'tweet_id': 'N/A',
                    'type': 'info',
                    'content': f'Posting scheduled content index {index}: {content[:50]}...',
                    'content_link': 'N/A'
                }
                bot_logger.info(f'Posting scheduled content index {index}', extra=extra)
                
                # Post to all platforms
                twitter_id = self.twitter_client.post_content(content)
                # await self.discord_client.post_content(content)
                # await self.telegram_client.post_content(content)
                
                return twitter_id
        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error posting content: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Error posting content', extra=extra)
            return None

    async def check_and_reply_to_comments(self):
        try:
            mentions = self.twitter_client.get_mentions()
            print(f"mentions: {mentions}")
            if not mentions:
                print("No mentions found.")
                return

            for mention in mentions:
                if mention.id not in self.replied_tweets:
                    print(f"mention.id: {mention.id}")
                    print(f"mention.text: {mention.text}")
                    reply_content = self.openai_client.generate_reply(mention.text)
                    print(f"reply_content: {reply_content}")
                    self.twitter_client.reply_to_tweet(mention.id, reply_content)
                    self.replied_tweets.append(mention.id)
                    self.save_reply_tracker()
                    time.sleep(3)

        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error checking replies: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Error checking replies', extra=extra)