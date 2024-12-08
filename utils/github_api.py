import os
import logging
import json
import redis
from fastapi import HTTPException
from github import Github, GithubException
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Initialize redis client
redis_client = redis.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    decode_responses=True
)


async def fetch_repository_contents(repo_url: str) -> list:
    """
    Fetches the repository contents using the PyGithub library and caches results in Redis.
    """
    cache_key = f"repo_contents:{repo_url}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        logger.info(f"Using cached repository contents for {repo_url}")
        return json.loads(cached_data)

    try:
        owner, repo_name = repo_url.split("/")[-2:]
        my_git = Github(GITHUB_TOKEN)
        repo = my_git.get_repo(f"{owner}/{repo_name}")
        contents = repo.get_contents("")
        files = []
        while contents:
            file = contents.pop(0)
            if file.type == "dir":
                contents.extend(repo.get_contents(file.path))
            else:
                files.append({
                    "name": file.name,
                    "path": file.path,
                    "download_url": file.download_url,
                    "type": file.type
                })
        redis_client.set(cache_key, json.dumps(files), ex=3600)
        return files
    except GithubException as e:
        logger.error(f"GitHub API error: {e}")
        raise HTTPException(status_code=400, detail="Failed to fetch repository contents from GitHub.")
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")
        raise RuntimeError(f"Failed to fetch repository contents: {e}")
