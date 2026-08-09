from django.core.management.base import BaseCommand

from tracker.models import TrackedProduct
from tracker.price_service import update_tracked_product_price
from tracker.email_service import send_price_alert


class Command(BaseCommand):

    help = "Check prices of all actively tracked products"

    def handle(self, *args, **options):

        tracked_products = TrackedProduct.objects.filter(
            is_tracking=True
        )

        if not tracked_products.exists():

            self.stdout.write(
                self.style.WARNING(
                    "No active products are being tracked."
                )
            )

            return

        self.stdout.write(
            "Checking tracked product prices..."
        )

        for product in tracked_products:

            self.stdout.write(
                f"Checking: {product.product_name}"
            )

            old_price = product.current_price

            new_price = update_tracked_product_price(
                product
            )

            if new_price is None:

                self.stdout.write(
                    self.style.ERROR(
                        f"Could not fetch price for: "
                        f"{product.product_name}"
                    )
                )

                continue

            self.stdout.write(
                f"Price: ₹{new_price}"
            )

            if new_price <= float(
                product.threshold_price
            ):

                self.stdout.write(
                    self.style.SUCCESS(
                        "Target price reached!"
                    )
                )

                try:

                    alert_sent = send_price_alert(
                        product
                    )

                    if alert_sent:

                        self.stdout.write(
                            self.style.SUCCESS(
                                "Price alert email sent."
                            )
                        )

                    else:

                        self.stdout.write(
                            "Alert was already sent "
                            "or email could not be sent."
                        )

                except Exception as error:

                    self.stdout.write(
                        self.style.ERROR(
                            f"Email error: {error}"
                        )
                    )

            else:

                self.stdout.write(
                    "Target price has not been reached yet."
                )

            self.stdout.write("-" * 50)

        self.stdout.write(
            self.style.SUCCESS(
                "Price monitoring completed."
            )
        )