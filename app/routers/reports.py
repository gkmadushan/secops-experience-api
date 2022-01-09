from typing import Optional
from fastapi import APIRouter, Depends, Request, Body, Response
from dependencies import common_params, get_db, get_secret_random, send_email
from dependencies import get_token_header
from exceptions import username_already_exists
import os
from fastapi import APIRouter, Depends, HTTPException, Request
import sys
import json
import requests
import base64
from fastapi.responses import StreamingResponse, JSONResponse, RedirectResponse
from httpx import AsyncClient


page_size = os.getenv('PAGE_SIZE')
BASE_URL = os.getenv('BASE_URL')
ISSUE_SERVICE_URL = os.getenv('ISSUE_SERVICE_URL')
ENVIRONMENT_SERVICE_URL = os.getenv('ENVIRONMENT_SERVICE_URL')
KNOWLEDGE_BASE = os.getenv('KNOWLEDGE_BASE')
REPORTING_SERVICE_URL = os.getenv('REPORTING_SERVICE_URL')
DETECTOR_SERVICE_URL = os.getenv('DETECTOR_SERVICE_URL')

router = APIRouter(
    prefix="/experience-service/v1",
    tags=["ReportingAPIs"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/cve")
def cve(score: Optional[str] = 4):
    try:
        response = requests.get(DETECTOR_SERVICE_URL+'/v1/sync?score='+str(score))
        return Response(status_code=response.status_code, content=response.text, headers={'Content-type': 'json'})
    except:
        return str(sys.exc_info())


@router.get("/reports")
def get(request: Request = None):
    response = requests.get(REPORTING_SERVICE_URL+'/v1/reports?'+str(request.query_params))
    try:
        return json.loads(response.text)
    except:
        return response.text


client = AsyncClient(base_url=REPORTING_SERVICE_URL)


@router.get("/reports/scans/{id}")
async def get(id: str, request: Request = None):
    req = client.build_request('GET', '/v1/reports/scans/'+id)
    r = await client.send(req, stream=True)
    return StreamingResponse(
        r.aiter_raw(),
        headers=r.headers
    )


@router.get("/reports/environments/{id}")
async def get(id: str, request: Request = None):
    req = client.build_request('GET', '/v1/reports/environments/'+id)
    r = await client.send(req, stream=True)
    return StreamingResponse(
        r.aiter_raw(),
        headers=r.headers
    )
