from .llm import get_openai_client

from .schemas import EmailMessageSchema


def generate_email(query: str) -> EmailMessageSchema:
    llm_client = get_openai_client()
    llm = llm_client.with_structured_output_schema(EmailMessageSchema)
    message =[
            (
                "system",
                "You are a helpful assistant that generates email messages based on user queries."
            ),
            (
                "user",
                f"Generate an email message based on the following query: {query}"
            )
        ]

    
    
    return llm.invoke(message)  