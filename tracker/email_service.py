from django.core.mail import send_mail
from django.conf import settings


def send_price_alert(tracked_product):
    """
    Send an email when the product reaches
    or goes below the user's target price.
    """

    if tracked_product.alert_sent:
        return False

    if tracked_product.current_price is None:
        return False

    if tracked_product.current_price > tracked_product.threshold_price:
        return False

    user_email = tracked_product.user.email

    if not user_email:
        return False

    subject = "Price Alert - Your target price has been reached!"

    message = (
        f"Good news!\n\n"
        f"Product: {tracked_product.product_name}\n"
        f"Current Price: ₹{tracked_product.current_price}\n"
        f"Your Target Price: ₹{tracked_product.threshold_price}\n\n"
        f"The product has reached your target price.\n"
        f"You can check the product here:\n"
        f"{tracked_product.url}\n\n"
        f"Price Tracker"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    tracked_product.alert_sent = True
    tracked_product.is_tracking = False

    tracked_product.save(
        update_fields=[
            "alert_sent",
            "is_tracking"
        ]
    )

    return True