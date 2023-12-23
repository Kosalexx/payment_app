from dataclasses import dataclass
from decimal import Decimal

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class AddItemDTO:
    name: str
    price: Decimal
    description: str | None
    currency: str
    photo: InMemoryUploadedFile | None
