"""Utils."""
from .const import UNIQUE_ID_POSTFIX


def add_unique_id_postfix(unique_id):
    """Add unique ID postfix"""
    return unique_id + UNIQUE_ID_POSTFIX


def remove_unique_id_postfix(unique_id):
    """Remove unique ID postfix"""
    return unique_id[0 : -len(UNIQUE_ID_POSTFIX)]
