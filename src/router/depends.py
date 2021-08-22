
import uuid
from flask import make_response, request
from core.config import settings


def get_client_id(request) -> str:
    return request.cookies.get('client-id', None)


def get_remote_addr(request) -> str:
    if "x-forwarded-for" in request.headers:
        return request.headers['x-forwarded-for']
    else:
        return request.environ["REMOTE_ADDR"]


def base_response(response, headers: dict = None):
    response = make_response(response)

    if not get_client_id(request):
        response.set_cookie(
            "client-id",
            uuid.uuid4().hex,
            max_age=settings.EXPIRE_COOKIE
        )

    if headers:
        for key, value in headers.items():
            response.headers[key] = value

    return response
