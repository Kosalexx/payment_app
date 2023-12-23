class ItemAlreadyExistsError(Exception):
    """Raises when created Item already exist in the database."""


class ItemNotFoundError(Exception):
    """Raises when Item wasn't found in the database."""
