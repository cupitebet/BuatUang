import hmac
from uuid import uuid4

from fastapi import Request

from app.config import config
from app.models.exception import HttpException


def get_task_id(request: Request):
    task_id = request.headers.get("x-task-id")
    if not task_id:
        task_id = uuid4()
    return str(task_id)


def get_api_key(request: Request):
    api_key = request.headers.get("x-api-key")
    return api_key


def verify_token(request: Request):
    """Wajibkan header x-api-key jika `api_key` diisi di config.toml; tanpa api_key API tetap terbuka."""
    expected = str(config.app.get("api_key", "") or "")
    if not expected:
        return
    token = get_api_key(request) or ""
    if not hmac.compare_digest(token.encode(), expected.encode()):
        raise HttpException(
            task_id=get_task_id(request),
            status_code=401,
            message="invalid or missing x-api-key",
        )
