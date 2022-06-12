from typing import *


def _g(data: dict, path: str):
    """
    Function used to access a dictionary using the dot notation.

    :param data: dicitonary to access
    :param path: path (dot notation) to access
    :return: dict item"""
    result = data
    for p in path.split("."):
        result = result.get(p)
    return result


def parse_order(data: dict) -> dict:
    return {"price": _g(data, "price"),
            "quantity": _g(data, "amount"),
            "vendor_id": _g(data, "userID")}


def parse_orders(orders: list) -> list:
    return [parse_order(order) for order in orders]


def parse_listings(data: dict) -> Tuple[List, dict]:
    return (
        [{"name": name,
          "buy_best": _g(v, "summary.buy.Best"),
          "sell_best": _g(v, "summary.sell.Best"),

          "buy_volume": _g(v, "summary.buy.Volume"),
          "sell_volume": _g(v, "summary.sell.Volume"),

          "buy_orders": parse_orders(_g(v, "listings.buy")),
          "sell_orders": parse_orders(_g(v, "listings.sell"))}
         for name, v in data.items()],

        {key: index for index, key in enumerate(data)}
    )


def parse_scan(data):
    result = dict()
    result["scan_id"] = _g(data, "_id")
    result["scan_time"] = _g(data, "scInfo.capturedTime")
    result["listings"] = _g(data, "marketInfo")
    (result["listings"], result["listings_index"]) = parse_listings(result["listings"])

    return result
