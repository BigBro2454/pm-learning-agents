from google import genai
from google.genai import types
from src.tools import calculate_total
from src.config import MODEL_NAME

class AccountantAgent:
    """
    Agent B: The Accountant.
    Goal: Ensure the itinerary stays within the budget.
    Personality: Pragmatic, budget-focused, strict.
    """
    def __init__(self, client: genai.Client, budget: float):
        self.client = client
        self.budget = budget
        self.system_instruction = (
            f"You are a strict Travel Accountant. The absolute maximum budget for the trip is ${self.budget}.\n"
            "You receive travel proposals from the Planner. The proposal will include a JSON block at the end with the chosen items.\n"
            "Extract the JSON and use the calculate_total tool with that JSON string to find the exact total cost.\n"
            "If the total cost is less than or equal to the budget, you MUST approve the itinerary. Say 'APPROVED' prominently at the beginning of your message.\n"
            "If the total cost is strictly greater than the budget, you MUST critique the proposal. Tell the planner exactly how much they are over budget and suggest what they could cut (e.g., choose a cheaper hotel, downgrade the flight, or remove some activities).\n"
            "Do NOT approve if it is over budget. Do NOT critique if it is under or equal to the budget."
        )
        
        # We use a chat session here as well to maintain history of what we've reviewed
        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=[calculate_total],
                temperature=0.2, # Lower temperature for analytical strictness
            )
        )

    def review_proposal(self, proposal: str) -> str:
        """
        Review the planner's proposal, calculate costs, and return either an approval or a critique.
        """
        prompt = (
            f"Please review this proposal from the planner and check if it fits our budget of ${self.budget}.\n"
            f"Proposal:\n{proposal}"
        )
        # The SDK will automatically call calculate_total based on the tools provided
        response = self.chat.send_message(prompt)
        return response.text
