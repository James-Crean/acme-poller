# acme-poller
Secure side poller


## Usage

Runs can be retrieved from the poller by submitting an HTTP get request with a parameter named 'request'. The poller currently supports the following requests:

Example URL: `http://127.0.0.1/poller/update/?request=next`

* **all**
    * *GET: ()* -> Returns every job
    * *GET: (user)* -> Returns every job for that user
    *  *POST: (status)* -> Updates every job to the new status
    *  *POST: (user, status)* -> Updates every job for a user to the new status
* **new**
    * *GET: ()* -> Returns every job with a status of 'new'
    * *GET: (user)* -> Returns every job for that user with a status of 'new'
    *  *POST: (user, config_options{} )* -> Creates a new job for that user
* **in_progress**
    * *GET: ()* -> Returns every job with a status of 'in_progress'
    * *GET: (user)* -> Returns every job with a status of 'in_progress' for that user
    * *POST: (job_id)* -> Sets a job to 'in_progress'
* **complete**
    * *GET: ()* -> Returns every job with a status of 'complete'
    * *GET: (user)* -> Returns every job with a status of 'complete' for that user
    * *POST: (job_id)* -> Sets a job to 'complete'
* **failed**
    * *GET: ()* -> Returns every job with a status of 'failed'
    * *GET: (user)* -> Returns every job with a status of 'failed' for that user
    * *POST: (job_id)* -> Sets a job to 'failed'
* **next**
    * *GET: ()* -> Returns the next job to be run.
* **job**
    * *GET: ()* -> Returns a specific job.

All requests that return objects will return a status of 200, with a single empty object if no runs were found.
E.g. A request for the 'next' run on an empty queue will return an empty object with status 200.


The response is encoded in JSON format and each run is an object that contains the run id, user, and run status in addition to the individual fields that describe the run parameters.  

## Error Checking

The poller attempts to send back appropriate HTTP status codes. A status of 200 indicates a successful interaction, while 400 indicates an issue with the request, and 500 indicates a server error.  
