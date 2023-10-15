import base64
from django.core.exceptions import ValidationError
from string import Template, punctuation
from django.utils.translation import gettext_lazy as text

def convert_string_to_base32(text: str):
    """
    Convert a given string to a base32-encoded string.
    Args:
        text (str): The input string that needs to be encoded.
    Returns:
        str: The base32-encoded string representing the input text.
    """
    encoded_bytes = base64.b32encode(text.encode())
    encoded_string = encoded_bytes.decode()
    return encoded_string



def validate_password(password: str):
    """
    Validates the given password based on specific criteria.
    Args:
        password (str): The password string to be validated.
    Raises:
        ValidationError: If the password fails to meet any of the following criteria:
            - The length of the password is less than 8 characters.
            - The password does not contain at least one numeric digit.
            - The password does not contain at least one uppercase character.
            - The password does not contain at least one lowercase character.
            - The password does not contain at least one special character.
    Returns:
        bool: True if the password passes all validation criteria.
    Note:
        - The password must be at least 8 characters long.
        - The password must contain at least one numeric digit (0-9).
        - The password must contain at least one uppercase letter (A-Z).
        - The password must contain at least one lowercase letter (a-z).
        - The password must contain at least one special character (e.g., !@#$%^&*()_-+=).
    """
    special_characters = list(punctuation)

    if len(password) < 8:
        return False, text("Password must be at least 8 characters")
    if not any(char.isdigit() for char in password):
        return False, text("Password must contain at least one numeric digit")
    if not any(char.isupper() for char in password):
        return False, text("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        return False, text("Password must contain at least one lowercase letter")
    if not any(char in special_characters for char in password):
        return False, text("Password must contain at least one special character")
    return True, None