from typing import Optional, Dict, List
import google.generativeai as genai

genai.configure(api_key="AIzaSyB0B_5nh6l119AvObrLUs90rU6yIa9ZRh4")
model = genai.GenerativeModel("gemini-2.5-flash")


def chat_with_gemini(user_query: str, insights: Optional[Dict], history: List) -> str:
    """
    Conversation-aware chatbot.
    Supports both structured insights (dict) and plain-text insights.
    """

    # Build conversation context (last 8 messages)
    conversation_context = ""
    for role, msg in history[-8:]:
        conversation_context += f"{role.upper()}: {msg}\n"

    # ----------------------------
    # FIXED: Handle both dict and str insights
    # ----------------------------
    insights_text = ""

    if insights:
        if isinstance(insights, dict):
            insights_text = f"""
### Log Insights
- Log Type: {insights.get('log_type')}
- Patterns: {insights.get('detected_patterns')}
- Root Cause: {insights.get('root_cause')}
"""
        else:
            # insights is plain-text from LLM
            insights_text = f"""
### Log Insights
{insights}
"""

    # ----------------------------
    # Build prompt
    # ----------------------------
    prompt = f"""
You are ErrorDNA — an intelligent log assistant that can chat naturally AND diagnose logs.

{insights_text}

### Recent Conversation
{conversation_context}

### User Query
{user_query}

### Instructions:
- If user greets (“hi”, “hey”), respond normally.
- If user asks “who are you”, introduce yourself.
- If question is about errors or logs, use the insights.
- Keep replies concise and helpful.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"
