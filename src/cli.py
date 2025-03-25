import uvicorn


def run_dev_server():
    """Entry point for the development server."""
    uvicorn.run("app.main:app", reload=True)


if __name__ == "__main__":
    run_dev_server()
