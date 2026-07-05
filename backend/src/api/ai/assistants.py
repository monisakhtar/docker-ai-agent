from .llm import get_openai_client
from .tools import (
    send_me_email,
    get_unread_emails,
)

EMAIL_TOOLS = {
    "send_me_email": send_me_email,
    "get_unread_emails": get_unread_emails,
}

def email_assistant(query: str) -> str:
    llm_client = get_openai_client()
    llm  = llm_client.bind_tools(list(EMAIL_TOOLS.values()))
    message =[
            (
                "system",
                "You are a helpful assistant for managing my emails."
            ),
            ("human",f"{query}")
        ]
    response = llm.invoke(message)
    message.append(("assistant", response.content))

    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call.get("tool_name")
            tool_args = tool_call.get("tool_args")
            tool_func = EMAIL_TOOLS.get(tool_name)
            if not tool_func:
                continue
            tool_response = tool_func.invoke(**tool_args)
            message.append(tool_response)
        final_response = llm.invoke(message)
        return final_response
    return response  