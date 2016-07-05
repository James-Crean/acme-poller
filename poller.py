import settings
import requests
import json
import datetime

def send_to_titan(data):
    # placeholder function to represent sending to titan
    return True


def job_status_check(id):
    # placeholder function to represent checking on jobs being run
    return 'complete'


# Begin Set Up
url = settings.URL
next_payload = {'request': 'next'}
progress_payload = {'request': 'in_progress'}
# End Set Up
# Add a new run
r = requests.post(url, data={'request': 'new', 'user': 'testaccount', 'model': 'CMIP5', 'frequency': 'decadal', 'foo': 'bar'})
if r.status_code == requests.codes.ok:
    data = json.loads(r.content)
    print "New job created with an id of ", data['job_id']
else:
    print 'Could not create new job. Error code ', r.status_code
# Begin Getting Next Run
r = requests.get(url, params=next_payload)
if r.status_code == requests.codes.ok:
    data = json.loads(r.content)
    if data:
        # There was an item waiting in the queue
        success = send_to_titan(data)
        if success:
            # Titan received the job
            data = json.loads(r.content)
            r = requests.post(url, data={'request': 'in_progress', 'job_id': data['job_id']})
            if r.status_code == requests.codes.ok:
                # Job status was changed
                print "Success: Job ", data['job_id'], " is running"
        else:
            # Pegasus broke
            pass
    else:
        # There were no items in the queue
        pass
else:
    # An error occurred, log time and code for debugging
    print datetime.datetime.now(), ' ', r.status_code
# End Getting Next Run
# Begin Finding Completed or Failed Runs

r = requests.get(url, params=progress_payload)
#Let's say that Titan finished all of the jobs at once.
#So we will retrieve all in_progress jobs and set them to complete or failed based on the results of job_status_check
#In the example case, job_status_check just returns complete, but the principle is the same.
if r.status_code == requests.codes.ok:
    objects = json.loads(r.content)
    for run in objects:
        status = job_status_check(run['job_id'])  # Obviously will be different for real implementation
        if status == 'in_progress':
            continue
        elif status == 'complete':
            completed_run = {'job_id': run['job_id'], 'request': 'complete'}
            r = requests.post(url, data=completed_run)
            if r.status_code == requests.codes.ok:
                print "Success: Job ", run['job_id'], " completed"
            else:
                print "Error: Job ", run['job_id'], " completed, but the poller could not update the status"
        elif status == 'failed':
            failed_run = {'job_id': run['job_id'], 'request': 'failed'}
            r = requests.post(url, data=failed_run)
            if r.status_code == requests.codes.ok:
                print "Success: Job ", run['job_id'], " failed and its status was changed"
            else:
                print "Error: Job ", run['job_id'], " failed, but the poller could not update the status"
else:
    # An error occurred, log time and code for debugging
    print datetime.datetime.now(), ' ', r.status_code
