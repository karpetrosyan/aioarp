
__all__ = (
    'AioArpError',
    'NotFoundError',
    'TimeoutError',
    'ReadTimeoutError'
)

class AioArpError(Exception):
    ...

class NotFoundError(AioArpError):
    ...

class TimeoutError(AioArpError):
    ...

class ReadTimeoutError(TimeoutError):
    ...

class WriteTimeoutError(TimeoutError):
    ...
