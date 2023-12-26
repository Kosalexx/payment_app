from typing import Any

from django import forms


class SubmitOrderForm(forms.Form):
    """An implementation of submitting Order form."""

    user_email = forms.EmailField(
        label="Enter your email",
        help_text="Product information will be sent to your e-mail address",  # TODO: send_email
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True,
    )
    coupon = forms.CharField(
        label="Enter promo code for discount", widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    currency = forms.ChoiceField(
        label="Currency of payment", required=True, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, currencies: list[tuple[str, str]], *args: Any, **kwargs: Any) -> None:
        super(SubmitOrderForm, self).__init__(*args, **kwargs)
        self.fields["currency"].choices = currencies
