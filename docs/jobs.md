# Jobs and execution model

Video ingestion is asynchronous from the API client's perspective. A job is created as QUEUED, processed in a FastAPI background worker, and ends as COMPLETED or FAILED.

For larger deployments, replace FastAPI BackgroundTasks with a durable queue such as Celery/RQ/managed workers without changing the job API contract.
