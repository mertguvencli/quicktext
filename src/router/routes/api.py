from flask import request, jsonify
from router import depends
from router.route import app, cache
from model.quicktext import QuickText
from utils import shorten
from core.config import settings


@app.route('/q', methods=("POST",))
@app.route('/q/<key>', methods=("GET",))
def route_api(key=None):
    if request.method == "POST":
        key = shorten.generate(cache)
        payload: dict = request.get_json(force=True)

        if payload:
            quick = QuickText(
                cache=cache,
                key=key,
                text=payload.get('text', None),
                owner_client_id=depends.get_client_id(request),
                ip_whitelist=str(payload.get('ip_whitelist')).split(';') if payload.get('ip_whitelist', None) else [],  # noqa
                viewer_can_edit=payload.get('viewer_can_edit', False),
                share_on_network=payload.get('share_on_network', False),
                remote_addr=depends.get_remote_addr(request)
            )
            quick.add()

            return jsonify({
                "success": True,
                "key": key,
                "data": quick.get(),
                "url": f"{settings.BASE_URL}/{key}"
            }), 201

        return jsonify({
            "success": False,
            "message": "Body cant be null." if not payload else "Something went wrong",  # noqa
        }), 400

    if request.method == "GET":
        client_id = depends.get_client_id(request)
        quick = QuickText(cache=cache, key=key)
        data = quick.get()
        if data:
            if not quick.allowed_whitelist(
                client_id=client_id,
                remote_addr=depends.get_remote_addr(request)
            ):
                return jsonify({
                    "success": False,
                    "message": "You do not have permission to view this data",  # noqa
                }), 400

        return jsonify({
            "success": True,
            "key": key,
            "data": quick.get(),
            "url": f"{settings.BASE_URL}/{key}"
        }), 200
