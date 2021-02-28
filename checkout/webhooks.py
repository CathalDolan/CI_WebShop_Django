from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe

@require_POST # Reject GET requests
@csrf_exempt #  Stripe doesn;t send the CSRF token which we normally need
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Stripe provided code. endpoint_secret changed to wh_secret
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError as e:
        # Invalid payload. Stripe provided code
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature. Stripe provided code
        return HttpResponse(status=400)
    except Exception as e:
        # Added to handle all other exceptions
        return HttpResponse(content=e, status=400)
    # End of Stripe provided code. All rest replaced.

    print('Success!')
    return HttpResponse(status=200)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # Use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)
    return response
