import logging

logger = logging.getLogger(__name__)


def run_job(job_func, *args, **kwargs):
    job_name = job_func.__name__
    try:
        logging.info(f"Starting job: {job_name}")
        job_func(*args, **kwargs)
        logging.info(f"Job {job_name} completed successfully.")
    except Exception as e:
        logging.error(f"Error executing job {job_name}: {e}", exc_info=True)
