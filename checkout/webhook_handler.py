from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    # Confirms event sent from Stripe was received
    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    # Sent every time a User completes payment and it's successful
    # It handles the payment_intent.succeeded webhook from Stripe
    # This intent contains all of the customer data, I think from the JS Fn
    # Order will already be on the system in theory
    def handle_payment_intent_succeeded(self, event):
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Empty strings are replaced with "None"
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # 1. We assume the order doesn't already exist in the DB
        order_exists = False
        # 8. Start of correcting potential asynchronous delays:
        # The while loop tries every second (see except below), up to 5 times
        attempt = 1
        while attempt <= 5:
            try:
                # 2. We try to get the order using the info from the payment intent
                # Need an exact match, but case insensitive (iexact)
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    # These allow a User place identical orders
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # 3. If order does exist, set to True...
                order_exists = True
                # 9. Once order is found, break out of loop
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        # 4 & 10. ...and return response to Stripe that we verified existance of order
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        # 5 & 11. If order doesn't exist, we create it just like we would from the submitted form (Views "Checkout")
        else:
            order = None
            try:
                # 6. This creates the order (like a form would) using the intenmt data
                # How does this come before 5.1 below?
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    # These allow a User place identical orders. It says that if we
                    # don't have these pieces of data, it;s OK to create the order
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # 5.1. The data is loaded from json version in intent, rather than session
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            # 7. If it fails, sending a 500 error will let Stripe know to try it again later
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # 6.1 & 12. If we;re here, then the order has been created so we let Stripe know
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    # Where the above fails, this handles the...
    # ...payment_intent.payment_failed webhook from Stripe
    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)