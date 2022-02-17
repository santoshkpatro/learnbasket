from django.db import models
from server.models.base import BaseModel
from server.models.order import Order


class BillingAddress(BaseModel):
    program_order = models.OneToOneField(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField()
    landmark = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=10)

    class Meta:
        db_table = 'billing_addresses'

    def __str__(self) -> str:
        return 'Billing address of order - ' + self.program_order.order_id