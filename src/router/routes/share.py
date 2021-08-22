
from flask import request, jsonify
from router import depends
from router.route import app, cache
from model.quicktext import QuickText


@app.route('/share', methods=("POST",))
def sharing():
    key = request.headers.get('key', None)

    if key:
        if key in cache.keys():
            return jsonify({"success": False, "message": "Key already exists!"}), 400  # noqa

        payload = request.get_json()
        if payload:
            quick = QuickText(
                cache=cache,
                key=key,
                text=payload.get('text', None),
                owner_client_id=depends.get_client_id(request),
                password=payload.get('password', None),
                ip_whitelist=str(payload.get('ip_whitelist')).split(';') if payload.get('ip_whitelist', None) else [],  # noqa
                viewer_can_edit=payload.get('viewer_can_edit', False),
                share_on_network=payload.get('share_on_network', False),
                remote_addr=depends.get_remote_addr(request)
            )
            quick.add()
            return jsonify({
                "key": key,
                "data": quick.get()
            }), 201

    return jsonify({"success": False, "message": "Something went wrong"}), 400
