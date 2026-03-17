# Setup

1. `cd` to the project directory and run `pip install` to install the project dependencies.

    - You can optionally install the dependencies in a virtual environment to avoid polluting your operating system with globally installed Python packages:

        1. Run `pip install virtualenv` to install the `virtualenv` package globally.
        2. Run `python -m virtualenv env` inside the project directory to create a virtual Python environment `env` in the directory.
        3. Run `source env/Scripts/activate` (on Linux or macOS) or `env/Scripts/activate` (on Windows) to activate the virtual environment.
        4. To confirm that the virtual environment is active, look for the `(env)` marker in your shell.
        4. Run `pip install` while the virtual environment is active to sandbox the installed dependencies inside the virtual environment, rather than making them accessible from anywhere on your machine.
        5. When you're done, you can run `deactivate` from the terminal where the virtual environment is active to deactivate it and return to a normal shell session (you should see the `(env)` marker disappear).

2. Create a `.env` file in the directory containing `NEBIUS_API_KEY=<API_KEY_HERE>`.

3. Run `uvicorn main:app` to start the API server.

4. From a different shell window, run `curl -X POST http://localhost:8000/summarize -H "Content-Type: application/json" -d '{"github_url": "<REPOSITORY_URL_HERE>"}'` while the API server is running to get a summary of the supplied GitHub repository.

5. You can use `Ctrl + C` in the terminal window where the API server is running to stop the server.

# Model Selection

I chose **DeepSeek-V3.2** because it struck a good balance between cost and response quality, while remaining fast enough for the needs of this assignment.

# Approach

I prompt-engineered the model to browse the supplied repository URL and used Pydantic's `BaseModel` to ensure that the model returned either a summary in the format specified by the assignment instructions or a valid FastAPI `HTTPException`. I found that the model hallucinated quite a bit with the default temperature, so I turned the temperature down to 0.5.