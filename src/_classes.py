from __future__ import annotations
import json
import time
import dacite
from ._response_parser import *
from dataclasses import dataclass, asdict, astuple, field


@dataclass()
class Exportable:
    def asdict(self):
        return asdict(self)

    def astuple(self):
        return astuple(self)

    def asjson(self):
        return json.dumps(self.asdict())


@dataclass(repr=True, eq=True)
class MarketOrder(Exportable):
    price: float
    quantity: int
    vendor_id: int


@dataclass(repr=True, eq=True)
class MarketListing(Exportable):
    """WARNING: DO NOT INSTANTIATE DIRECTLY, USE create_market_listing OR dacite.from_dict()"""
    buy_best: Optional[float]
    sell_best: Optional[float]
    buy_volume: Optional[int]
    sell_volume: Optional[int]
    buy_orders: Optional[list[MarketOrder]]
    sell_orders: Optional[list[MarketOrder]]


@dataclass(repr=True, eq=True)
class MarketScan(Exportable):
    """WARNING: DO NOT INSTANTIATE DIRECTLY, USE create_market_scan OR dacite.from_dict()"""
    scan_id: Optional[int]
    listings: list[MarketListing]
    listings_index: dict
    scan_time: int = field(default_factory=lambda: round(time.time()))

    def get_listing(self, name):
        return self.listings[self.listings_index[name]]


def create_market_scan(data):
    return dacite.from_dict(MarketScan, data)


def create_market_listing(data):
    return dacite.from_dict(MarketListing, data)


def create_market_order(data):
    return dacite.from_dict(MarketOrder, data)
