from django.core.management.base import BaseCommand

from tracker.models import TrackedProduct
from tracker.price_service import get_product_price

class Command(BaseCommand):

 help = "Check current prices of all tracked products"


def handle(self, *args, **kwargs):

    tracked_products = TrackedProduct.objects.filter(
        is_tracking=True
    )

    if not tracked_products.exists():
        self.stdout.write(
            self.style.WARNING(
                "No products are currently being tracked."
            )
        )
        return

    for product in tracked_products:

        self.stdout.write(
            f"Checking: {product.product_name}"
        )

        try:
            current_price = get_product_price(
                product.url
            )

            if current_price is None:
                self.stdout.write(
                    self.style.WARNING(
                        "Could not get the current price."
                    )
                )
                continue

            product.current_price = current_price

            if current_price <= product.threshold_price:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"TARGET REACHED! "
                        f"Current price: ₹{current_price}"
                    )
                )

                product.is_tracking = False

            else:
                self.stdout.write(
                    f"Current price: ₹{current_price} | "
                    f"Target price: ₹{product.threshold_price}"
                )

            product.save()

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error checking product: {e}"
                )
            )

    self.stdout.write(
        self.style.SUCCESS(
            "Price checking completed."
        )
    )

