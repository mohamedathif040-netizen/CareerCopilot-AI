import json
import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def analyze_resume(
    resume_text,
    job_description,
    recruiter_mode
):

    prompt = f"""
You are a {recruiter_mode}.

Analyze the resume against the job description.

Generate:

1. LinkedIn connection request to recruiter
2. Cold email to hiring manager
3. Employee referral request

Keep them professional, concise and personalized.

Create a 4-week career improvement roadmap.

Week 1:
Week 2:
Week 3:
Week 4:

Focus on missing skills and interview readiness.


You are an expert AI resume generator. Analyze the user's input and generate an optimized resume.
Focus on missing skills and interview readiness.

Generate the optimized resume using this exact format:

[FULL NAME]
[Email Address] | [Phone Number] | [LinkedIn Profile URL] | [GitHub/Portfolio URL]

SUMMARY
[Professional summary paragraph focusing on target roles]

SKILLS
[Bullet points of technical and soft skills]

PROJECTS
[Project names, tech stacks, and STAR bullet points]

EXPERIENCE
[Work history, roles, and accomplishments]

EDUCATION
[Degrees, institutions, and graduation dates]

CERTIFICATIONS
[Relevant professional certifications]

Formatting Rules:
1. Extract and place the user's name and contact information at the absolute top.
2. Use professional ATS-friendly formatting.
3. Use bullet points where appropriate.
4. Do not include explanations, introductions, or markdown blocks (like ```).
5. Return only the final resume content.


Return ONLY valid JSON.

Format:

{{
  "ats_score": 85,
  "keyword_match": 78,
  "missing_skills": [],
  "interview_probability": 72,
  "roast": "",
  "improvement_plan": "",
  "optimized_resume": "",

  "linkedin_message": "",
  "cold_email": "",
  "referral_request": ""
  "career_roadmap":""
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)