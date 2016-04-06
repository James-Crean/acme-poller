# acme-poller
Secure side poller.

This repository contains an example script that demonstrates several general use cases of the poller. The poller source code can be found under the apps directory of the [ACME-web-fe](https://github.com/ACME-OUI/acme-web-fe) inside views.py.


## Usage

Runs can be retrieved from the poller by submitting an HTTP get request with a status query. The poller currently supports the following statuses: 
* **new** (Returns every job with a status of 'new')
* **in_progress** (Returns every job with a status of 'in_progress')
* **complete** (Returns every job with a status of 'complete')
* **failed** (Returns every job with a status of 'failed')
* **next** (Returns only the oldest job with the status of new)
* **all** (Returns every job currently known to the poller)

Example URL: `http://127.0.0.1/poller/?status=next`

The response is encoded in JSON format and has the following fields:

* id 
* user
* runspec
* casename
* mppwidth
* stop_option
* stop_n
* walltime
* mach
* compset
* res
* project
* compiler

Updating the status of a run in the poller is done via an HTTP POST request. The poller current expects that a post request will contain a CSRF Token, the id of the run being updated and the new status as a string. The CSRF token can be retrieved at the /poller/ base path. Due to the nature of the Django CSRF token, the 'Referer' header should also be set for any post requests. A 503 status code will be sent if Django can not validate the request. For example usage please refer to the poller.py example file. 

## Error Checking

The poller attempts to send back appropriate HTTP status codes. A status of 200 indicates a successful interaction, but be aware that a response of 200 does not imply that a run existed to send back. Response contents may be empty.  
