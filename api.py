import os
from typing import List, Tuple, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from checker import execute_socket_checks

app = FastAPI()


class CheckSocketsRequest(BaseModel):
    api_secret: str
    sockets: List[Tuple[str, int]]
    timeout: Optional[float]


def authorise_client(request_body: CheckSocketsRequest) -> bool:
    return request_body.api_secret == os.getenv('SOCKET_CHECKER_SECRET')


@app.get('/check_sockets')
def check(request_body: CheckSocketsRequest):
    if not authorise_client(request_body):
        raise HTTPException(401, 'Unauthorised.')
    results = execute_socket_checks(request_body.sockets, timeout=request_body.timeout)
    return results
