import os
from datetime import datetime

# Import components
from .planner import generate_plan, update_plan
from .searcher import search_web
from .synthesizer import summarize_findings, generate_final_report
from .verifier import verify_completeness
from .memory import log_run

def run_research_agent(query: str, max_iterations: int = 3):
    """
    Main orchestration loop for the Deep Researcher agent.
    Follows the 5-Phase Lifecycle: Task Reception -> Planning -> Execution Loop -> Verification -> Delivery
    """
    print("="*50)
    print(f"🚀 Starting Deep Research on: '{query}'")
    print("="*50)
    
    # Phase 2: Planning (Goal Decomposition)
    print("\n--- PHASE 2: PLANNING ---")
    plan = generate_plan(query)
    
    iteration = 0
    is_complete = False
    
    # Phase 3 & 4: Execution Loop & Verification
    while iteration < max_iterations and not is_complete:
        iteration += 1
        print(f"\n--- PHASE 3: EXECUTION LOOP (Iteration {iteration}/{max_iterations}) ---")
        
        # Execute pending tasks in the plan
        for idx, task in enumerate(plan):
            if task["status"] == "pending":
                print(f"\n>> Executing Subtask: {task['subtask']}")
                
                # Perform searches for this subtask
                all_results = []
                for search_query in task.get("search_queries", []):
                    results = search_web(search_query)
                    all_results.extend(results)
                
                # Synthesize the findings from search results
                findings_summary = summarize_findings(task["subtask"], all_results)
                print(f"   Findings: {findings_summary[:100]}...")
                
                # Update the plan with the new findings
                update_plan(plan, idx, findings_summary, status="completed")
                
        # Phase 4: Verification
        print("\n--- PHASE 4: VERIFICATION ---")
        verification_result = verify_completeness(query, plan)
        
        is_complete = verification_result["is_complete"]
        missing_aspects = verification_result.get("missing_aspects", [])
        
        if not is_complete and missing_aspects:
            print(">> Gaps identified. Dynamically re-planning...")
            # Add missing aspects as new pending subtasks to the plan
            for aspect in missing_aspects:
                plan.append({
                    "subtask": aspect,
                    "status": "pending",
                    "search_queries": [aspect], # Simplified search query generation for missing aspects
                    "findings": ""
                })
        else:
            is_complete = True
            
    if not is_complete:
        print(f"\n[Warning] Reached max iterations ({max_iterations}) before full completion.")
        
    # Phase 5: Delivery
    print("\n--- PHASE 5: DELIVERY ---")
    final_report = generate_final_report(query, plan)
    
    # Save report to file
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_report)
        
    print(f"✅ Final report saved to: {filepath}")
    
    # Log to episodic memory
    log_run(query, plan, {"status": "success", "iterations": iteration}, final_report)
    
    print("="*50)
    print("🎉 Research Complete!")
    print("="*50)
    
if __name__ == "__main__":
    import sys
    
    # Simple CLI interface
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter a research topic: ")
        
    if user_query.strip():
        run_research_agent(user_query)
    else:
        print("No query provided. Exiting.")
