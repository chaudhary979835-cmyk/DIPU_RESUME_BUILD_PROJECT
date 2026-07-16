from openai import OpenAI
import json

client = OpenAI()

def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's goal,

User goal: "{user_goal}"
    
STRICT RULES:
- Extractonly relevent skills for this goal
-REMOVE irrelevent tools [exec for backed,etc]
-Identify real gaps
-Generate roadmap only for missing fields
-Make output DIFFERENT based on goal

Return only JSON:
{{
"skills":[],
"missing_skills":[],
"roadmap":[],
"interview_questions":[]

}}
Resume:
{resume_text}

"""
    try:
        response = client.chat.completions.create{
            model = "gpt-4.1-mini",
            temperature = 0.3,
            messages = [
                {"role":"system","content":"You're a strict hirict manger,"}
                {"role":"user","content":prompt}
            ]

        }
        content = response.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("{")

        return json.loads(content[start:end])
    except Exception as e :
        return {
            "skills":[],
            "missing_skills":[],
            "roadmap":[],
            "interview_questions":[],
            "error":str(e)
        }