from .cart import Cart

# create contact processor so our cart can work on all pages
def cart(request):
    # return the default data from our Cart
    return {'cart': Cart(request)}