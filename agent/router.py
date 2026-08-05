from rag.retriever import retrieve
from rag.prompt_builder import build_prompt

from llm import generate_reply

from agent.tools import (
    github_tool,
    linkedin_tool
)


def execute_action(email, classification):

    tool = classification["tool"]

    # ----------------------------
    # Ignore
    # ----------------------------

    if tool == "ignore":

        return "Email ignored."

    # ----------------------------
    # GitHub
    # ----------------------------

    elif tool == "github":

        return github_tool()

    # ----------------------------
    # LinkedIn
    # ----------------------------

    elif tool == "linkedin":

        return linkedin_tool()

    # ----------------------------
    # RAG
    # ----------------------------

    elif tool == "rag":

        results = retrieve(

            query=email.body,

            category=classification["document_filter"]

        )

        context = "\n\n".join(

            results["documents"][0]

        )

        prompt = build_prompt(

            email,

            context

        )

        return generate_reply(prompt)

    # ----------------------------
    # Direct LLM
    # ----------------------------

    else:

        return generate_reply(email.body)