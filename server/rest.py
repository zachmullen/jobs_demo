import cherrypy
import os

from girder.api import access
from girder.api.describe import Description
from girder.api.rest import Resource

class JobDemo(Resource):
    def __init__(self):
        self.resourceName = 'job_demo'

        self.route('POST', (), self.startDemoJob)

    @access.public
    def startDemoJob(self, params):
        jobModel = self.model('job', 'jobs')
        apiUrl = os.path.dirname(cherrypy.url())

        # Create the job record. Do not pass a user since it is anonymous.
        job = jobModel.createJob(
            title='Demo', type='demo_task', handler='demo_handler')

        # Create a token that is scoped for updating the job.
        jobToken = jobModel.createJobToken(job)

        # Set the kwargs that will be passed to the celery task.
        job['kwargs'] = {
            'url': '{}/job/{}'.format(apiUrl, job['_id']),
            'method': 'PUT',
            'headers': {'Girder-Token': jobToken['_id']},
            'count': 100
        }
        job = jobModel.save(job)

        # Actually schedule the job (triggers our handler in __init__.py)
        jobModel.scheduleJob(job)
        return job
    startDemoJob.description = (
        Description('Start a demo job that writes job log entries.'))
