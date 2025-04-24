
```markdown
# **Twitch Clips to Discord**

This project automates the process of retrieving recent Twitch clips from a specific channel and sending them to a Discord channel using a webhook. The script is designed to run daily via GitHub Actions.

---

## **Features**
- Fetches recent Twitch clips from the last 24 hours.
- Sends new clips to a Discord channel via a webhook.
- Tracks already sent clips to avoid duplicates.
- Runs automatically every day using GitHub Actions.

---

## **Requirements**
- Python 3.10 or higher.
- A Twitch account with API credentials.
- A Discord webhook URL.
- GitHub repository with Actions enabled.

---

## **Setup**

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/clip-getter-twitch.git
cd clip-getter-twitch
```

### **2. Install dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **3. Create a `.env` file**
Create a `.env` file in the root directory to store your Twitch and Discord credentials:
```
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_CLIENT_SECRET=your_twitch_client_secret
TWITCH_USERNAME=your_twitch_username
DISCORD_WEBHOOK=your_discord_webhook_url
```

### **4. Run the script locally**
You can test the script locally by running:
```bash
python main.py
```

---

## **GitHub Actions Setup**

### **1. Add secrets to your repository**
Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**, and add the following secrets:
- `TWITCH_CLIENT_ID`
- `TWITCH_CLIENT_SECRET`
- `TWITCH_USERNAME`
- `DISCORD_WEBHOOK`

### **2. Workflow configuration**
The workflow is already configured in `.github/workflows/cron.yml`. It is set to run daily at **15:00 GMT+1** (14:00 UTC). You can modify the schedule by editing the `cron` expression in the workflow file.

---

## **How It Works**

1. The script retrieves recent Twitch clips from the last 24 hours using the Twitch API.
2. It compares the retrieved clips with previously sent clips stored in `clips_sent.json`.
3. New clips are sent to Discord via the webhook.
4. The list of sent clips is updated and stored securely using GitHub Artifacts.

---

## **File Structure**
```
clip-getter-twitch/
├── .github/
│   └── workflows/
│       └── cron.yml          # GitHub Actions workflow
├── data/
│   └── clips_sent.json       # Tracks sent clips (managed by GitHub Artifacts)
├── main.py                   # Main script
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## **Customization**

### **Change the Discord message format**
You can modify the `send_clip_to_discord` function in `main.py` to customize the message sent to Discord:
```python
data = {
    "content": f"🎥 New clip by {clip['broadcaster_name']}!\n{clip['url']}"
}
```

### **Adjust the schedule**
Edit the `cron` expression in `.github/workflows/cron.yml` to change the execution time:
```yaml
schedule:
  - cron: "0 14 * * *" # Runs daily at 14:00 UTC
```

---

## **Contributing**
Feel free to fork this repository and submit pull requests for improvements or new features.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**
- [Twitch API Documentation](https://dev.twitch.tv/docs)
- [Discord Webhooks Documentation](https://discord.com/developers/docs/resources/webhook)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
```
