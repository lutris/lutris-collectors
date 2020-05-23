"""Export Humble Bundle library with the Lutris client
The user must be connected to Humble Bundle in Lutris for the export to work
"""
import json
from lutris.services.humblebundle import HumbleBundleService


def get_humble_library():
    """Without an official API to get a list of Humble Bundle games, the next best
    thing is to extract data from orders.
    """
    service = HumbleBundleService()
    humble_orders = service.get_orders()
    humble_products = {}
    # Skip Android games / Ebooks / Soundtracks / Videos
    ignored_platforms = (
        {"audio"},
        {"ebook"},
        {"ebook", "audio"},
        {"android"},
        {"video"},
        set(),  # Empty platforms are ususally a redemption deadline
    )
    for order in humble_orders:
        for product in order["subproducts"]:
            platforms = {d["platform"] for d in product["downloads"]}
            if platforms in ignored_platforms:
                continue
            humble_products[product["machine_name"]] = {
                "slug": product["machine_name"],
                "name": product["human_name"],
                "website": product["url"],
                "icon": product["icon"],
                "platforms": list(platforms)
            }
    return humble_products


if __name__ == "__main__":
    humble_library = get_humble_library()
    with open("humblebundle.json", "w") as humble_export:
        humble_export.write(json.dumps(humble_library, indent=2))
