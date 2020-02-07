class IvoyException(Exception):
    """Generic iVoy API exception"""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f'Code: {self.code} - Message: {self.message}'


class ExpiredTokens(IvoyException):
    """API Tokens Expired"""


class NotEnoughAddresses(IvoyException):
    """Addresses Needed to create Budget/Order"""


class NecessaryFields(IvoyException):
    """Necessary Fields needed to create/edit Packages"""


class InvalidPhone(IvoyException):
    def __init__(self, **kwargs):
        message = f'Invalid or incomplete Phone Number'
        super().__init__(message=message, **kwargs)


class InvalidInformation(IvoyException):
    def __init__(self, **kwargs):
        message = f'Invalid Information Provided'
        super().__init__(message=message, **kwargs)


class NotAvailable(IvoyException):
    def __init__(self, **kwargs):
        message = f'System Not Available, try again later'
        super().__init__(message=message, **kwargs)


class OutOFRange(IvoyException):
    def __init__(self, **kwargs):
        message = f'Address is out of range'
        super().__init__(message=message, **kwargs)


class InvalidCode(IvoyException):
    def __init__(self, **kwargs):
        message = f'This code is not valid or already used'
        super().__init__(message=message, **kwargs)


class AlreadyExists(IvoyException):
    def __init__(self, **kwargs):
        message = f'User with this information already exists'
        super().__init__(message=message, **kwargs)


class MissingInformation(IvoyException):
    def __init__(self, **kwargs):
        message = f'Incomplete or missing information'
        super().__init__(message=message, **kwargs)


class InvoiceError(IvoyException):
    def __init__(self, **kwargs):
        message = f'Invoice cannot be created for this order'
        super().__init__(message=message, **kwargs)


class InvalidDate(IvoyException):
    def __init__(self, **kwargs):
        message = f'Invalid date try a different date'
        super().__init__(message=message, **kwargs)


class InvalidVehicle(IvoyException):
    def __init__(self, **kwargs):
        message = f'Error on vehicle or not available'
        super().__init__(message=message, **kwargs)


class InvalidWarehouse(IvoyException):
    def __init__(self, **kwargs):
        message = f'Invalid Warehouse id'
        super().__init__(message=message, **kwargs)


class DoesNotExists(IvoyException):
    def __init__(self, **kwargs):
        message = f'Could not find anything with the information provided'
        super().__init__(message=message, **kwargs)


class UnableToCreate(IvoyException):
    def __init__(self, **kwargs):
        message = f'Unable to create or process try again later'
        super().__init__(message=message, **kwargs)


class InsufficientFunds(IvoyException):
    def __init__(self, **kwargs):
        message = f'Insufficient Founds'
        super().__init__(message=message, **kwargs)


class NotRegistered(IvoyException):
    def __init__(self, **kwargs):
        message = f'Found not registered with the information provided'
        super().__init__(message=message, **kwargs)


IVOY_EXCEPTIONS = {
    -101: InvalidPhone,
    -102: InvalidPhone,
    -103: InvalidPhone,
    -104: AlreadyExists,
    -111: InvalidInformation,
    -112: InvalidDate,
    -113: OutOFRange,
    -114: OutOFRange,
    -117: NotAvailable,
    -118: NotAvailable,
    -119: InvalidCode,
    -120: InvalidCode,
    -121: NotRegistered,
    -122: InvalidCode,
    -123: AlreadyExists,
    -124: InvalidCode,
    -126: NotRegistered,
    -127: NotAvailable,
    -128: UnableToCreate,
    -132: InvalidInformation,
    -133: UnableToCreate,
    -134: UnableToCreate,
    -135: NotAvailable,
    -136: OutOFRange,
    -137: UnableToCreate,
    -139: InsufficientFunds,
    -141: InvalidInformation,
    -142: InvalidInformation,
    -144: NotRegistered,
    -145: OutOFRange,
    -150: OutOFRange,
    -152: InvalidCode,
    -153: InvalidCode,
    -154: InvalidCode,
    -157: InvoiceError,
    -159: InvoiceError,
    -160: NotAvailable,
    -161: UnableToCreate,
    -162: InvoiceError,
    -163: DoesNotExists,
    -164: NotAvailable,
    -169: InvalidDate,
    -170: AlreadyExists,
    -171: NotRegistered,
    -172: MissingInformation,
    -173: UnableToCreate,
    -174: DoesNotExists,
    -175: InvalidCode,
    -176: InvoiceError,
    -177: UnableToCreate,
    -178: InvoiceError,
    -179: UnableToCreate,
    -180: UnableToCreate,
    -182: MissingInformation,
    -192: InvalidInformation,
    -193: DoesNotExists,
    -194: InvalidInformation,
    -197: MissingInformation,
    -199: MissingInformation,
    -200: NotAvailable,
    -202: AlreadyExists,
    -208: AlreadyExists,
    -209: DoesNotExists,
    -213: OutOFRange,
    -214: OutOFRange,
    -247: MissingInformation,
    -248: MissingInformation,
    -249: MissingInformation,
    -250: InvalidInformation,
    -251: UnableToCreate,
    -252: InvalidVehicle,
    -258: InvalidVehicle,
    -327: InvalidWarehouse,
}


def raise_ivoy_exception(code, message):
    if code in IVOY_EXCEPTIONS:
        ex = IVOY_EXCEPTIONS[code]
        raise ex(code=code)
    else:
        raise IvoyException(code, 'iVoy API error: {}'.format(message))
