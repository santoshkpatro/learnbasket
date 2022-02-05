from rest_framework import serializers
from techowiz.models.order import Order

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'order_id',
            'program',
            'price',
            'amount',
            'discount',
            'status',
            'transaction_id'
        ]
