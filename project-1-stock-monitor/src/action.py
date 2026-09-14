import requests
from .perception import Article
from .reasoning import RelevanceResult

class ActionSender:
    def __init__(self, discord_webhook_url: str):
        """
        Initializes the Action layer.
        This component is responsible for changing the environment (in this case, sending a notification).
        """
        self.webhook_url = discord_webhook_url

    def send_alert(self, article: Article, relevance: RelevanceResult, topic: str):
        """
        Sends an alert about a relevant article to the configured Discord webhook.
        """
        if not self.webhook_url:
            print(f"[MOCK ALERT - Webhook URL not set]")
            print(f"Topic: {topic}")
            print(f"Title: {article.title}")
            print(f"URL: {article.url}")
            print(f"Relevance: {relevance.relevance_score} - {relevance.rationale}")
            print("-" * 40)
            return

        # Construct the Discord message payload
        embed = {
            "title": article.title,
            "url": article.url,
            "description": article.summary[:500] + "..." if len(article.summary) > 500 else article.summary,
            "color": 3447003, # Blueish color
            "fields": [
                {
                    "name": "Relevance Score",
                    "value": f"{relevance.relevance_score:.2f}",
                    "inline": True
                },
                {
                    "name": "Source",
                    "value": article.source,
                    "inline": True
                },
                {
                    "name": "Agent Rationale",
                    "value": relevance.rationale
                }
            ],
            "footer": {
                "text": f"Detected at {article.timestamp}"
            }
        }

        payload = {
            "content": f"🚨 **New Relevant Article Detected for Topic: {topic}**",
            "embeds": [embed]
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            print(f"Successfully sent alert for: {article.title}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send alert via Discord webhook: {e}")
