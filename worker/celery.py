from __future__ import absolute_import

import celery
import time

from .logger import StdoutLogger


app = celery.Celery(
    main='jobs_worker',
    broker='amqp://guest@localhost//')


@app.task(name='demo_task')
def demo_task(url, method, headers=None, count=10):
    """
    This is a really dumb task that just logs a bunch of numbers and then
    returns the sum of those integers [0 .. count).
    """
    sum = 0
    with StdoutLogger(url, method, headers):
        for i in range(count):
            print i
            sum += i
            time.sleep(0.1)

    return sum
