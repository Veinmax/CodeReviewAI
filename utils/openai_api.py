import os
from openai import OpenAI
import httpx
from dotenv import load_dotenv, find_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Initialize Grok client
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)


async def analyze_code(
    assignment_description: str, repo_contents: list, candidate_level: str
) -> dict:
    """
    Analyzes code using Grok API.
    """
    try:
        # Prepare file list and code snippets for the prompt
        file_list = [item["name"] for item in repo_contents]
        code_snippets = {}
        logger.info("Fetching code snippets...")
        for file in repo_contents:
            if file["type"] == "file" and "download_url" in file:
                async with httpx.AsyncClient() as async_client:
                    file_response = await async_client.get(file["download_url"])
                    code_snippets[file["name"]] = file_response.text

        prompt = f"""
        You are reviewing code for a {candidate_level} developer.
        Assignment Description: {assignment_description}
        Files Found: {file_list}
        Code Snippets: {code_snippets}

        Please analyze the code and provide answer in the following format:
        1. Downsides: A summary of downsides.
        2. Rating: A rating (e.g., Excellent, Good, Needs Improvement).
        3. Conclusion: A conclusion.
        """

        # Call Grok API
        logger.info(f"Waiting for response from Grok API...")
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {
                    "role": "system",
                    "content": "You are Grok, a helpful code review assistant.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        # Extract response content
        content = response.choices[0].message.content

        return {
            "found_files": file_list,
            "downsides": content.split("Downsides:")[1].split("Rating:")[0].replace("\n", " "),
            "rating": content.split("Rating:")[1].split("Conclusion:")[0].replace("\n", " "),
            "conclusion": content.split("Conclusion:")[1].replace("\n", " "),
        }

    except Exception as e:
        raise RuntimeError(f"Failed to analyze code using Grok API: {e}")
