
__all__ = (
    'AioArpError',
    'InvalidIpError',
    'NotFoundError',
    'TimeoutError',
    'ReadTimeoutError'
)

class AioArpError(Exception):
    ...

class InvalidIpError(AioArpError):
    ...

class NotFoundError(AioArpError):
    ...

class TimeoutError(AioArpError):
    ...

class ReadTimeoutError(TimeoutError):
    ...

class WriteTimeoutError(TimeoutError):
    ...
