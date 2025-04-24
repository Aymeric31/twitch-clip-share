import requests
import json
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Twitch API credentials
TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")
TWITCH_USERNAME = os.environ.get("TWITCH_USERNAME")

# Discord Webhook URL
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# JSON file to store sent clips
CLIPS_LOG_FILE = "./data/clips_sent.json"

# Retrieve a Twitch access token
def get_twitch_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

# Retrieve recent clips from a Twitch channel
def get_recent_clips(access_token):
    url = f"https://api.twitch.tv/helix/clips"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    # Define the parameters for the API request
    params = {
        "broadcaster_id": get_broadcaster_id(access_token),  # Get the broadcaster ID for the specified Twitch username
        "started_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()  # Retrieve clips from the last 24 hours
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]

# Get the broadcaster ID using the Twitch API
def get_broadcaster_id(access_token):
    url = f"https://api.twitch.tv/helix/users"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {"login": TWITCH_USERNAME}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"][0]["id"]

# Load sent clips from the JSON file
def load_sent_clips():
    if not os.path.exists(CLIPS_LOG_FILE):
        return []
    with open(CLIPS_LOG_FILE, "r") as file:
        clips = json.load(file)
    # Return only the IDs of the clips
    return [clip["id"] for clip in clips]

# Save sent clips to the JSON file if they are new
def save_sent_clips_if_new(clips):
    # Sort clips by their ID to ensure consistent order
    clips_sorted = sorted(clips, key=lambda clip: clip["id"])
    existing_clips = load_sent_clips()
    existing_clips_sorted = sorted(existing_clips, key=lambda clip: clip["id"])

    # Save only if the sorted lists are different
    if clips_sorted != existing_clips_sorted:
        with open(CLIPS_LOG_FILE, "w") as file:
            json.dump(clips_sorted, file, indent=4, ensure_ascii=False)
        print("Clips log updated.")
    else:
        print("No new clips to update.")

# Send a clip to Discord via a webhook
def send_clip_to_discord(clip):
    data = {
        "content": f"🎥 Nouveau clip créé par {clip['broadcaster_name']}!\n{clip['url']}"
    }
    response = requests.post(f"https://discord.com/api/webhooks/{DISCORD_WEBHOOK}", json=data)
    response.raise_for_status()

def main():
    access_token = get_twitch_access_token()
    recent_clips = get_recent_clips(access_token)
    sent_clips = load_sent_clips()
    new_clips = [clip for clip in recent_clips if clip["id"] not in sent_clips]

    # Check if there are new clips
    if not new_clips:
        print("No new clips to send.")
        return

    # Send new clips to Discord
    for clip in new_clips:
        send_clip_to_discord(clip)

    save_sent_clips_if_new(recent_clips)

if __name__ == "__main__":
    main()