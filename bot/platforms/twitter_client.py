import tweepy
import os
import datetime
from ..utils.logger import bot_logger

class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token = os.getenv("X_BEARER_TOKEN"),
            consumer_key=os.getenv('X_API_KEY'),
            consumer_secret=os.getenv('X_API_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET')
        )
        self.start_time = datetime.datetime.now() - datetime.timedelta(days=3)
        self.end_time = datetime.datetime.now()


    def post_content(self, content):
        try:
            response = self.client.create_tweet(text=content)
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"
            
            extra = {
                'tweet_id': tweet_id,
                'type': 'post',
                'content': content,
                'content_link': tweet_url
            }
            bot_logger.info('Posted to Twitter', extra=extra)
            return tweet_id
        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error posting to Twitter: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Twitter posting error', extra=extra)
            return None

    def reply_to_tweet(self, tweet_id, content):
        try:
            response = self.client.create_tweet(
                text=content,
                in_reply_to_tweet_id=tweet_id
            )
            reply_id = response.data['id']
            reply_url = f"https://twitter.com/user/status/{reply_id}"
            
            extra = {
                'tweet_id': reply_id,
                'type': 'reply',
                'content': content,
                'content_link': reply_url
            }
            bot_logger.info('Posted reply to Twitter', extra=extra)
            return reply_id
        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error replying on Twitter: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Twitter reply error', extra=extra)
            return None

    def get_mentions(self):
        try:
            user_id = os.getenv('X_USER_ID')
            print("get_users_mentions() is called.")
            response = self.client.get_users_mentions(
                id=user_id,
                tweet_fields=['created_at', 'text'],
                start_time=self.start_time,
                end_time=self.end_time,
                max_results=100,
                expansions=['author_id']
            )

            if not response.data:
                bot_logger.info('No mentions found')
                return []
            
            # Filter out deleted tweets (tweets without text)
            valid_mentions = [tweet for tweet in response.data if hasattr(tweet, 'text')]
            return valid_mentions

        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error getting mentions: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Twitter mentions error', extra=extra)
            return []