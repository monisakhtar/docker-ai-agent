from langchain_core.tools import tool
from .myemailer.sender import send_email
from .myemailer.inbox_reader import read_inbox
from .services import generate_email

@tool
def research_email(query:str):
    """
    Perform research based on the query

    Arguments:
    - query: str - Topic of research
    """
    response = generate_email(query)
    msg = f'Subject {response.subject}:\nBody: {response.content}'
    return msg 


@tool
def send_me_email(subject: str, content: str, to_email: str) -> str:
    """
    Send an email with the given subject and content.
    Args:
        subject (str): The subject of the email.
        content (str): The content/body of the email.
        to_email (str): The email address of the recipient.

    Returns:
        str: A message indicating the success or failure of the email sending operation.
    """
    try:
        send_email(subject, content, to_email)
        return f"Email sent successfully with subject: '{subject}'"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
    
@tool
def get_unread_emails(hours_ago:int=48) -> str:
    """
    Read all emails from my inbox within the last N hours

    Arguments:
    - hours_ago: int = 24 - number of hours ago to retrieve in the inbox
    
    Returns:
    A string of emails separated by a line "----"
    """
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except Exception as e:
        return f"Error getting latest emails: {str(e)}"
    cleaned = []
    for email in emails:
        data = email.copy()
        if "html_body" in data:
            data.pop('html_body')
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t{v}"
        cleaned.append(msg)
    return "\n-----\n".join(cleaned)[:500]