  
/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

/* Taken from App views.py. Slices remove the quotes */
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

/* This sets up Stripe */
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
/* Used to style the card below. Taken from Stripe's JS Docs */
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
/* Injects the fields into the html */
card.mount('#card-element');

/* Handles realtime validation errors on the card element */
/* Error messages created by Stripe */
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    /* Prevents the default POST action from happening */
    ev.preventDefault();
    /* This executes instead */
    card.update({ 'disabled': true});
    /* This prevents multiple submissions */
    $('#submit-button').attr('disabled', true);
    /* Trigger the loader spinner when Submit buttyon is clicked */
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    /* Call fn for payment intent call to Stripe */
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            /* If there is an error, a notification displays */
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            /* Reverses the spinner and overlay if there is an error */
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            /* Where an error happens, the field and btn are re-enabled so User can fix error */
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            /* If payment intent is returned without issue, the form is submitted */
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});