import json
from .config import client, DEFAULT_MODEL

def generate_plan(query: str) -> list[dict]:
    """
    Decomposes a vague user query into a structured research plan.
    Uses the LLM to generate 3-5 concrete subtasks.
    
    Args:
        query: The user's original research question.
        
    Returns:
        A list of subtask dictionaries.
    """
    print(f"[Planner] Decomposing query: '{query}'")
    
    prompt = f"""
    You are an expert research planner. The user wants to research the following topic:
    "{query}"
    
    Your job is to break this broad topic down into 3 to 5 concrete research subtasks.
    Each subtask should focus on a specific aspect of the topic to ensure comprehensive coverage.
    For each subtask, provide 1 or 2 specific search queries that would help gather information about it.
    
    Respond STRICTLY with a JSON array of objects. Do not include markdown formatting like ```json.
    Each object must have the following keys:
    - "subtask": A string describing the specific aspect to research.
    - "search_queries": An array of strings representing search engine queries.
    
    Example response format:
    [
      {{
        "subtask": "Investigate the history of X",
        "search_queries": ["history of X", "origins of X"]
      }},
      {{
        "subtask": "Analyze the impact of X on Y",
        "search_queries": ["X impact on Y", "how X changed Y"]
      }}
    ]
    """
    
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )
        
        # Clean up the response in case the model included markdown blocks
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        raw_plan = json.loads(text.strip())
        
        # Format the plan into the internal structure
        plan = []
        for item in raw_plan:
            plan.append({
                "subtask": item.get("subtask", "Unknown subtask"),
                "status": "pending", # Status can be 'pending', 'in_progress', 'completed'
                "search_queries": item.get("search_queries", []),
                "findings": ""
            })
            
        print(f"[Planner] Generated {len(plan)} subtasks.")
        return plan
        
    except Exception as e:
        print(f"[Planner] Error generating plan: {e}")
        # Fallback plan in case of failure
        return [
            {
                "subtask": f"General overview of {query}",
                "status": "pending",
                "search_queries": [query],
                "findings": ""
            }
        ]

def update_plan(plan: list, subtask_index: int, new_findings: str, status: str = "completed"):
    """
    Updates the plan with new findings and changes the status of a subtask.
    
    Args:
        plan: The current research plan.
        subtask_index: The index of the subtask to update.
        new_findings: The summarized findings to append.
        status: The new status for the subtask.
    """
    if 0 <= subtask_index < len(plan):
        plan[subtask_index]["findings"] += new_findings + "\n"
        plan[subtask_index]["status"] = status
        print(f"[Planner] Updated subtask '{plan[subtask_index]['subtask']}' to status '{status}'.")
