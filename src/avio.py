from __future__ import annotations
import asyncio
import json

import httpx
import websockets
from aiolimiter import AsyncLimiter
from syncer import sync
from ._classes import *

API_URI = "http://adv.vi-o.tech/api"
WS_URI = "ws://adv.vi-o.tech/ws"
DEFAULT_RATELIMIT = lambda: AsyncLimiter(60)


def replace_with(new_func):
    def decorator(original_func):
        return new_func

    return decorator


class Client:
    def __init__(self, key: str, ratelimiter: AsyncLimiter = None):
        self._key = key
        self._ratelimiter = ratelimiter or DEFAULT_RATELIMIT()

        self._web = httpx.AsyncClient(headers={"X-API-KEY": self._key}, base_url=API_URI)

    async def _req(self, *args):
        try:
            async with self._ratelimiter:
                res = await self._web.get(*args)

            if res.is_success:
                return res.json()
            else:
                raise ConnectionError(f"Request failed, status_code=f{res.status_code}")
        except TimeoutError or httpx.TimeoutException or asyncio.TimeoutError:
            raise TimeoutError("Connection timed out, Vio API is unreachable")

    async def async_get_current_scan(self) -> MarketScan:
        """Asynchronously fetches current market scan"""

        res = await self._req("/market")
        return create_market_scan(parse_scan(res))

    async def async_get_scan_by_id(self, scan_id: int) -> MarketScan:
        """Asynchronously fetches old market scan by its id
        :param scan_id: scan_id to fetch"""

        res = await self._req(f"/market/{scan_id}")
        print(res)
        return create_market_scan(parse_scan(res))

    @replace_with(sync(async_get_current_scan))
    def get_current_scan(self) -> MarketScan:
        """Fetches current market scan"""
        pass

    @replace_with(sync(async_get_scan_by_id))
    def get_scan_by_id(self, scan_id: int) -> MarketScan:
        """Fetches old market scan by its id
        :param scan_id: scan_id to fetch"""
        pass


class WebsocketsClient:
    def __init__(self, key: str):
        self._key = key
        self._connection = None
        self._listening_lock = asyncio.Lock()
        self.sync_callbacks = []
        self.async_callbacks = []

    def add_sync_callback(self, f):
        self.sync_callbacks.append(f)

    def add_async_callback(self, f):
        self.async_callbacks.append(f)

    async def listen(self):
        if self._listening_lock.locked():
            raise Exception("Already listening!")

        async with self._listening_lock:
            self._connection = await websockets.connect(WS_URI, extra_headers={"X-API-KEY": self._key})
            while True:
                res = await self._connection.recv()
                res = json.loads(res)

                if not res["Rtype"] == "Update":
                    continue

                current_scan = create_market_scan(parse_scan(res["DataType"]))

                for callback in self.sync_callbacks:
                    callback(current_scan)

                await asyncio.gather(*[async_callback(current_scan) for async_callback in self.async_callbacks])

    def run(self):
        asyncio.run(self.listen())
