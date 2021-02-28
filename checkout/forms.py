from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    # Tells Django which model to associate the class with and which fields to render
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # Overriding the default form labels, sets autofocus and puts * on required fields
    def __init__(self, *args, **kwargs):

        # Calls the default form set-up
        super().__init__(*args, **kwargs)
        # To be used in teh form instead of labels
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # Sets placeholders according to the dict values above
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Addition of a CSS class for styling applied to all fields
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Removing default form labels because we have placeholders instead
            self.fields[field].label = False
