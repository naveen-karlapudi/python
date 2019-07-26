#!/usr/local/bin/python3.6 -u
import requests
import json

ACCESS_ENDPOINT = "access.platform.intuit.com"
DEVELOPER_SERVICE_ENDPOINT = 'developer.api.intuit.com'


APP_ID = 'Intuit.dev.test.monitoringclient'
APP_SECRET = '@option.APP_SECRET@'
intuit_token_type='IAM-Ticket'


# Execute the TEP Job and get the Execution ID
ACCESS_ENDPOINT_URI = 'https://' + ACCESS_ENDPOINT  + '/v1/offline_tickets/create_for_system_user'
access_headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'intuit_originatingip': '1.1.1.1',
           'Authorization': 'Intuit_IAM_Authentication intuit_appid='+APP_ID+',intuit_app_secret='+APP_SECRET+',intuit_token_type=IAM-Ticket'}
access_body = {
    "username":"prdg6tj9jsix2haxnwllgv0ykjwnxwkndy1@robot.net",
    "password":"@option.access_offlineuser_password@",
    "namespaceid":"50000000"
}

gettoken = requests.post(url=ACCESS_ENDPOINT_URI, data=json.dumps(access_body), headers=access_headers)

if gettoken.status_code == 200:
    print("Get Token Success")
else:
    print("Get Token failure")
    exit(1)

# Get the Execution ID to valudate the Job Status
gettoken_json = json.loads(gettoken.content)
access_token = gettoken_json["offlineTicket"]

# Access developer service aws accounts api for a specific user
DEVELOPER_SERVICE_ENDPOINT_URI = 'https://'+ DEVELOPER_SERVICE_ENDPOINT + '/v3/resources/user?resourceTypeId=cloudAccount&username=vprasad1'
developer_service_header = { 'Authorization': 'Intuit_IAM_Authentication intuit_appid='+APP_ID+',intuit_app_secret='+APP_SECRET+',intuit_token='+access_token+',intuit_token_type=IAM-Offline-Ticket'}

developer_service_response = requests.get(url=DEVELOPER_SERVICE_ENDPOINT_URI, headers=developer_service_header)


if developer_service_response.status_code == 200:
    print("AWS account page loaded successfully")
else:
    print("AWS account page load failure, Paging Oncall",developer_service_response.status_code)
    exit(1)

