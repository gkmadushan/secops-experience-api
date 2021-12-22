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
INVENTORY_SERVICE_URL = os.getenv('INVENTORY_SERVICE_URL')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["InventoryAPIs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/inventory")
def get(request: Request = None):
    response = requests.get(INVENTORY_SERVICE_URL+'/v1/inventory?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/inventory/varients")
def get(request: Request = None):
    response = requests.get(INVENTORY_SERVICE_URL+'/v1/inventory/varients?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/inventory/varients/{id}")
def get_by_id(id:str):
    response = requests.get(INVENTORY_SERVICE_URL+'/v1/inventory/varients/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

@router.get("/inventory/{id}")
def get_by_id(id:str):
    response = requests.get(INVENTORY_SERVICE_URL+'/v1/inventory/'+id)
    try:
        return json.loads(response.text)
    except:
        return response.text

