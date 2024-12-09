from content_generator import generate_content
from platforms.twitter import post_to_twitter
from platforms.discord import post_to_discord
from utils.scheduler import schedule_posts
from utils.logger import log_message

prompt = "Write a financial tweet that captures your best financial perspective in 40 words or less."

def post_task():
    content = generate_content(prompt)
    print(f"{content}")
    
    # Log content generation
    log_message(f"Generated content from openai: {content}")
    
    # Post to Twitter
    post_to_twitter(content)
    
    # Post to Discord
    post_to_discord(content)
   
# Schedule the posts
# post_task()
schedule_posts(post_task, interval_hours=1)
log_message("Post scheduler started.")