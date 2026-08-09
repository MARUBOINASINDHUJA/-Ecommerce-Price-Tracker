from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    rating = models.FloatField(
        null=True,
        blank=True
    )

    reviews = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )

    seller = models.CharField(
        max_length=255
    )

    source = models.CharField(
        max_length=50
    )

    is_tracking = models.BooleanField(
    default=True
    )

    alert_sent = models.BooleanField(
    default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class TrackedProduct(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    url = models.URLField()

    product_name = models.CharField(
        max_length=255,
        default="Tracked Product"
    )

    threshold_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    current_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_tracking = models.BooleanField(
        default=True
    )

    alert_sent = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product_name


class TrackedPriceHistory(models.Model):
    product = models.ForeignKey(
        TrackedProduct,
        on_delete=models.CASCADE,
        related_name="price_history"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.product_name} - {self.price}"