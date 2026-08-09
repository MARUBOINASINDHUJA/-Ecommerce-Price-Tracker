from rest_framework import generics

from .models import (
    Product,
    TrackedProduct,
    TrackedPriceHistory,
)

from .price_service import get_product_price
from .email_service import send_price_alert

from .serializers import ProductSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User

from .forms import RegisterForm


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        if "search" in self.request.query_params:
            keyword = self.request.query_params.get("search")

            if keyword:
                return queryset.filter(
                    title__icontains=keyword
                )

        return queryset


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "tracker/register.html",
        {"form": form}
    )


def test(request):
    return HttpResponse("Tracker is working!")


def login_view(request):
    if request.method == "POST":

        username_or_email = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username_or_email,
            password=password
        )

        if user is None:
            try:
                user_by_email = User.objects.get(
                    email=username_or_email
                )

                user = authenticate(
                    request,
                    username=user_by_email.username,
                    password=password
                )

            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username/email or password."
        )

    return render(
        request,
        "tracker/login.html"
    )


def start_tracking(request):
    if request.method == "POST":

        url = request.POST.get("url", "").strip()
        threshold_price = request.POST.get(
            "threshold_price",
            ""
        ).strip()

        if not url or not threshold_price:
            messages.error(
                request,
                "Please enter both the product URL and target price."
            )
            return redirect("dashboard")

        try:
            threshold_price = float(threshold_price)
        except ValueError:
            messages.error(
                request,
                "Please enter a valid target price."
            )
            return redirect("dashboard")

        if threshold_price <= 0:
            messages.error(
                request,
                "Target price must be greater than ₹0."
            )
            return redirect("dashboard")

        # Get the current product price
        current_price = get_product_price(url)

        if current_price is None:
            messages.error(
                request,
                "We could not get the current product price. Please check the product URL and try again."
            )
            return redirect("dashboard")

        current_price = float(current_price)

        # ------------------------------------------------
        # TARGET PRICE HIGHER THAN CURRENT PRICE
        # ------------------------------------------------

        if threshold_price >= current_price:
            messages.warning(
                request,
                f"⚠️ Your target price ₹{threshold_price:,.0f} "
                f"is higher than the current price ₹{current_price:,.0f}. "
                f"Please enter a target price lower than the current price."
            )
            return redirect("dashboard")

        # ------------------------------------------------
        # TARGET PRICE VERY LOW
        # ------------------------------------------------

        if threshold_price < current_price * 0.5:
            messages.warning(
                request,
                f"⚠️ Your target price ₹{threshold_price:,.0f} "
                f"is more than 50% below the current price "
                f"₹{current_price:,.0f}. Please enter a more reasonable target price."
            )
            return redirect("dashboard")

        # ------------------------------------------------
        # START TRACKING
        # ------------------------------------------------

        TrackedProduct.objects.create(
            user=request.user,
            url=url,
            product_name="Amazon Product",
            threshold_price=threshold_price,
            current_price=current_price,
            is_tracking=True
        )

        messages.success(
            request,
            f"✅ Tracking started! Current price is ₹{current_price:,.0f} "
            f"and your target price is ₹{threshold_price:,.0f}."
        )

        return redirect("dashboard")

    return redirect("dashboard")

def dashboard(request):

    tracked_products = TrackedProduct.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for product in tracked_products:

        if product.current_price is not None:

            current = float(
                product.current_price
            )

            target = float(
                product.threshold_price
            )

            if current > 0:

                product.price_difference_percent = round(
                    ((current - target) / current) * 100,
                    1
                )

            else:

                product.price_difference_percent = 0

            if target < current * 0.5:

                product.price_warning = True

            else:

                product.price_warning = False

            if target >= current:

                product.target_reached = True

            else:

                product.target_reached = False

        else:

            product.price_difference_percent = None
            product.price_warning = False
            product.target_reached = False

    return render(
        request,
        "tracker/dashboard.html",
        {
            "tracked_products": tracked_products
        }
    )