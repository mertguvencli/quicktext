from flask import request
from flask_socketio import (
    emit, join_room, leave_room
    # close_room, rooms, disconnect
)
from router.depends import get_client_id
from router.route import socketio, cache
from model.viewers import Viewers
from model.quicktext import QuickText


def add_room_viewers(room):
    Viewers(cache=cache, key=room, client_id=get_client_id(request)).add()


def remove_room_viewers(room):
    Viewers(cache=cache, key=room, client_id=get_client_id(request)).remove()


def get_room_viewers(room):
    return Viewers(cache=cache, key=room).viewer_count()


def get_data(room):
    return QuickText(cache=cache, key=room).get()


@socketio.event
def join(message):
    room = message["room"]
    add_room_viewers(room)
    join_room(room)
    visitors = get_room_viewers(room)
    data = {
        'data': get_data(room),
        'viewer_count': visitors
    }
    emit('channel', data, to=room)


@socketio.event
def channel_event(message):
    room = message["room"]
    client_id = get_client_id(request)
    add_room_viewers(room)
    quick = QuickText(cache=cache, key=room, text=message["text"])
    quick.update_text(client_id=client_id)
    emit(
        'channel',
        {
            'data': quick.get(client_id=client_id),
            'typing_client_id': client_id,
            'viewer_count': get_room_viewers(room),
        },
        to=message['room']
    )


@socketio.event
def typing(message):
    emit(
        'channel_typing',
        {
            "client_id": get_client_id(request),
            "text": message["text"]
        },
        to=message['room']
    )


@socketio.event
def leave(message):
    room = message['room']
    leave_room(room)
    remove_room_viewers(room)
    emit(
        'channel',
        {
            'data': QuickText(cache=cache, key=room).get(),
            'viewer_count': get_room_viewers(room),
        },
        to=room
    )
