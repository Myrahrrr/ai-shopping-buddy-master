import os
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from chatbots.utils.environment import IS_DATABRICKS


def build_llm(
    model_name: str = "databricks-meta-llama-3-3-70b-instruct",
    temperature: float = 0.0,
) -> BaseChatModel:
    """
    Build a chat LLM using Databricks serving endpoints
    via OpenAI-compatible API.
    """

    if not IS_DATABRICKS:
        raise RuntimeError(
            "Databricks LLM is requested but IS_DATABRICKS is False."
        )

    databricks_token = os.getenv("DATABRICKS_TOKEN")
    databricks_host = os.getenv("DATABRICKS_HOST")

    if not databricks_token or not databricks_host:
        raise RuntimeError(
            "DATABRICKS_TOKEN and DATABRICKS_HOST must be set."
        )

    llm = ChatOpenAI(
        api_key=databricks_token,
        base_url=f"{databricks_host}/serving-endpoints",
        model=model_name,
        temperature=temperature,
    )

    return llm
