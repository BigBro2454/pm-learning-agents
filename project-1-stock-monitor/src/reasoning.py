from google import genai
from google.genai import types
from pydantic import BaseModel
import os
from .perception import Article

class RelevanceResult(BaseModel):
    """Structured output expected from the LLM."""
    relevance_score: float
    rationale: str
    is_relevant: bool

class Reasoner:
    def __init__(self, api_key: str, topic: str):
        """
        Initializes the Reasoning layer using the Google GenAI SDK.
        It uses an LLM to evaluate if a perceived article is relevant to the target topic.
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please set it in .env file.")
        
        self.client = genai.Client(api_key=api_key)
        self.topic = topic
        # Use gemini-2.5-flash as it is fast and suitable for basic reasoning tasks
        self.model_name = "gemini-2.5-flash"

    def evaluate_relevance(self, article: Article) -> RelevanceResult:
        """
        Evaluates the relevance of an article to the agent's topic.
        Returns a RelevanceResult containing a score, rationale, and a boolean decision.
        """
        prompt = f"""
        You are an intelligent news filtering agent. Your goal is to determine if a given news article is highly relevant to the topic: "{self.topic}".

        Article Title: {article.title}
        Article Summary: {article.summary}
        Source: {article.source}

        Evaluate the relevance of this article to the topic.
        - relevance_score: A float between 0.0 and 1.0, where 1.0 is extremely relevant and 0.0 is completely irrelevant.
        - rationale: A short, 1-2 sentence explanation of WHY it is or isn't relevant.
        - is_relevant: true if the score is > 0.7, otherwise false.
        """

        try:
            # We use structured outputs to ensure the LLM returns the data in a predictable format
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RelevanceResult,
                    temperature=0.1, # Low temperature for more deterministic reasoning
                ),
            )
            
            # The SDK automatically handles the structured output mapping if we use pydantic/schemas, 
            # but response.text is the JSON string.
            # We can parse it manually or rely on the SDK's built-in conversion if available.
            # Here we parse the JSON string back into our Pydantic model for safety.
            return RelevanceResult.model_validate_json(response.text)

        except Exception as e:
            print(f"Error during reasoning evaluation: {e}")
            # Fallback in case of error: assume irrelevant to prevent spam
            return RelevanceResult(
                relevance_score=0.0,
                rationale=f"Error evaluating relevance: {str(e)}",
                is_relevant=False
            )
