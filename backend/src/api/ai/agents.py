from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from .llm import get_openai_client

from .tools import (
    send_me_email,
    get_unread_emails,
    research_email
)

EMAIL_TOOLS = [
    send_me_email,
    get_unread_emails,  
]

def get_email_agent():
    model = get_openai_client()
    agent = create_react_agent(
        model=model,
        tools=EMAIL_TOOLS,
        prompts = 'You are a helpful assistant for managing my email inbox for generating, sending and reviewing emails.',
        name = 'email_agent'

    )
    return agent

def get_research_agent():
    model = get_openai_client()
    agent = create_react_agent(
        model=model,
        tools=[research_email],
        prompts = 'You are helpful research assistant for preparing email data',
        name = "research_agent"
    )
    return agent

def get_supervisor():
    llm = get_openai_client()
    email_agent = get_email_agent()
    research_agent = get_research_agent()
    supe = create_supervisor(
        agents = [email_agent, research_agent],
        model = llm,
        prompt=(
            "You manage a research assistant and a"
            "email inbox manager assistant. Assign work to them."
        ),
    ).compile()
    return supe