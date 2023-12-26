from shop.models import Tax


def get_stripe_payment_tax() -> Tax:
    """Gets tax object with name 'sales_stripe_tax' from DB."""

    tax: Tax = Tax.objects.get(name="sales_stripe_tax")
    return tax
