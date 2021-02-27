from django.contrib import admin
from .models import Order, OrderLineItem


# Allows us to manipulate the line without going to the site I think
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):

    # Comes from the class above
    inlines = (OrderLineItemAdminInline,)

    # Prevents these fields from being tampered with in the Admin once set
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    # Dictates the order the fields appear. Not essential, but nice
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    # Restricts the columns that show up in the order list to only a few key items
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    # Related to the list above. Ordered by date with newest to the top
    ordering = ('-date',)

# Registering the models.
admin.site.register(Order, OrderAdmin)
