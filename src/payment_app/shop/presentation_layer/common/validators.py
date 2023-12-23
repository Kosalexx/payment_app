from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import NotRequired, TypedDict

if TYPE_CHECKING:
    from django.core.files import File


class ValidatorResponse(TypedDict):
    status: bool
    message: NotRequired[str]


class ValidateFileSize:
    """Validates file size."""

    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> ValidatorResponse:
        file_size = value.size
        if file_size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            return {"status": False, "message": f"Max file size is {max_size_in_mb} MB."}

        return {"status": True}


class ValidateImageExtensions:
    """Validates image extensions."""

    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> ValidatorResponse:
        image_extensions = value.name.split(".")[-1]
        if image_extensions not in self._available_extensions:
            return {"status": False, "message": f"Accept only {self._available_extensions}."}

        return {"status": True}
