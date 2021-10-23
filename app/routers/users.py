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
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["UserServiceAPIs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/users")
def create(payload: dict = Body(...)):
    response = requests.post(USER_SERVICE_URL+'/v1/users', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.post("/users/{id}/reset-password")
def reset(payload: dict = Body(...)):
    response = requests.post(USER_SERVICE_URL+'/v1/users'+id+'/reset-password', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/users")
def get(request: Request = None):
    response = requests.get(USER_SERVICE_URL+'/v1/users?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.put("/users/{id}")
def update(id:str, payload: dict = Body(...)):
    response = requests.put(USER_SERVICE_URL+'/v1/users/'+id, json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.get("/users/{id}")
def get_by_id(id:str):
    response = requests.get(USER_SERVICE_URL+'/v1/users/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.delete("/users/{id}")
def delete(id:str):
    response = requests.delete(USER_SERVICE_URL+'/v1/users/'+id)
    if response.text:
        return json.loads(response.text)
    else:
        return Response(status_code=204) 

@router.get("/groups")
def get(request: Request = None):
    response = requests.get(USER_SERVICE_URL+'/v1/groups?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.post("/groups")
def create(payload: dict = Body(...), ):    
    response = requests.post(USER_SERVICE_URL+'/v1/groups', json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text


@router.put("/groups/{id}")
def create(id:str, payload: dict = Body(...)):
    response = requests.put(USER_SERVICE_URL+'/v1/groups/'+id, json=payload)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/groups/{id}")
def get_by_id(id:str):
    response = requests.get(USER_SERVICE_URL+'/v1/groups/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.delete("/groups/{id}")
def delete(id:str):
    response = requests.delete(USER_SERVICE_URL+'/v1/groups/'+id)
    if response.text:
        try:
            return json.loads(response.text)
        except:
            return response.text
    else:
        return Response(status_code=204) 

@router.get("/roles")
def get(request:Request = None):
    response = requests.get(USER_SERVICE_URL+'/v1/roles?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text