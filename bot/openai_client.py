from openai import OpenAI
import os
from dotenv import load_dotenv
from .utils.logger import bot_logger

load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generate_daily_tweets(self):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a financial expert. Generate exactly 6 separate insightful sentences about finance, 
                        markets, or investing. Each sentence must be:
                        1. Under 280 characters
                        2. Cover different topics
                        3. Include relevant facts or statistics
                        4. Be engaging and informative
                        5. End with a clear point or takeaway
                        6. include 1~2 hashtags at the end of each sentence
                        

                        Format: Return exactly 6 lines, one sentence per line."""
                    },
                    {"role": "user", "content": "Generate 6 financial insights."}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Split the response into 6 sentences and clean them
            content = response.choices[0].message.content
            sentences = [s.strip() for s in content.split('\n') if s.strip()]
            print(sentences)
            

            # Ensure we have exactly 6 sentences
            if len(sentences) != 6:
                raise ValueError("OpenAI did not generate exactly 6 sentences")
            
            # Log successful generation
            extra = {
                'tweet_id': 'N/A',
                'type': 'info',
                'content': 'Generated 6 new financial insights',
                'content_link': 'N/A'
            }
            bot_logger.info('Successfully generated daily content', extra=extra)
            
            return sentences

        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error generating daily tweets: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('OpenAI generation error', extra=extra)
            return []

    def generate_reply(self, comment_text):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a financial expert. Generate a helpful and professional reply to a comment.
                        Requirements:
                        1. Keep it under 280 characters
                        2. Be professional and informative
                        3. Address the specific question or comment
                        4. Include factual information when relevant
                        5. Maintain a helpful and educational tone"""
                    },
                    {"role": "user", "content": f"Reply professionally to this comment: {comment_text}"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            reply_content = response.choices[0].message.content.strip()
            
            # Verify reply length
            if len(reply_content) > 280:
                reply_content = reply_content[:277] + "..."
            
            extra = {
                'tweet_id': 'N/A',
                'type': 'info',
                'content': f'Generated reply to: {comment_text[:50]}...',
                'content_link': 'N/A'
            }
            bot_logger.info('Successfully generated reply', extra=extra)
            
            return reply_content

        except Exception as e:
            extra = {
                'tweet_id': 'N/A',
                'type': 'error',
                'content': f'Error generating reply: {str(e)}',
                'content_link': 'N/A'
            }
            bot_logger.error('OpenAI reply generation error', extra=extra)
            return "We apologize, but we're unable to process your request at this time. Please try again later."

    def validate_content(self, content):
        """Utility method to validate content meets requirements"""
        if not content:
            return False
        if len(content) > 280:
            return False
        return True