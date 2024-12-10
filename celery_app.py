from celery import Celery

celery = Celery(
    __name__,
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True
)

celery.autodiscover_tasks(['utils'])


celery.conf.update(
    task_track_started=True,  # Track task start
    worker_concurrency=1,  # Single worker concurrency (adjust as needed)
)
