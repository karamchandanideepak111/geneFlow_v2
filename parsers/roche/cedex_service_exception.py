""" This module provides functionality to raise CedexServiceException"""


class CedexServiceException(Exception):
    """
    This Class is used to raise a Custom Exception
    """

    def __init__(self, message, errorcode):
        self.message = message
        self.error_code = errorcode

    def __dict__(self):
        return {'message': self.message, "errorCode": str(self.error_code)}
