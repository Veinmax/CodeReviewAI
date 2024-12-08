import logging
from fastapi import FastAPI, HTTPException
from utils.github_api import fetch_repository_contents
from utils.openai_api import analyze_code
from schemas import ReviewRequest, ReviewResponse


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(title="CodeReviewAI")


@app.post("/review", response_model=ReviewResponse)
async def review_assignment(request: ReviewRequest) -> ReviewResponse:
    """
       Endpoint to review a coding assignment.
       Parameters:
           - request: JSON payload containing GitHub repository URL, assignment description, and candidate level.
       Returns:
           - ReviewResponse: Analysis result.
    """
    try:
        # Fetch repository contents
        repo_contents = await fetch_repository_contents(request.github_repo_url)
        # Analyze code using Grok API
        analysis_result = await analyze_code(
            assignment_description=request.assignment_description,
            repo_contents=repo_contents,
            candidate_level=request.candidate_level
        )

        return ReviewResponse(**analysis_result)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
