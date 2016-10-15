from future import standard_library
standard_library.install_aliases()


class OnfleetException(Exception):
    pass


class OnfleetDuplicateKeyException(OnfleetException):
    pass
