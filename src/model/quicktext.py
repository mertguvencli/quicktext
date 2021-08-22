from datetime import datetime
from typing import List
from cachetools import TTLCache
from core.config import settings
from time import time


class QuickText:
    def __init__(
        self,
        *,
        cache: TTLCache,
        key: str,
        text: str = None,
        owner_client_id: str = None,
        password: str = "",
        ip_whitelist: List = [],
        viewer_can_edit: bool = False,
        share_on_network: bool = False,
        remote_addr: str = None
    ) -> None:
        self.cache = cache
        self.key = key
        self.text = text
        self.owner_client_id: str = owner_client_id
        self.password: str = password
        self.ip_whitelist: List = ip_whitelist
        self.viewer_can_edit: bool = viewer_can_edit
        self.share_on_network: bool = share_on_network
        self.remote_addr: str = remote_addr

    def is_alive(self) -> bool:
        return self.key in self.cache.keys()

    def add(self):
        now = time()
        self.cache[self.key] = {
            "text": self.text,
            "owner_client_id": self.owner_client_id,
            "password": self.password,
            "ip_whitelist": self.ip_whitelist,
            "viewer_can_edit": self.viewer_can_edit,
            "share_on_network": self.share_on_network,
            "remote_addr": self.remote_addr,
            "created_at": now,
            "expire_at": now + settings.EXPIRE_CACHE
        }

    def get(self) -> dict:
        def friendly_format(timestamp):
            return datetime.fromtimestamp(timestamp).strftime(settings.DATE_FORMAT) # noqa

        if self.is_alive():
            model = self.cache[self.key]
            model['created_at_friendly'] = friendly_format(model['created_at'])
            model['expire_at_friendly'] = friendly_format(model['expire_at'])
            return model

    def delete(self) -> None:
        self.cache.pop(self.key)

    def update_text(self, *, client_id) -> None:
        item = self.get()
        if item:
            if item["viewer_can_edit"] or item["owner_client_id"] == client_id:
                self.cache[self.key]["text"] = self.text

    def allowed_whitelist(self, *, client_id, remote_addr) -> bool:
        item = self.get()
        if item:
            if len(item["ip_whitelist"]) > 0:
                return remote_addr in item["ip_whitelist"] or item["owner_client_id"] == client_id  # noqa
        return True
