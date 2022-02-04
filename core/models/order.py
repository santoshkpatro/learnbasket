from django.db import models
from core.models.base import BaseModel
from core.models.program import Program
from core.models.user import User
from core.models.coupon import Coupon


class Order(BaseModel):
    ORDER_STATUS_CHOICES = (
        (0, 'INITIATED'),
        (1, 'PROCESSING'),
        (2, 'SUCCESS'),
        (3, 'CANCELLED'),
    )

    order_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='user_orders'
    )
    program = models.ForeignKey(
        Program, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        related_name='program_orders'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey(
        Coupon, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='coupon_orders'
    )
    status = models.IntegerField(default=0, choices=ORDER_STATUS_CHOICES)
    transaction_id = models.CharField(max_length=35, blank=True, null=True)
    payment_id = models.CharField(max_length=35, blank=True, null=True)

    class Meta:
        db_table = 'orders'

    def __str__(self) -> str:
        return self.order_number