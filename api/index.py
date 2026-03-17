import os
import json
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.us-central1.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

model = "deepseek-ai/DeepSeek-V3.2"

class Repository(BaseModel):
    github_url: str

class Summary(BaseModel):
    summary: str
    technologies: list[str]
    structure: str

class Error(BaseModel):
    status: int
    message: str

@app.post('/api/summarize', response_model=Summary)
def summarize(repository: Repository):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """Your job is to take a URL for a GitHub repository, browse the repository's contents, and return 
                    NOTHING but a stringified Python dict[Literal["summary", "technologies", "structure"], str | list[str] | str] where 
                    "summary" is a brief, human-readable description of what the project does, "technologies" is
                    a list of the main technologies, languages, and frameworks used in the project, and "structure" is
                    a brief description of the project structure. 
                    
                    The following is an example of the output I want for the GitHub URL "https://github.com/psf/requests":
                    
                    {
                        "summary": "**Requests** is a popular Python library for making HTTP requests...",
                        "technologies": ["Python", "urllib3", "certifi"],
                        "structure": "The project follows a standard Python package layout with the main source code in `src/requests/`, tests in `tests/`, and documentation in `docs/`."
                    }

                    Again, return NOTHING but the dictionary formatted as a string -- no backticks or code blocks.
                    """
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{repository.github_url}"
                        }
                    ]
                }
            ],
            temperature=0.5
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Error generating a response")

    # Convert the model's response to JSON
    try:
        raw = response.choices[0].message.content
        parsed = json.loads(raw)
    except Exception:
        raise HTTPException(status_code=502, detail="Model response not valid JSON")

    # Ensure the model's response matches the Summary JSON schema defined above
    try:
        summary = Summary.model_validate(parsed)
        return summary
    except Exception:
        raise HTTPException(status_code=422, detail="Model returned valid JSON but didn't match expected schema")