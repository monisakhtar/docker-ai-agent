from email.mime import base
import os

from langchain_openai import ChatOpenAI

model_name = os.environ.get("OPENAI_MODEL", "ai/gemma3:270M-F16")
base_url = os.environ.get("OPENAI_BASE_URL", "http://model-runner.docker.internal/engines/v1/")
openai_key = os.environ.get("OPENAI_API_KEY", "notset")

if openai_key == "notset":
    raise ValueError("`OPENAI_API_KEY` environment variable is not set.")

openai_params = {
    "model_name": model_name,
    "base_url": base_url,
}
if base_url:
    openai_params["base_url"] = base_url

def get_openai_client() -> ChatOpenAI:
    return ChatOpenAI(
        **openai_params
    )