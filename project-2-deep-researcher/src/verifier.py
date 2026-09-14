import json
from .config import client, DEFAULT_MODEL

def verify_completeness(query: str, plan: list) -> dict:
    """
    Evaluates whether the research comprehensively answers the original query based on current findings.
    
    Args:
        query: The original user query.
        plan: The current research plan with findings.
        
    Returns:
        A dictionary with 'is_complete' (boolean) and 'missing_aspects' (list of strings/subtasks if incomplete).
    """
    print(f"[Verifier] Verifying completeness for query: '{query}'")
    
    compiled_findings = ""
    for item in plan:
        compiled_findings += f"Subtask: {item['subtask']}\n"
        compiled_findings += f"Findings: {item['findings']}\n\n"
        
    prompt = f"""
    You are a meticulous research verifier.
    
    Original Topic/Query: "{query}"
    
    Current Research Findings:
    {compiled_findings}
    
    Your job is to determine if the original topic has been comprehensively covered by the current findings.
    Ask yourself: "Are there any obvious gaps or important aspects of the original query that haven't been addressed?"
    
    Respond STRICTLY with a JSON object. Do not include markdown formatting like ```json.
    The JSON object must have these keys:
    - "is_complete": a boolean (true if the research is sufficient, false if major gaps exist).
    - "missing_aspects": a list of strings. If "is_complete" is false, list 1 to 3 specific subtasks that need to be researched to fill the gaps. If true, this should be an empty list.
    
    Example response (if complete):
    {{"is_complete": true, "missing_aspects": []}}
    
    Example response (if incomplete):
    {{"is_complete": false, "missing_aspects": ["Investigate the economic impact of X", "Compare X with alternative Y"]}}
    """
    
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )
        
        # Clean up response
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        result = json.loads(text.strip())
        
        is_complete = result.get("is_complete", True)
        missing_aspects = result.get("missing_aspects", [])
        
        if is_complete:
            print("[Verifier] Verification passed. Research is complete.")
        else:
            print(f"[Verifier] Verification failed. Missing aspects: {missing_aspects}")
            
        return {
            "is_complete": is_complete,
            "missing_aspects": missing_aspects
        }
        
    except Exception as e:
        print(f"[Verifier] Error during verification: {e}. Assuming complete to avoid infinite loop.")
        return {"is_complete": True, "missing_aspects": []}
