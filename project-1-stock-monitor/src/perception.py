import feedparser
from typing import List
from dataclasses import dataclass
import time

@dataclass
class Article:
    """Standardized representation of a perceived item."""
    title: str
    summary: str
    url: str
    source: str
    timestamp: str

class RSSPerception:
    def __init__(self, feeds: List[str]):
        """
        Initializes the perception layer with a list of RSS feeds to monitor.
        """
        self.feeds = feeds

    def fetch_articles(self) -> List[Article]:
        """
        Fetches and parses articles from all configured RSS feeds.
        Converts the noisy external data into standard `Article` objects.
        """
        articles = []
        for feed_url in self.feeds:
            try:
                # Parse the RSS feed
                feed = feedparser.parse(feed_url)
                
                # Check for errors in parsing
                if feed.bozo and getattr(feed.bozo_exception, 'getMessage', None):
                    print(f"Warning: Issue parsing feed {feed_url} - {feed.bozo_exception.getMessage()}")
                    continue

                source_title = feed.feed.title if 'title' in feed.feed else feed_url

                for entry in feed.entries:
                    # Safely extract fields with defaults
                    title = entry.title if 'title' in entry else 'No Title'
                    summary = entry.summary if 'summary' in entry else 'No Summary'
                    url = entry.link if 'link' in entry else ''
                    
                    # Try to get a timestamp
                    if 'published' in entry:
                        timestamp = entry.published
                    elif 'updated' in entry:
                        timestamp = entry.updated
                    else:
                        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    
                    if not url:
                        continue # Skip articles without a URL, as we need it for deduplication

                    articles.append(Article(
                        title=title,
                        summary=summary,
                        url=url,
                        source=source_title,
                        timestamp=timestamp
                    ))
            except Exception as e:
                print(f"Error fetching from {feed_url}: {e}")
        
        return articles
