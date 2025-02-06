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

3. [Milvus](https://milvus.io/): It's an open-source vector database built for GenAI applications.

4. [Apache Kafka](https://kafka.apache.org/): It's an open-source distributed event streaming platform used for high-throughput, real-time data streaming

5. [FastAPI](https://fastapi.tiangolo.com/) - It's a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.

6. [Poetry](https://python-poetry.org/) - It's a modern dependency management tool. To install it use the below command.

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

## Example Demo

The data indexed into milvus:

```
{
	"text": "Hi! My name is Gurbaj Singh. I am a senior backend engineer with over 7+ years of relevant experience in various product based startups in the fields of AI, Blockchain and Data intensive Applications. In my recent role, I architected and implemented a real-time alerting system for blockchain security products, specifically focusing on Solana and Cosmos-based chains. This system was designed to handle the challenges of ever-growing blockchain data and an expanding user base, ensuring scalability and reliability. My hands-on experience with real-time data processing, system architecture, and scalable solutions aligns closely with the technical stack and requirements of this opportunity.",
	"timestamp": "2025-01-29 08:49:13.676"
}
```

The user prompted:

```
Can you tell me about gurbaj?
```

API output response:

```
<think>
Okay, so I need to figure out how to answer the question "can you tell me about gurbaj?" using the provided context. Let's break it down step by step.

First, I should look at the context given. It includes several sentences about Gurbaj Singh:

1. He is a senior backend engineer with over 7+ years of experience.
2. His experience spans product-based startups in AI, Blockchain, and Data-intensive Applications.
3. He designed a system to handle growing blockchain data and expanding user bases, ensuring scalability and reliability.
4. Recently, he architected and implemented a real-time alerting system for blockchain security on Solana and Cosmos chains.
5. His hands-on experience includes real-time data processing, system architecture, and scalable solutions.

Now, the question is asking about Gurbaj, so I need to compile this information into a coherent answer. It should include his name, role, experience, specific projects or roles he's had, and his expertise areas.

I should structure it in a way that flows naturally, perhaps starting with an introduction of who he is, followed by his experience, then some specifics about his recent work, and ending with how his skills align with opportunities.

Wait, I need to make sure not to include any information outside the context. For example, there's mention of Solana and Cosmos- based chains in his recent role, so that should be included as specific areas he's focused on.

Also, I need to ensure that the answer is concise but covers all key points from the context without adding unnecessary details or making assumptions beyond what's provided.

I think a good approach would be:
1. Introduce Gurbaj Singh and his current role.
2. Mention his years of experience and fields he's worked in.
3. Highlight a specific project or system he architected recently.
4. Note his expertise areas that align with opportunities.

Putting it all together, the answer should flow smoothly, connecting each piece of information logically to present a comprehensive overview of Gurbaj based on the context provided.

I also need to avoid using any markdown formatting and keep the language clear and straightforward as per the user's request.
</think>

Gurbaj Singh is a senior backend engineer with over seven years of experience in product-based startups, specializing in AI, Blockchain, and Data-intensive Applications. He has designed systems to manage growing blockchain data and expanding user bases, ensuring scalability and reliability. Recently, he architected and implemented a real-time alerting system for blockchain security products focused on Solana and Cosmos chains. His expertise lies in real-time data processing, system architecture, and scalable solutions, making him well-suited for relevant opportunities.
```

![demo-screenshot](/rag_app_deepseek/static/images/demo-screenshot.png)

## Note

This project was generated using [fastapi_template](https://github.com/s3rius/FastAPI-template).
