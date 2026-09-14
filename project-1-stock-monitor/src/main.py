import time
from .config import Config
from .perception import RSSPerception
from .reasoning import Reasoner
from .memory import MemoryDB
from .action import ActionSender

def main():
    """
    The main Agent Loop.
    This continuous cycle is the heart of an autonomous agent:
    Perceive -> Reason -> Check Memory -> Act -> Store Memory -> Wait -> Repeat
    """
    print(f"Starting Agent for topic: '{Config.TOPIC}'")
    
    # Initialize components
    perception = RSSPerception(Config.RSS_FEEDS)
    try:
        reasoner = Reasoner(Config.GEMINI_API_KEY, Config.TOPIC)
    except ValueError as e:
        print(f"Initialization Error: {e}")
        return
        
    memory = MemoryDB(Config.DB_PATH)
    action = ActionSender(Config.DISCORD_WEBHOOK_URL)

    # Enter the continuous agent loop
    while True:
        print(f"\n--- Starting new cycle at {time.strftime('%X')} ---")
        
        # 1. PERCEIVE: Gather raw data from the environment
        print("Perceiving environment...")
        articles = perception.fetch_articles()
        print(f"Found {len(articles)} total articles across feeds.")

        for article in articles:
            # 2. CHECK MEMORY (early exit): Have we seen this before?
            if memory.is_article_seen(article.url):
                # Skip to avoid duplicated reasoning effort and duplicate alerts
                continue

            # 3. REASON: Is this article relevant to our goals?
            print(f"Evaluating new article: {article.title[:50]}...")
            relevance = reasoner.evaluate_relevance(article)
            
            alert_sent = False
            
            if relevance.is_relevant:
                # 4. ACT: Change the environment by sending a notification
                print(f"-> Highly relevant! Score: {relevance.relevance_score}. Rationale: {relevance.rationale}")
                action.send_alert(article, relevance, Config.TOPIC)
                alert_sent = True
            else:
                print(f"-> Not relevant enough. Score: {relevance.relevance_score}.")

            # 5. STORE MEMORY: Remember we've processed this to avoid infinite loops
            memory.log_article(
                title=article.title, 
                url=article.url, 
                relevance_score=relevance.relevance_score, 
                alerted=alert_sent
            )
            
            # Small delay to avoid hammering the LLM API too quickly in a batch
            time.sleep(1)

        print(f"Cycle complete. Sleeping for {Config.POLL_INTERVAL_SECONDS} seconds...")
        
        # Wait before the next observation cycle
        try:
            time.sleep(Config.POLL_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nAgent loop stopped by user.")
            break

if __name__ == "__main__":
    main()
