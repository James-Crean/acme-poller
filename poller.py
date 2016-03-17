import settings
import requests
import json
import datetime


def send_to_pegasus(data):
  return True # placeholder function to represent sending to pegasus
def job_status_check(id):
  return 'complete' # placeholder function to represent checking on jobs being run
# Begin Set Up
url = settings.URL
s = requests.Session()
r = s.get(url)
csrf_token = r.cookies['csrftoken']
headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': url}
next_payload = {'status': 'next'}
progress_payload = {'status': 'in_progress'}
# End Set Up
# Begin Getting Next Run
r = s.get(url, params=next_payload)
if r.status_code == requests.codes.ok:
  data = json.loads(r.content)
  if data: 
    # There was an item waiting in the queue
    success = send_to_pegasus(data)
    if success:
      # Pegasus received the job
      patch_payload = json.dumps({'id': data['id'], 'status': 'In_progress'})
      r = s.patch(url, data=patch_payload, headers=headers)
      if r.status_code == requests.codes.ok:
        # Job status was changed
        print "Success: Job ", data['id'], " is running"
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
r = s.get(url, params=progress_payload)
if r.status_code == requests.codes.ok:
  objects = json.loads(r.content)
  for run in objects:
    status = job_status_check(run['id']) # Obviously will be different for real implementation
    if status == 'in_progress':
      continue
    elif status == 'complete':
      patch_payload = json.dumps({'id': run['id'], 'status': 'complete'})
      r = s.patch(url, data=patch_payload, headers=headers)
      if r.status_code == requests.codes.ok:
        print "Success: Job ", run['id'] ," completed"
      else:
        print "Error: Job ", run['id'] ," completed, but did not change status"
    elif status == 'failed':
      patch_payload = json.dumps({'id': run['id'], 'status': 'failed'})
      r = s.patch(url, data=patch_payload, headers=headers)
      if r.status_code == requests.codes.ok:
        print "Success: Job ", run['id'] ," failed and its status was changed"
      else:
        print "Error: Job ", run['id'] ," failed, but did not change status"











