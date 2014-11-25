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

        # Create the job record. Do not pass a user since it is anonymous.
        job = jobModel.createJob(
            title='Demo', type='demo_task', handler='demo_handler')

        # Create a token that is scoped for updating the job.
        jobToken = jobModel.createJobToken(job)

        # Set the kwargs that will be passed to the celery task.
        job['kwargs'] = {
            'token': jobToken['_id'],
            'count': 100
        }
        job = jobModel.save(job)

        # Actually schedule the job (triggers our handler in __init__.py)
        jobModel.scheduleJob(job)
        return 'Job was scheduled.'
    startDemoJob.description = (
        Description('Start a demo job that writes job log entries.'))
