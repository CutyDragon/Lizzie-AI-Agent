from telegram.ext import Application
import os
from ..utils.logger import bot_logger

class TelegramClient:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        self.app = Application.builder().token(self.token).build()

    async def post_content(self, content):
        try:
            message = await self.app.bot.send_message(
                chat_id=self.channel_id,
                text=content
            )
            
            extra = {
                'tweet_id': str(message.message_id),
                'type': 'post',
                'content': content,
                'content_link': f"https://t.me/c/{self.channel_id}/{message.message_id}"
            }
            bot_logger.info('Posted to Telegram', extra=extra)
            return message.message_id
        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error posting to Telegram: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Telegram posting error', extra=extra)
            return None

    async def start(self):
        await self.app.initialize()
        await self.app.start()