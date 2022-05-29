class CantGetCoordinates(Exception):
    """Program can't get current GPS coordinates"""

class TokenNotFound(Exception):
    """Program can`t get token"""

class ApiServiceError(Exception):
    """Program can't get current weather"""