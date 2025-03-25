import uvicorn
from task_queue.celery_app import app


def run_dev_server():
    """Entry point for the development server."""
    uvicorn.run("app.main:app", reload=True)


def run_celery():
    """Entry point for the celery worker."""
    app.worker_main(["worker", "--loglevel=info"])


if __name__ == "__main__":
    run_celery()
