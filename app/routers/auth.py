from typing import Optional
from fastapi import APIRouter, Request
from fastapi.param_functions import Form
from dependencies import get_db, hash, validate_token, generate_token, get_secret_random
import requests
import json
import os

page_size = os.getenv('PAGE_SIZE')
BASE_URL = os.getenv('BASE_URL')
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')

router = APIRouter(
    tags=["TokenAPIs"],
    responses={404: {"description": "Not found"}},
)

@router.get("/experience-service/users/{id}/verify/{token}")
def get(id:str, token:str, request:Request = None):
    response = requests.get(USER_SERVICE_URL+'/users/'+id+'/verify/'+token)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.post("/experience-service/oauth/token")
def post(username = Form(...), password = Form(...), otp : Optional[str] = Form(None)):
    data = {"username":username, "password":password}
    if(otp):
        data["otp"] = otp
    response = requests.post(USER_SERVICE_URL+'/oauth/token', data=data)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.post("/experience-service/oauth/refresh-token")
def post(username = Form(...), password = Form(...), otp : Optional[str] = Form(None)):
    data = {}
    response = requests.post(USER_SERVICE_URL+'/oauth/refresh-token', data=data)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.patch("/experience-service/users/{id}/verify/{token}")
def post(id:str, token:str):
    data = {}
    response = requests.patch(USER_SERVICE_URL+'/oauth/refresh-token', data=data)
    try:
        return json.loads(response.text)
    except:
        return response.text