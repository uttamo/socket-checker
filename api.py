import os
from typing import List, Tuple, Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from checker import execute_socket_checks

app = FastAPI()


def authenticate_client(client_secret: str) -> bool:
    return os.getenv('SOCKET_CHECKER_SECRET') == client_secret


class CheckSocketsRequest(BaseModel):
    sockets: List[Tuple[str, int]]
    timeout: Optional[float]


@app.get('/check')
def check(request_body: CheckSocketsRequest, http_authorization: str = Header(None, convert_underscores=False)):
    if not authenticate_client(http_authorization):
        raise HTTPException(401, 'Unauthorised')
    results = execute_socket_checks(request_body.sockets, timeout=request_body.timeout)
    return results
