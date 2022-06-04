from __future__ import annotations
import dacite
from ._response_parser import *
from dataclasses import dataclass

@dataclass(repr=True, eq=True)
class MarketOrder:
    price: float
    quantity: int
    vendor_id: int


@dataclass(repr=True, eq=True)
class MarketListing:
    """WARNING: DO NOT INSTANTIATE DIRECTLY, USE dacite.from_dict()"""
    buy_best: Optional[float]
    sell_best: Optional[float]
    buy_volume: Optional[int]
    sell_volume: Optional[int]
    buy_orders: Optional[list[MarketOrder]]
    sell_orders: Optional[list[MarketOrder]]


@dataclass(repr=True, eq=True)
class MarketScan:
    """WARNING: DO NOT INSTANTIATE DIRECTLY, USE dacite.from_dict()"""
    scan_id: int
    scan_time: int
    listings: list[MarketListing]
    listings_index: dict

    def get_listing(self, name):
        return self.listings[self.listings_index[name]]


def create_market_scan(data):
    return dacite.from_dict(MarketScan, data)


def create_market_listing(data):
    return dacite.from_dict(MarketListing, data)


def create_market_order(data):
    return dacite.from_dict(MarketOrder, data)
