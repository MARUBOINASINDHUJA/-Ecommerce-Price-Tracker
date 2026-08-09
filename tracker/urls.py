from rest_framework import generics

from .models import (
    Product,
    PriceHistory,
    TrackedProduct,
    TrackedPriceHistory,
)

from .price_service import get_product_price

from .serializers import (
    ProductSerializer,
    PriceHistorySerializer,
)

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


class ProductPriceHistoryView(generics.ListAPIView):
    serializer_class = PriceHistorySerializer

    def get_queryset(self):
        queryset = PriceHistory.objects.all()

        return queryset.filter(
            product_id=self.kwargs["pk"]
        )


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

        url = request.POST.get("url")

        threshold_price = request.POST.get(
            "threshold_price"
        )

        if url and threshold_price:

            current_price = get_product_price(url)

            tracked_product = TrackedProduct.objects.create(
                user=request.user,
                url=url,
                product_name="Amazon Product",
                threshold_price=threshold_price,
                current_price=current_price,
                is_tracking=True
            )

            if current_price is not None:
                TrackedPriceHistory.objects.create(
                    product=tracked_product,
                    price=current_price
                )

        return redirect("dashboard")

    return redirect("dashboard")


def dashboard(request):

    tracked_products = TrackedProduct.objects.filter(
        user=request.user
    ).order_by("-created_at")

    for product in tracked_products:

        if product.current_price is not None:

            current = float(product.current_price)

            target = float(product.threshold_price)

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