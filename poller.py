import settings
import requests
import json
import datetime


def send_to_pegasus(data):
  return True # placeholder function to represent sending to pegasus
def job_status_check(id):
  return True # placeholder function to represent checking on jobs being run
# Begin Set UP
url = settings.URL
s = requests.Session()
r = s.get(url)
csrf_token = r.cookies['csrftoken']
headers = {'Content-type': 'application/json',  "X-CSRFToken":csrf_token, 'Referer': url}
next_payload = {'status': 'next'}
progress_payload = {'status': 'in_progress'}
complete_payload = {'status': 'complete'}
fail_payload = {'status': 'failed'}
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



