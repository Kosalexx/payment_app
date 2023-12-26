from __future__ import annotations

import logging
from io import BytesIO
from sys import getsizeof
from typing import TYPE_CHECKING
from uuid import uuid4

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from PIL import Image
from shop.business_logic.errors import ItemAlreadyExistsError, ItemNotFoundError
from shop.models import Category, Currency, Item

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from shop.business_logic.dto import AddItemDTO


logger = logging.getLogger(__name__)


def replace_file_name_to_uuid(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Replaces the user's filename with the uuid4 standard name."""

    old_name = file.name
    file_extension = old_name.split(".")[-1]
    file_name = str(uuid4())
    file.name = file_name + "." + file_extension
    logger.info(
        "Successfully replaced file name with the uuid4 standard name",
        extra={"old_file_name": old_name, "new_file_name": file.name},
    )
    return file


def change_file_size(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
    """Changes the size of uploaded images."""

    content_type = file.content_type
    if content_type is not None:
        file_format = content_type.split("/")[-1].upper()
    else:
        file_format = ""
    output = BytesIO()
    with Image.open(file) as image:
        image.thumbnail(size=(400, 400))
        image.save(output, format=file_format, quality=100)
    old_size = file.size
    new_size = getsizeof(output)
    file = InMemoryUploadedFile(
        file=output,
        field_name=file.field_name,
        name=file.name,
        content_type=file.content_type,
        size=getsizeof(output),
        charset=file.charset,
    )
    logger.info("Successfully changed file size", extra={"old_size": str(old_size), "new_size": str(new_size)})
    return file


def get_all_products() -> QuerySet:
    """Gets info about all products from DB."""

    data = Item.objects.select_related("currency").all()
    return data


def create_product(data: AddItemDTO) -> str:
    """Creates product in database with passed data."""

    try:
        currency = Currency.objects.get(name=data.currency)
        category = Category.objects.get(name=data.category)
        created_item = Item.objects.create(
            name=data.name, price=data.price, description=data.description, currency=currency, category=category
        )
        if data.photo is not None:
            file = replace_file_name_to_uuid(data.photo)
            file = change_file_size(file=file)
            created_item.photo = file
            created_item.save()
        pk: str = created_item.pk
    except IntegrityError:
        logger.info(
            msg="Product with passed name already exist.",
            extra={"name": data.name},
        )
        raise ItemAlreadyExistsError
    return pk


def get_product_by_id(item_id: int) -> QuerySet:
    """Gets info about concrete product from DB by passed id."""
    try:
        item = Item.objects.select_related("currency").get(id=item_id)
        return item
    except Item.DoesNotExist as err:
        logger.error("Item not found.", extra={"item_id": item_id}, exc_info=err)
        raise ItemNotFoundError
