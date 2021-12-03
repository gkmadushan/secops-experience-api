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
    tags=["KnowledgeBaseAPIs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/lessons")
def create(payload: dict = Body(...)):
    response = requests.post(KNOWLEDGE_BASE+'/v1/reports', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/lessons")
def get(request: Request = None):
    response = requests.get(KNOWLEDGE_BASE+'/v1/reports?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/lessons/{id}")
def get_by_id(id:str):
    response = requests.get(KNOWLEDGE_BASE+'/v1/reports/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text