from .models import Cart, Order, OrderItem, Customer


def get_or_create_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(
        session_key=session_key,
        store=request.store
    )
    return cart


def convert_cart_to_order(cart, customer_data):
    """
    Converts a Cart into an Order.

    Args:
        cart (Cart): The cart object.
        customer_data (dict): A dict with 'name', 'email', (optional 'phone').

    Returns:
        Order: The created order object.
    """
    # 1. Get or create customer
    customer, _ = Customer.objects.get_or_create(
        store=cart.store,
        email=customer_data['email'],
        defaults={
            'name': customer_data.get('name', ''),
            'phone': customer_data.get('phone', '')
        }
    )

    # 2. Create order
    order = Order.objects.create(
        store=cart.store,
        customer=customer
    )

    # 3. Create OrderItems from CartItems
    for item in cart.items.select_related('product'):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,  # snapshot
            quantity=item.quantity,
            unit_price=item.product.price  # snapshot
        )

    # 4. Calculate total
    order.calculate_total()

    # 5. Optionally clear the cart
    cart.items.all().delete()

    return order
