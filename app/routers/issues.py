from starlette.responses import Response
from fastapi import APIRouter, Depends, Request, Body
from dependencies import common_params, get_db, get_secret_random, send_email
from dependencies import get_token_header
from exceptions import username_already_exists
import os

import json
import requests


page_size = os.getenv('PAGE_SIZE')
BASE_URL = os.getenv('BASE_URL')
ISSUE_SERVICE_URL = os.getenv('ISSUE_SERVICE_URL')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["IssueManagementAPIs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/issues")
def get(request: Request = None):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/issues/{id}")
def get_by_id(id:str):
    response = requests.get(ISSUE_SERVICE_URL+'/v1/issues/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

