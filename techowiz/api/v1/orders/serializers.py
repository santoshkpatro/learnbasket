from rest_framework import serializers
from techowiz.models.order import Order
from techowiz.models.program import Program

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
            'transaction_id',
            'payment_id',
        ]


class RazorpayPaymentSerializer(serializers.Serializer):
    razorpay_payment_id = serializers.CharField(required=True)
    razorpay_order_id = serializers.CharField(required=True)
    razorpay_signature = serializers.CharField(required=True)


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'id',
            'title',
            'description'
        ]


class OrderSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(read_only=True)

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