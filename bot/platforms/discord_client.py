import discord
import os
from ..utils.logger import bot_logger

class DiscordClient:
    def __init__(self):
        self.token = os.getenv('DISCORD_TOKEN')
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
        self.client = discord.Client(intents=discord.Intents.default())

    async def post_content(self, content):
        try:
            await self.client.wait_until_ready()
            channel = self.client.get_channel(self.channel_id)
            message = await channel.send(content)
            
            extra = {
                'tweet_id': str(message.id),
                'type': 'post',
                'content': content,
                'content_link': message.jump_url
            }
            bot_logger.info('Posted to Discord', extra=extra)
            return message.id
        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error posting to Discord: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('Discord posting error', extra=extra)
            return None

    def start(self):
        self.client.run(self.token)