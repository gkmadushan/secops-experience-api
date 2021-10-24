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
ENVIRONMENT_SERVICE_URL = os.getenv('ENVIRONMENT_SERVICE_URL')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["UserServiceAPIs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/environments")
def create(payload: dict = Body(...)):
    response = requests.post(ENVIRONMENT_SERVICE_URL+'/v1/environments', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text
        

@router.get("/environments")
def get(request: Request = None):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/environments?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.put("/environments/{id}")
def update(id:str, payload: dict = Body(...)):
    response = requests.put(ENVIRONMENT_SERVICE_URL+'/v1/environments/'+id, json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/environments/{id}")
def get_by_id(id:str):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/environments/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.delete("/environments/{id}")
def delete(id:str):
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


@router.put("/resources/{id}")
def update(id:str, payload: dict = Body(...)):
    response = requests.put(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id, json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/resources/{id}")
def get_by_id(id:str):
    response = requests.get(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.delete("/resources/{id}")
def delete(id:str):
    response = requests.delete(ENVIRONMENT_SERVICE_URL+'/v1/resources/'+id)
    if response.text:
        return json.loads(response.text)
    else:
        return Response(status_code=204) 