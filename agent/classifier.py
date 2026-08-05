import os
import json

from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI email classification engine.

Your job is to analyze incoming emails and classify them.

Return ONLY valid JSON.

Categories:
- recruiter
- interview
- follow_up
- personal
- spam
- newsletter
- other

Definitions:

recruiter:
Job opportunities, HR outreach, hiring manager,
talent acquisition, resume requests, hiring discussion.

interview:
Interview invitation, interview scheduling,
technical assessment, coding round,
online assessment.

follow_up:
Recruiter requesting additional information,
documents,
resume update,
salary expectation,
availability,
notice period.

personal:
Friends, family or personal communication.

newsletter:
Marketing emails,
subscriptions,
company announcements,
promotional content.

spam:
Scam,
phishing,
fraud,
fake offers,
malicious content.

other:
Anything that doesn't fit above.

Return ONLY JSON in this format:

{
    "category":"recruiter",
    "intent":"project_question",
    "tool":"rag",
    "document_filter":"projects",
    "confidence":0.98,
    "reason":"Recruiter is asking about projects."
}

Rules:

tool values:

rag
github
linkedin
resume
ignore
llm

document_filter values:

projects
skills
education
profile
resume
github
linkedin
general

Never explain your answer.

Never return markdown.

Never return extra text.

Only JSON.
"""


def classify_email(subject: str, body: str):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0,

        response_format={
            "type": "json_object"
        },

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": f"""
Subject:
{subject}

Body:
{body}
"""
            }

        ]

    )

    try:

        return json.loads(
            response.choices[0].message.content
        )

    except Exception:

        return {

            "category": "other",

            "intent": "unknown",

            "tool": "llm",

            "document_filter": "general",

            "confidence": 0.0,

            "reason": "Unable to classify email."

        }


if __name__ == "__main__":

    result = classify_email(

        subject="Machine Learning Engineer Opportunity",

        body="""
Hi Sharath,

We came across your LinkedIn profile.

We are hiring an AI/ML Engineer at Microsoft.

Would you be interested in discussing this opportunity?

Regards,
Talent Acquisition
"""

    )

    print(json.dumps(result, indent=4))