from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import users, auth, environments, inventory, issues, kb
import time
from starlette_exporter import PrometheusMiddleware, handle_metrics


app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8089",
    "http://localhost:3000",
]

#middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-request-payload"] = str(request.body)
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


#user routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(environments.router)
app.include_router(inventory.router)
app.include_router(issues.router)
app.include_router(kb.router)