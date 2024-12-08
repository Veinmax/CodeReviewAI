from pydantic import BaseModel, HttpUrl

class ReviewRequest(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: str


class ReviewResponse(BaseModel):
    found_files: list[str]
    downsides: str
    rating: str
    conclusion: str


