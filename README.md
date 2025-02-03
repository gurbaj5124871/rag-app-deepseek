# RAG APP DEEPSEEK

This project is a RAG (Retrieval-Augmented Generation) application which combines retrieval-based and generative approaches to improve the accuracy and relevance of AI-generated responses.

## Technologies

1. [Deepseek-r1](https://github.com/deepseek-ai/DeepSeek-R1) - It's an Open Sourced Reasoning Large Language Model (LLM)

2. [Ollama](https://ollama.com/) - It's like docker for AI models. Download ollama to self host AI models like deepseek-r1 either via installer or docker</br>
   a. After Installation verify via below command, make sure it's running

    ```
    $ ollama --version
    $ ollama version is 0.5.7

    $ ollama serve
    $ Error: listen tcp 127.0.0.1:11434: bind: address already in use
    ```

    b. Pull the model image using the below command:

    ```
    $ ollama pull deepseek-r1:32b
    ```

    c. Verify the download of the model using the below command:

    ```
    $ ollama list
    ```

    d. Run the model via below command:

    ```
    $ ollama run deepseek-r1:32b
    $ /bye (to exit and go into detached mode)
    ```

    e. Run the below command to see the running models:

    ```
    $ ollama ps
    ```

    f. To stop the model, run the below command:

    ```
    $ ollama stop deepseek-r1:32b
    ```

3. [Apache Kafka](https://kafka.apache.org/): It's an open-source distributed event streaming platform used for high-throughput, real-time data streaming

4. [FastAPI](https://fastapi.tiangolo.com/) - It's a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

5. [Poetry](https://python-poetry.org/) - It's a modern dependency management tool. To install it use the below command.

    ```
    pipx install poetry
    ```

## Get Started

To run the project use this set of commands:

```bash
poetry install
poetry run python3 -m rag_app_deepseek
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry [here](https://python-poetry.org/docs/)

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "rag_app_deepseek"
rag_app_deepseek
├── conftest.py  # Fixtures for all tests.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such kafka etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

An exmaple of .env file:

```bash
RELOAD="True"
PORT="8000"
ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

-   black (formats your code);
-   mypy (validates types);
-   isort (sorts imports in all files);
-   flake8 (spots possibe bugs);
-   yesqa (removes useless `# noqa` comments).

You can read more about pre-commit here: https://pre-commit.com/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
```

For running tests on your local machine.

2. Run the pytest.

```bash
pytest -vv .
```

## Note

This project was generated using [fastapi_template](https://github.com/s3rius/FastAPI-template).
