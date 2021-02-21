from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ Renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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
                # If Yes, increment the quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # If not, just set the quantity to = the quantity. Applies to new sizes, same item
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # If item not already in the bag, it's added in form of a doct with the size and quantity
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # Over-write the current session or add the new one
    request.session['bag'] = bag
    return redirect(redirect_url)
