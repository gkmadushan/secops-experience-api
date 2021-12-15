from typing import Optional
from fastapi import APIRouter, Request, Body
from fastapi.responses import Response
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
        return Response(content=response.text, status_code=response.status_code)
    except:
        return response.text

@router.post("/experience-service/oauth/token")
def post(username = Form(...), password = Form(...), otp : Optional[str] = Form(None), response: Response = None):
    data = {"username":username, "password":password}
    if(otp):
        data["otp"] = otp
    token_response = requests.post(USER_SERVICE_URL+'/oauth/token', data=data)
    if token_response.status_code == 200:
        token_response_json = json.loads(token_response.text)
        response.set_cookie(key="refresh_token", value=token_response_json['refresh_token'], httponly=True, secure=True)
        response.set_cookie(key="access_token", value=token_response_json['access_token'], httponly=True, secure=True)
        response.status_code = token_response.status_code
        response.body = token_response_json

        try:
            return json.loads(token_response.text)
        except:
            return token_response.text
    else:
        return Response(content=token_response.text, status_code=token_response.status_code)

@router.post("/experience-service/oauth/refresh-token")
def post(username = Form(...), password = Form(...), otp : Optional[str] = Form(None)):
    data = {}
    response = requests.post(USER_SERVICE_URL+'/oauth/refresh-token', data=data)
    try:
        return Response(content=response.text, status_code=response.status_code)
    except:
        return response.text

@router.patch("/experience-service/users/{id}/verify/{token}")
def post(id:str, token:str, payload: dict = Body(...)):

    response = requests.patch(USER_SERVICE_URL+'/users/'+id+'/verify/'+token, json=payload)
    try:
        return Response(content=response.text, status_code=response.status_code)
    except:
        return response.text

@router.post("/experience-service/oauth/revoke")
def post(response: Response = None):
    response.set_cookie(key="refresh_token", value=None, httponly=True, secure=True)
    response.set_cookie(key="access_token", value=None, httponly=True, secure=True)

    return True
        