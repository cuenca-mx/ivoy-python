class IvoyException(Exception):
    """Generic iVoy API exception"""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f'Code: {self.code} - Message: {self.message}'


class ExpiredTokens(IvoyException):
    """API Tokens Expired"""
