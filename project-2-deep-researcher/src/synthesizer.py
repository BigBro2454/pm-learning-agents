from .config import client, DEFAULT_MODEL

def summarize_findings(subtask: str, search_results: list[dict]) -> str:
    """
    Takes raw search results and uses the LLM to extract key insights relevant to the subtask.
    
    Args:
        subtask: The specific subtask being researched.
        search_results: The list of raw search results (title, snippet, url).
        
    Returns:
        A concise summary of the findings.
    """
    print(f"[Synthesizer] Summarizing findings for subtask: '{subtask}'")
    
    if not search_results:
        return "No relevant information found."
        
    context = ""
    for idx, res in enumerate(search_results):
        context += f"Result {idx+1}:\nTitle: {res.get('title')}\nURL: {res.get('url')}\nSnippet: {res.get('snippet')}\n\n"
        
    prompt = f"""
    You are a research assistant tasked with extracting key insights.
    
    Subtask: "{subtask}"
    
    Search Results:
    {context}
    
    Based on the search results above, write a concise summary (1-3 paragraphs) that directly addresses the subtask.
    Focus on facts, figures, and main points. Do not include introductory filler.
    If the search results do not contain relevant information, state that clearly.
    """
    
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Synthesizer] Error summarizing findings: {e}")
        return "Error occurred during summarization."

def generate_final_report(query: str, plan: list) -> str:
    """
    Generates a final, well-structured markdown report using all the accumulated findings.
    
    Args:
        query: The original user query.
        plan: The completed research plan containing all subtasks and their findings.
        
    Returns:
        A markdown string of the final report.
    """
    print(f"[Synthesizer] Generating final report for query: '{query}'")
    
    compiled_findings = ""
    for item in plan:
        compiled_findings += f"### Subtask: {item['subtask']}\n"
        compiled_findings += f"Findings: {item['findings']}\n\n"
        
    prompt = f"""
    You are an expert report writer.
    
    Original Topic: "{query}"
    
    Compiled Research Findings:
    {compiled_findings}
    
    Your task is to synthesize these findings into a comprehensive, well-structured markdown report.
    The report should include:
    1. A catchy title
    2. An Executive Summary (brief overview)
    3. Detailed sections based on the subtasks (use appropriate headings)
    4. A Conclusion (summarizing the main takeaways)
    
    Format the output as valid Markdown. Make it professional and easy to read.
    """
    
    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Synthesizer] Error generating report: {e}")
        return f"# Error generating report\n\nCould not generate the final report for '{query}'."
