from flask import render_template, request, redirect, jsonify
from router.route import app, cache
from router.depends import base_response, get_client_id, get_remote_addr
from utils import shorten
from model.quicktext import QuickText
from core.config import settings


def get_all_items():
    global items
    items = []

    def append(key):
        if key not in items:
            items.append(key)

    for key, value in cache.items():
        if "text" in value:  # prevent to viewer list
            if value["share_on_network"]:
                if value["remote_addr"] == get_remote_addr(request):
                    append(key)
            if get_remote_addr(request) in value["ip_whitelist"]:
                append(key)
            # owners can see their all items
            if value["owner_client_id"] == get_client_id(request):
                append(key)

    results = []
    for key in items:
        model = cache[key]
        model['key'] = key
        model['summary'] = str(model["text"][:7]) + "..."
        results.append(model)

    return results


@app.route('/', methods=("GET",))
def index():
    key = shorten.generate(cache)
    shared_items = get_all_items()
    return base_response(
        render_template(
            'pages/index.html',
            key=key,
            shared_items=shared_items
        ),
        headers={"key": key}
    )


@app.route('/<key>', methods=("GET",))
def get_data(key):
    client_id = get_client_id(request)
    quick = QuickText(cache=cache, key=key)
    data = quick.get()
    if data:
        if not quick.allowed_whitelist(
            client_id=client_id,
            remote_addr=get_remote_addr(request)
        ):
            return redirect('/')

    return base_response(
        render_template(
            'pages/app.html',
            data=data,
            key=key,
            base_url=settings.BASE_URL,
            client_id=client_id
        ),
        headers={"key": key}
    )


@app.route('/offline', methods=("GET",))
def offline():
    return base_response(
        render_template(
            'pages/offline.html'
        )
    )


@app.route('/check', methods=("POST",))
def check():
    payload = request.get_json()
    if not payload or "key" not in payload:
        return jsonify({
            "success": False,
            "found": False,
            "message": "Request is invalid!"
        }), 400

    return base_response(
        jsonify({
            "success": True,
            "found": True if payload["key"] in cache.keys() else False,
            "message": ""
        })
    )
