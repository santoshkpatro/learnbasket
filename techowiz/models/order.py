from django.db import models
from techowiz.models.base import BaseModel
from techowiz.models.program import Program
from techowiz.models.user import User
from techowiz.models.coupon import Coupon


class UserOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status=0)


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

    objects = models.Manager()
    user_objects = UserOrderManager()

    class Meta:
        db_table = 'orders'

    def __str__(self) -> str:
        return self.order_id