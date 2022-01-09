from starlette.responses import Response
from fastapi import APIRouter, Depends, Request, Body
from dependencies import common_params, get_db, get_secret_random, send_email
from dependencies import get_token_header
from exceptions import username_already_exists
import os
from fastapi import APIRouter, Depends, HTTPException, Request
import sys
import json
import requests
import base64


page_size = os.getenv('PAGE_SIZE')
BASE_URL = os.getenv('BASE_URL')
ISSUE_SERVICE_URL = os.getenv('ISSUE_SERVICE_URL')
ENVIRONMENT_SERVICE_URL = os.getenv('ENVIRONMENT_SERVICE_URL')
KNOWLEDGE_BASE = os.getenv('KNOWLEDGE_BASE')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["IssueManagementAPIs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/issues")
def get(request: Request = None):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/issues/graphs")
def new_issues():
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/graphs')
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/action-types")
def get(request: Request = None):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/action-types?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/issue-status")
def get(request: Request = None):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/issue-status?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/action-types/{id}")
def get(id=str):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/action-types/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/issues/{id}")
def get_by_id(id: str):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/'+id)
    try:
        issue = json.loads(response.text)
        resource_response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+issue['data']['resource_id'])
        resource = json.loads(resource_response.text)
        environment_response = requests.get(
            ENVIRONMENT_SERVICE_URL+'/v1/environments/'+resource['data']['environment_id'])
        environment = json.loads(environment_response.text)
        issue_ids = json.loads(base64.b64decode(issue['data']['issue_id']))
        kb_ref = None
        for issue_id in issue_ids:
            ref_details = json.loads(requests.get(KNOWLEDGE_BASE+'/v1/reports?ref='+issue_id['ref']).content)
            if int(ref_details['meta']['total_records']) > 0:
                kb_ref = ref_details['data'][0]['id']
                break

        response = {
            'data': {
                'issue_status_id': issue['data']['issue_status_id'],
                'id': issue['data']['id'],
                'description': issue['data']['description'],
                'detected_at': issue['data']['detected_at'],
                'last_updated_at': issue['data']['last_updated_at'],
                'locked': issue['data']['locked'],
                'title': issue['data']['title'],
                'resource_id': issue['data']['resource_id'],
                'score': issue['data']['score'],
                'remediation_script': issue['data']['remediation_script'],
                'resolved_at': issue['data']['resolved_at'],
                'false_positive': issue['data']['false_positive'],
                'reference': issue['data']['reference'],
                'issue_id': json.loads(base64.b64decode(issue['data']['issue_id'])),
                'issue_id_raw': issue['data']['issue_id'],
                'resource': resource,
                'environment': environment,
                'kb_ref': kb_ref
            }
        }
        return response
    except:
        raise HTTPException(status_code=404, detail="Error")


@ router.patch("/issues/{id}")
def patch_issue_by_id(id: str, payload: dict = Body(...)):
    try:
        action_request = {
            "issue": id,
            "action_type": payload['action'],
            "notes": payload['notes']
        }
        response = requests.post(ISSUE_SERVICE_URL+'/v1/issues/issue-actions', json=action_request)

        return json.loads(response.text)
    except:
        raise HTTPException(status_code=404, detail="Error")


@ router.get("/issue-actions")
def get(request: Request = None):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/issue-actions?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text
