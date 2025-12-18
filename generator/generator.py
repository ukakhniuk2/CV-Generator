from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def ask_openai(vacancy):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    from .current_cv import current_cv

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are an expert LaTeX CV writer. You MUST output ONLY valid, compilable LaTeX code. Do NOT use markdown code blocks (no ```). Do NOT include any introductory or concluding text. The output must start with \\documentclass and end with \\end{document}. You MUST properly escape all LaTeX special characters (like %, $, &, _, #, ^) in the content text."},
            {"role": "user", "content": f"Here is the candidate's current CV:\n{current_cv}"},
            {"role": "user", "content": f"Please adapt this CV to fit the following job description:\n{vacancy}"},
            {"role": "user", "content": f"Please keep the same style, formatting and length of the document as the current CV."},
            {"role": "user", "content": f"It's VERY IMPORTANT, EVEN CRUCIAL to keep the same length of the document and number of lines in one topic as the current CV, everything should be in one page."},
            {"role": "user", "content": f"Output all text ONLY in english language."}
        ]
    )

    adapted_cv = response.choices[0].message.content
    return adapted_cv

def ask_openai_cover_letter(vacancy, cv):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are an expert cover letter writer. You creating cover letters for job applications. It should be personalized for a vacancy and candidate's CV. It should contain 5-7 sentences about how candidate's experience and skills match the job description, how candidate can be a good fit for the company and how candidate excited to work for the company. Write from the candidate's perspective."},
            {"role": "user", "content": f"Here is the candidate's current CV:\n{cv}"},
            {"role": "user", "content": f"Please adapt this CV to fit the following job description:\n{vacancy}"}
        ]
    )

    cover_letter = response.choices[0].message.content
    return cover_letter
