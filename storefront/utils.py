from store_admin.models import Order, OrderItem
from .models import Cart, CartItem, StoreCustomerUser
from django.contrib.contenttypes.models import ContentType


def get_or_create_cart(request):
    if request.user.is_authenticated:
        # Get or create cart for authenticated user
        content_type = ContentType.objects.get_for_model(request.user.__class__)
        cart = Cart.objects.filter(
            store=request.store,
            content_type=content_type,
            object_id=request.user.id
        ).first()
        
        if not cart:
            cart = Cart.objects.create(
                store=request.store,
                content_type=content_type,
                object_id=request.user.id,
                session_key=None  # Authenticated users don't need session_key
            )
    else:
        # Get or create cart for guest user
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            store=request.store,
            content_type=None,
            object_id=None
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
    customer, _ = StoreCustomerUser.objects.get_or_create(
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


def merge_carts(session_cart, user_cart):
    """
    Merge a guest user's cart into a registered user's cart.
    """
    if not session_cart or not user_cart:
        return

    for item in session_cart.items.all():
        # Try to find the same product in user's cart
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={'quantity': item.quantity}
        )

        if not created:
            # If item exists in user's cart, add quantities
            user_item.quantity += item.quantity
            user_item.save()

    # Delete the session cart after merging
    session_cart.delete()


def user_logged_in_handler(sender, request, user, **kwargs):
    # Get the existing session cart
    session_cart = Cart.objects.filter(
        session_key=request.session.session_key,
        store=request.store,
        content_type=None,
        object_id=None
    ).first()

    # Get or create the user's cart
    user_cart = get_or_create_cart(request)

    # Merge the carts if there was a session cart
    if session_cart:
        merge_carts(session_cart, user_cart)
