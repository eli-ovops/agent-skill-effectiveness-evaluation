FREE_SHIPPING_FROM = 100


def default_shipping(subtotal):
    return 0 if subtotal >= FREE_SHIPPING_FROM else 10


def total_due(subtotal, shipping=None):
    shipping = shipping or default_shipping(subtotal)
    return subtotal + shipping


def cart_total(subtotal, shipping=None):
    return total_due(subtotal, shipping)


def invoice_total(subtotal, shipping=None):
    return total_due(subtotal, shipping)
