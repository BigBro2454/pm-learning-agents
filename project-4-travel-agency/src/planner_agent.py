from google import genai
from google.genai import types
from src.tools import search_flights, search_hotels, search_activities
from src.config import MODEL_NAME

class PlannerAgent:
    """
    Agent A: The Travel Planner.
    Goal: Create the best possible travel itinerary.
    Personality: Optimistic, luxurious, wants the best experience.
    """
    def __init__(self, client: genai.Client):
        self.client = client
        self.system_instruction = (
            "You are a Travel Planner. Your goal is to create the best, most appealing itinerary possible.\n"
            "You have access to tools to search for flights, hotels, and activities.\n"
            "You must propose a complete itinerary formatted clearly, including the flight, hotel, and activities.\n"
            "IMPORTANT: Always provide a JSON representation of the chosen itinerary at the very end of your message.\n"
            "The JSON must be enclosed in ```json ... ``` and have the exact keys:\n"
            '{"flight_id": "F1", "hotel_id": "H1", "nights": <integer>, "activity_ids": ["A1", "A2"]}\n'
            "If the Accountant critiques your proposal because it is over budget, you must read their feedback and revise your itinerary to be cheaper (e.g. choose a budget flight or hotel, or remove activities).\n"
            "Always explain why your itinerary is fantastic!"
        )
        
        # We use a chat session to maintain conversation context (this provides Autonomy and Memory within the agent itself)
        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=[search_flights, search_hotels, search_activities],
                temperature=0.7, # Higher temperature for more creativity
            )
        )

    def propose_itinerary(self, request: str, previous_critique: str = None) -> str:
        """
        Generate a proposal based on the initial request and any feedback from the Accountant.
        """
        prompt = request
        if previous_critique:
            prompt = (
                f"The accountant rejected your previous proposal with this feedback:\n"
                f"'{previous_critique}'\n"
                f"Please search for cheaper alternatives and revise your itinerary."
            )
        
        # The SDK will automatically handle tool calls during this send_message
        response = self.chat.send_message(prompt)
        return response.text
