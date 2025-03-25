# Story Core

A FastAPI-based service for story protocol agent interactions.

## Prerequisites

- Python 3.11 or higher
- uv (Python package installer)

## Installation

1. Clone the repository:
    
    ```bash
    git clone https://github.com/DeepSynth-HQ/story-core.git
    ```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

3. Install the project and its dependencies:
```bash
uv pip install -e .
```

## Running the Development Server
You can run the development server in two ways:

1. Using the `api` script:
```bash
api
```
2. Or using the Python module directly:
```bash
python src/cli.py
```
