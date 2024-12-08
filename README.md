# CodeReviewAI

CodeReviewAI is a tool to automate code reviews for coding assignments. It fetches repository contents from GitHub, analyzes the code using an OpenAI API, and provides insights such as downsides, ratings, and conclusions.

---

## Features

- **GitHub Repository Integration**: Fetches repository files and contents.
- **OpenAI-Powered Analysis**: Reviews and rates code using OpenAI's API.
- **Redis Caching**: Optimizes performance by caching repository contents.

---

## Prerequisites

To set up and run this project, ensure you have the following installed:

1. [Docker](https://docs.docker.com/get-docker/)
2. [Docker Compose](https://docs.docker.com/compose/install/)
3. [Poetry](https://python-poetry.org/docs/#installation)

---

## Setup Instructions

### Step 1: Clone the Repository

Clone the project to your local machine:
```bash
git clone https://github.com/Veinmax/CodeReviewAI.git
cd CodeReviewAI
```

### Step 2: Configure Environment Variables

Create a .env file in the project root and copy the environment variables from the .env.example file
To use Grok AI you can get API key from https://console.x.ai/team/813592f7-9394-42f2-b980-09badd39995e/api-keys 

### Step 3: Build and Run with Docker Compose
To build and start the application using Docker Compose:
```bash
sudo docker-compose up --build
```
This will:
1. Start the FastAPI application at http://0.0.0.0:8000.
2. Start a Redis instance for caching.

### Run with poetry
Install dependencies:
```bash
poetry install
```
Start the application:
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Future Improvements

The following phases outline planned improvements for CodeReviewAI to enhance its ability to handle large projects and optimize performance.

---

### Phase 1: Chunking and Hierarchical Summarization

To address limitations in analyzing large repositories, the following techniques will be implemented:

1. **Chunking**:
   - Split the project being analyzed into smaller chunks based on directories, modules, or file groups.
   - Process each chunk independently to ensure prompts remain within manageable size limits.

2. **Hierarchical Analysis**:
   - Perform individual analysis on each chunk.
   - Summarize insights from each chunk.
   - Combine chunk-level summaries into a final comprehensive report.

---

### Phase 2: Parallel Processing and Caching

To improve performance and scalability, the following optimizations will be introduced:

1. **Parallel Processing**:
   - Analyze files or chunks concurrently using asynchronous programming (e.g., `asyncio`).
   - Distribute tasks across multiple workers or machines using frameworks like **Celery** or **Ray**.

2. **Caching Results**:
   - Persist analysis results at the file or chunk level.
   - Avoid re-analyzing unchanged files between runs by storing results in Redis or a database.
   - Automatically invalidate outdated cache entries when files are updated.
