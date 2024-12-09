import requests
import os
from dotenv import load_dotenv
from utils.logger import log_message

load_dotenv()

def post_to_discord(content):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message posted to Discord successfully!")
        log_message(f"Successfully posted to Discord: {content}")
    else:
        print(f"Error posting to Discord: {response.status_code}, {response.text}")
        log_message(f"Error posting to Discord: {response.status_code}, {response.text}")
