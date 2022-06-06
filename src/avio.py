from __future__ import annotations
import httpx
from aiolimiter import AsyncLimiter
from syncer import sync
from ._classes import *

BASE_URI = "http://adv.vi-o.tech/api"
DEFAULT_RATELIMIT = lambda: AsyncLimiter(60)


def replace_with(new_func):
    def decorator(original_func):
        return new_func

    return decorator


class Client:
    def __init__(self, key: str, ratelimiter: AsyncLimiter = None):
        self._key = key
        self._ratelimiter = ratelimiter or DEFAULT_RATELIMIT()

        self._web = httpx.AsyncClient(headers={"X-API-KEY": self._key}, base_url=BASE_URI)

    async def _req(self, *args):
        async with self._ratelimiter:
            res = await self._web.get(*args)

        if res.is_success:
            return res.json()
        else:
            raise ConnectionError(f"Request failed, status_code=f{res.status_code}")

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
