import google.generativeai as genai

genai.configure(api_key="IzaSyB0B_5nh6l119AvObrLUs90rU6yIa9ZRh4")
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_log_llm(log_text: str):

    prompt = f"""
You are ErrorDNA, an intelligent log analysis system.

Analyze the following log and produce a clean, professional, human-readable summary with the following sections:

### Log Type
(what kind of log this is)

### Detected Patterns
(bullet points of unusual patterns)

### Root Cause
(short, clear explanation of the most likely cause)

### Impact
(description of severity and what breaks)

### Recommended Actions
(list of steps to fix the issue)

### Risk Score
(a number from 0–100 describing how dangerous this issue is)

### Meta Summary
- Total lines
- Error count
- Warning count

DO NOT return JSON.
DO NOT wrap in code blocks.
Return clean Markdown text ONLY.

LOG:
{log_text}
"""

    response = model.generate_content(prompt)
    return response.text
