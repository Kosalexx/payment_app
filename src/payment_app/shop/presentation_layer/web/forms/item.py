from decimal import Decimal
from typing import Any

from django import forms
from shop.presentation_layer.common.validators import (
    ValidateFileSize,
    ValidateImageExtensions,
)
from shop.presentation_layer.web.validators import WebValidator


class AddItemForm(forms.Form):
    """An implementation of adding Item form."""

    name = forms.CharField(
        max_length=100, label="Name", required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        max_length=400,
        label="Description",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False,
        help_text="Enter Description.",
    )
    price = forms.DecimalField(
        min_value=Decimal(0.50),
        max_digits=9,
        decimal_places=2,
        label="Price",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
    )
    currency = forms.ChoiceField(label="Currency", required=True, widget=forms.Select(attrs={"class": "form-control"}))
    category = forms.ChoiceField(label="Category", required=True, widget=forms.Select(attrs={"class": "form-control"}))
    photo = forms.ImageField(
        label="Photo",
        allow_empty_file=False,
        required=False,
        validators=[
            WebValidator(ValidateImageExtensions(["png", "jpeg", "jpg"])),
            WebValidator(ValidateFileSize(max_size=5_000_000)),
        ],
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    def __init__(
        self, currencies: list[tuple[str, str]], categories: list[tuple[str, str]], *args: Any, **kwargs: Any
    ) -> None:
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields["currency"].choices = currencies
        self.fields["category"].choices = categories
