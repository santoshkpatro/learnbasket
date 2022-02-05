from django.db import models
from techowiz.models.base import BaseModel
from techowiz.models.program import Program


class Coupon(BaseModel):
    programs = models.ManyToManyField(Program, blank=True)
    coupon_code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    show_at_checkout = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'coupons'

    def __str__(self) -> str:
        return self.coupon_code
