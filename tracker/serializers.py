from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'




    def get_product_name(self, obj):
        # Return the product's title associated with this price history entry
        return obj.product.title
