import urllib2


class OnfleetException(Exception):
    pass


class OnfleetDuplicateKeyException(OnfleetException):
    pass
