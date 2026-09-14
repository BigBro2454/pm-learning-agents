import os
import sys
from google import genai
from src.config import GEMINI_API_KEY, MAX_ROUNDS
from src.planner_agent import PlannerAgent
from src.accountant_agent import AccountantAgent
from src.conversation import ConversationBuffer
from src.memory import Memory

def main():
    print("✈️ Starting Project 4: Travel Agency (Multi-Agent Debate)")
    
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in .env or environment variables.")
        sys.exit(1)

    # Initialize the Google Gemini GenAI Client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # ---------------------------------------------------------
    # 1. Setup User Request and Constraints
    # ---------------------------------------------------------
    origin = "NYC"
    destination = "TYO"
    duration_nights = 5
    budget = 3000
    
    print(f"\nUser Request: Plan a {duration_nights}-night trip from {origin} to {destination} with a maximum budget of ${budget}.")

    # ---------------------------------------------------------
    # 2. Initialize Agents and Shared Environment
    # ---------------------------------------------------------
    planner = PlannerAgent(client)
    accountant = AccountantAgent(client, budget=budget)
    
    conversation = ConversationBuffer()
    memory = Memory()
    
    # ---------------------------------------------------------
    # 3. Multi-Agent Debate Loop (Orchestrator)
    # ---------------------------------------------------------
    initial_request = (
        f"Plan a {duration_nights}-night trip from {origin} to {destination} for 1 person. "
        f"Make it an amazing experience! Please select a flight, a hotel for {duration_nights} nights, and some activities."
    )
    
    agreement_reached = False
    final_itinerary = ""
    
    for round_num in range(1, MAX_ROUNDS + 1):
        print(f"\n{'='*40}")
        print(f"--- Round {round_num} ---")
        print(f"{'='*40}")
        
        # --- Agent A: Planner Proposes ---
        print("\n🌴 Planner is searching and thinking...")
        last_msg = conversation.get_last_message()
        
        # Check if there is a previous critique from the accountant
        critique = last_msg.content if last_msg and last_msg.msg_type == "critique" else None
        
        try:
            proposal = planner.propose_itinerary(initial_request if round_num == 1 else initial_request, previous_critique=critique)
        except Exception as e:
            print(f"Error during Planner execution: {e}")
            break
            
        # Log the proposal in the conversation buffer and memory
        conversation.add_message(sender="Planner", receiver="Accountant", msg_type="proposal", content=proposal, round_num=round_num)
        memory.add_entry({"round": round_num, "sender": "Planner", "action": "proposal", "content": proposal})
        
        print(f"\n🌴 Planner Proposal:\n{proposal}\n")
        
        # --- Agent B: Accountant Reviews ---
        print("\n💰 Accountant is reviewing and calculating...")
        
        try:
            review = accountant.review_proposal(proposal)
        except Exception as e:
            print(f"Error during Accountant execution: {e}")
            break
        
        # Check if the Accountant approved the proposal
        if "APPROVED" in review.upper():
            msg_type = "approval"
            agreement_reached = True
        else:
            msg_type = "critique"
            
        # Log the review
        conversation.add_message(sender="Accountant", receiver="Planner", msg_type=msg_type, content=review, round_num=round_num)
        memory.add_entry({"round": round_num, "sender": "Accountant", "action": msg_type, "content": review})
        
        print(f"\n💰 Accountant Review:\n{review}\n")
        
        # --- Check for Convergence ---
        if agreement_reached:
            final_itinerary = proposal
            print("\n✅ Agreement reached!")
            break
            
    # ---------------------------------------------------------
    # 4. Final Output and Summary
    # ---------------------------------------------------------
    if not agreement_reached:
        print(f"\n❌ Deadlock: Agents could not reach an agreement within {MAX_ROUNDS} rounds.")
    
    print("\n" + "*"*40)
    print("FINAL OUTPUT")
    print("*"*40)
    if agreement_reached:
        print("\nAgreed Itinerary:\n")
        print(final_itinerary)
    else:
        print("\nNo itinerary agreed upon due to budget constraints.")
        
    print("\n--- Negotiation Summary (Memory Log) ---")
    for entry in memory.get_history():
        print(f"Round {entry['round']} | {entry['sender']} | {entry['action'].upper()}")

if __name__ == "__main__":
    main()
