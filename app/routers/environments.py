from starlette import responses
from starlette.responses import Response
from fastapi import HTTPException, APIRouter, Depends, Request, Body
from dependencies import common_params, get_db, get_secret_random, send_email
from dependencies import get_token_header
from exceptions import username_already_exists
import os
import sys
import json
import requests


page_size = os.getenv('PAGE_SIZE')
BASE_URL = os.getenv('BASE_URL')
ENVIRONMENT_SERVICE_URL = os.getenv('ENVIRONMENT_SERVICE_URL')
DETECTOR_SERVICE_URL = os.getenv('DETECTOR_SERVICE_URL')
SCHEDULER_SERVICE_URL = os.getenv('SCHEDULER_SERVICE_URL')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["UserServiceAPIs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/scans/graphs")
def graph():
    response = requests.get(DETECTOR_SERVICE_URL+'/v1/scans/graphs')
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.post("/environments")
def create(payload: dict = Body(...)):
    env_response = requests.post(ENVIRONMENT_SERVICE_URL+'/v1/environments', json=payload)
    schedule_payload = {
        'frequency': payload['frequency'],
        'start': payload['scan_start_time'][0:5]+":00",
        'terminate': payload['scan_terminate_time'][0:5]+":00",
        'reference': payload['id'],
        'active': payload['active']
    }
    schedule_res = requests.post(SCHEDULER_SERVICE_URL+'/v1/schedules', json=schedule_payload)
    try:
        return json.loads(schedule_res.text)
    except:
        return schedule_res.text


@router.post("/bulk-scan")
def bulkscan(payload: dict = Body(...)):
    notify_to = []
    resources = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources?status=1&environment='+payload['reference'])

    try:
        resources_list = json.loads(resources.text)
        if resources_list['data'][0]:
            users = requests.get(USER_SERVICE_URL + '/v1/users?group=' +
                                 resources_list['data'][0]['access_group']+'&role_code=DEVOPS')
            users = json.loads(users.text)
            for user in users['data']:
                notify_to.append(user['email'])
        else:
            return False
    except:
        return False

    for resource in resources_list['data']:
        try:
            request = {
                "scan_type": "OVAL",
                "ipv4": resource['ipv4'],
                "ipv6": resource['ipv6'],
                "username": resource['console_username'],
                "port": resource['port'],
                "os": resource['os'],
                "secret_id": resource['console_secret_id'],
                "reference": resource['id'],
                "target_name": resource['name'],
                "target_url": resource['id'],
                "notify_to": notify_to
            }

            response = requests.post(DETECTOR_SERVICE_URL+'/v1/scans', json=request)
        except:
            # return str(sys.exc_info())
            continue


@router.get("/environments")
def get(request: Request = None):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/environments?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.patch("/environments/{id}/scan")
def scan_environment(id: str, payload: dict = Body(...)):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources?status=true&environment='+id, json=payload)
    try:
        resources = json.loads(response.text)
        for resource in resources['data']:
            request = {
                "scan_type": "OVAL",
                "ipv4": resource['ipv4'],
                "ipv6": resource['ipv6'],
                "username": resource['console_username'],
                "port": resource['port'],
                "os": resource['os'],
                "secret_id": resource['console_secret_id'],
                "reference": resource['id'],
                "target_name": resource['name'],
                "target_url": resource['id'],
                "notify_to": ["gkmadushan@gmail.com"]
            }
            requests.post(DETECTOR_SERVICE_URL+'/v1/scans', json=request).text

        return True

    except:
        return str(sys.exc_info())


@router.put("/environments/{id}")
def update(id: str, payload: dict = Body(...)):
    response = requests.put(ENVIRONMENT_SERVICE_URL+'/v1/environments/'+id, json=payload)
    schedule_payload = {
        'frequency': payload['frequency'],
        'start': payload['scan_start_time'][0:5]+":00",
        'terminate': payload['scan_terminate_time'][0:5]+":00",
        'reference': id,
        'active': payload['active']
    }
    schedule_res = requests.put(SCHEDULER_SERVICE_URL+'/v1/schedules/references/'+id, json=schedule_payload)
    try:
        return json.loads(schedule_res.text)
    except:
        return schedule_res.text


@router.get("/environments/{id}")
def get_by_id(id: str):
    env_response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/environments/'+id)
    schedule_response = requests.get(SCHEDULER_SERVICE_URL+'/v1/schedules/references/'+id)

    try:
        response = json.loads(env_response.text)
        response['schedule'] = json.loads(schedule_response.text)
        return response
    except:
        return schedule_response.text


@router.delete("/environments/{id}")
def delete(id: str):
    response = requests.delete(ENVIRONMENT_SERVICE_URL+'/v1/environments/'+id)
    if response.text:
        return json.loads(response.text)
    else:
        return Response(status_code=204)


@router.post("/resources")
def create(payload: dict = Body(...)):
    response = requests.post(ENVIRONMENT_SERVICE_URL+'/v1/resources', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.post("/resources/connection-test")
def create(payload: dict = Body(...)):
    response = requests.post(ENVIRONMENT_SERVICE_URL+'/v1/resources/connection-test', json=payload)
    try:
        return Response(status_code=response.status_code, content=response.text)
    except:
        return response.text


@router.post("/resources/resource-types")
def create(payload: dict = Body(...)):
    response = requests.post(ENVIRONMENT_SERVICE_URL+'/v1/resources/resource-types', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/resources")
def get(request: Request = None):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/resources/frequencies")
def get_frequencies():
    response = requests.get(SCHEDULER_SERVICE_URL+'/v1/schedules/frequencies')
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.put("/resources/{id}")
def update(id: str, payload: dict = Body(...)):
    response = requests.put(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id, json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.post("/resources/{id}/scan")
def scan(id: str, payload: dict = Body(...)):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id)

    if payload["autofix"]:
        autofix = True
    else:
        autofix = False

    try:
        response_obj = json.loads(response.text)
        request = {
            "ipv4": response_obj['data']['ipv4'],
            "ipv6": response_obj['data']['ipv6'],
            "username": response_obj['data']['console_username'],
            "port": response_obj['data']['port'],
            "os": response_obj['data']['os'],
            "secret_id": response_obj['data']['console_secret_id'],
            "reference": id,
            "autofix": autofix,
            "target_name": response_obj['data']['name'],
            "target_url": response_obj['data']['id'],
            "notify_to": ["gkmadushan@gmail.com"],
        }

        response = requests.post(DETECTOR_SERVICE_URL+'/v1/scans', json=request)
        return Response(status_code=response.status_code, content=response.text)
        # return json.loads(response.text)
    except:
        return response.text


@router.get("/resources/os")
def get_os():
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources/os')
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/resources/{id}")
def get_by_id(id: str):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.delete("/resources/{id}")
def delete(id: str):
    response = requests.delete(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id)
    if response.text:
        return json.loads(response.text)
    else:
        return Response(status_code=204)
