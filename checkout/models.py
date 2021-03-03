from django.db import models


import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product


# This is the overall order
class Order(models.Model):
    # All fields are required except postcode & county (null=True, blank=True)
    # Order no. will be automatically created with "uuid". It's not editable
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    # auto_now sets date and time when a new order is created
    date = models.DateTimeField(auto_now_add=True)
    # Fields will be calculated with amodel method when an order is saved
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    # These fields are added to allow the same user place identical orders
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    # The prepended _ indicates that this method is only available in this class
    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    # Aggregate allows us to update the total using "Sum()"
    # All line items are totalled first and then the delivery calculated
    # This fn is called from "signal.py"
    def update_total(self):

        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0 # How does this all work?
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    # Override default save method. If the order has no...
    # existing Order No. one is the _generate_order_number fn kicks in
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        # super() reactivates the default Save method
        super().save(*args, **kwargs)

    # 
    def __str__(self):
        return self.order_number


# Each individual product is given it's own line on the order form with a total cost for that line
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    # Override default save method to save line item total
    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        # super() reactivates the default Save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
