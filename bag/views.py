from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404

# Required for toasts
from django.contrib import messages
from products.models import Product

# Create your views here.

def view_bag(request):
    """ Renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    # Required for displaying toasts
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))

    # I think, this allows the User to stay on the page they were on
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # Check if there is a session called "bag" and if not, create one. It's a dict
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            # Checking if another item with same id and size already exists in the bag
            if size in bag[item_id]['items_by_size'].keys():
                # Adding to an existing size.
                # If Yes, increment the quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                # Adding a new size of any item already in the bag
                # If not, just set the quantity to = the quantity. Applies to new sizes, same item
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added {size.upper()} {product.name} to your bag')
        else:
            # Adding an item with a size
            # If item not already in the bag, it's added in form of a dict with the size and quantity
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            # Changing the qty of an item that has no sizes
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            # Adding a new item to the bag (that has no sizes?)
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    # Over-write the current session or add the new one
    request.session['bag'] = bag
    return redirect(redirect_url)


# Update - Actions taken within the shopping bag
def adjust_bag(request, item_id):
    """ Adjust a quantity of the specified product in the shopping bag """

    # product = Product.objects.get(pk=item_id) =
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            # Removes item ID if all sizes have been removed (IE QTY IS 0)
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removeded {size.upper()} {product.name} from your bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


# Delete - Actions taken within the shopping bag
def remove_from_bag(request, item_id):
    """ Remove a specified product from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            # Removes item ID if all sizes have been removed
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                messages.success(request, f'Removeded {size.upper()} {product.name} from your bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        # This view is posted from a JS fn so we return a 200 HTTP
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing it: {e}')
        return HttpResponse(status=500)
