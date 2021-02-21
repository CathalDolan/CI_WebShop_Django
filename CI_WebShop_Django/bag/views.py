from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ Renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    # I thinkm, this allows the User to stay on the page they were on
    redirect_url = request.POST.get('redirect_url')
    # Check if there is a session called "bag" and if not, create one. It's a dict
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
    
    # Over-write the current session or add the new one
    request.session['bag'] = bag
    return redirect(redirect_url)
