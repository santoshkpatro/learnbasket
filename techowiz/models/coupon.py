from django.db import models
from techowiz.models.base import BaseModel
from techowiz.models.program import Program


class ActiveCouponManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Coupon(BaseModel):
    programs = models.ManyToManyField(Program, blank=True)
    coupon_code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    show_at_checkout = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveCouponManager()

    class Meta:
        db_table = 'coupons'

    def __str__(self) -> str:
        return self.coupon_code
