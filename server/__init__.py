import celery

from . import rest
from girder import events
from girder.utility.model_importer import ModelImporter
from girder.plugins.jobs.constants import JobStatus


def schedule(event):
    """
    This is bound to the "jobs.schedule" event, and will be triggered any time
    a job is scheduled. This handler will process any job that has the
    handler field set to "demo_handler".
    """
    job = event.info
    if job['handler'] == 'demo_handler':
        # Instantiate the celery application with whatever params you want
        celeryapp = celery.Celery(main='jobs_worker', broker='amqp://guest@localhost//')

        # Set the job status to queued
        job['status'] = JobStatus.QUEUED
        ModelImporter.model('job', 'jobs').save(job)

        # Stop event propagation since we have taken care of scheduling.
        event.stopPropagation()

        # Send the task to celery
        celeryapp.send_task(
            job['type'], job['args'], job['kwargs'])


def load(info):
    info['apiRoot'].job_demo = rest.JobDemo()
    events.bind('jobs.schedule', 'jobs_demo', schedule)
