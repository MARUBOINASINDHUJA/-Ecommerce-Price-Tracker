import re
import requests
from bs4 import BeautifulSoup

from .models import TrackedPriceHistory


def get_product_price(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        selectors = [
            "#corePriceDisplay_desktop_feature_div .a-price-whole",
            "#corePriceDisplay_mobile_feature_div .a-price-whole",
            ".a-price .a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "#priceblock_saleprice"
        ]

        for selector in selectors:

            element = soup.select_one(selector)

            if element:

                price_text = element.get_text(
                    strip=True
                )

                price = clean_price(price_text)

                if price is not None:
                    return price

        return None

    except Exception as error:

        print("Price fetching error:", error)

        return None


def clean_price(price_text):

    if not price_text:
        return None

    cleaned = re.sub(
        r"[^\d.]",
        "",
        price_text
    )

    try:
        return float(cleaned)

    except ValueError:
        return None


def update_tracked_product_price(tracked_product):
    """
    Get the latest price and save it to price history.
    """

    new_price = get_product_price(
        tracked_product.url
    )

    if new_price is not None:

        tracked_product.current_price = new_price

        tracked_product.save(
            update_fields=["current_price"]
        )

        TrackedPriceHistory.objects.create(
            product=tracked_product,
            price=new_price
        )

    return new_price