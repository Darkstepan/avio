from __future__ import annotations
import httpx
from aiolimiter import AsyncLimiter
from syncer import sync
from ._classes import *

BASE_URI = "http://adv.vi-o.tech/api"
DEFAULT_RATELIMIT = lambda: AsyncLimiter(60)


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

    async def get_current_scan(self) -> MarketScan:
        """Fetches current market scan"""

        res = await self._req("/market")
        return create_market_scan(parse_scan(res))

    async def get_scan_by_id(self, scan_id: int) -> MarketScan:
        """Fetches old market scan by its id

        :param id: scan_id to fetch
        :result: MarketScan"""
        res = await self._req(f"/market/{scan_id}")
        print(res)
        return create_market_scan(parse_scan(res))

    sync_get_current_scan = sync(get_current_scan)
    sync_get_scan_by_id = sync(get_scan_by_id)
