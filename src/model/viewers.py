from typing import List
from cachetools import TTLCache


class Viewers:
    def __init__(
        self,
        *,
        cache: TTLCache,
        key: str,
        client_id: str = None
    ) -> None:
        self.cache = cache
        self.key = key
        self.client_id = client_id

    def live_key(self) -> str:
        return f'live_{self.key}'

    def get(self) -> List:
        return self.cache.get(self.live_key(), [])

    def add(self):
        viewer_list = self.get()
        if viewer_list:
            if self.client_id not in viewer_list:
                viewer_list.append(self.client_id)
                self.cache[self.live_key()] = viewer_list
        else:
            self.cache[self.live_key()] = [self.client_id]

    def remove(self):
        viewer_list = self.get()
        if viewer_list:
            if self.client_id in viewer_list:
                viewer_list.pop(viewer_list.index(self.client_id))
                self.cache[self.live_key()] = viewer_list

    def viewer_count(self) -> int:
        viewer_list = self.get()
        if viewer_list:
            return len(viewer_list)
        else:
            return 0
