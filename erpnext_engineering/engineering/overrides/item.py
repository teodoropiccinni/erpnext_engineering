from typing_extensions import Literal
from erpnext.stock.doctype.item.item import Item as ERPNextItem

class CustomItem(ERPNextItem):
    naming_series: Literal[
        "000.#####", "100.#####", "101.#####", "102.#####", "103.#####", "104.#####", "104.#####",
        "105.#####", "106.#####", "110.#####", "111.#####", "112.#####", "113.#####", "114.#####",
        "115.#####", "120.#####", "121.#####", "200.#####", "201.#####", "202.#####", "203.#####", "204.#####"
    ]
