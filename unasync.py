import re

FILES = [
     ("aioarp/_async.py", "aioarp/_sync.py"),
     ("tests/test_async.py", "tests/test_sync.py")
]

SUBS = [
    ('async def async_send_arp', 'def sync_send_arp'),
    ('async def', 'def'),
    ('from .backends._async import AsyncStream', 'from .backends._sync import Stream'),
    ('AsyncStream', 'Stream'),
    ('await ', ''),
    ('async_send_arp', 'sync_send_arp'),
    ('aioarp.arequest', 'aioarp.request'),
    ("async with", "with")
]

COMPILED_SUBS = [
    (re.compile(r'(^|\b)' + regex + r'($|\b)'), replaced)
    for regex, replaced in SUBS
]


def unasync_line(line):
    for regex, replaced in COMPILED_SUBS:
        line = re.sub(regex, replaced, line)
    return line


def unasync_file(async_path, sync_path):
    with open(async_path, "r") as in_file:
        with open(sync_path, "w", newline="") as sync_file:
            for line in in_file.readlines():
                line = unasync_line(line)
                sync_file.write(line)

def unasync_file_check(async_path, sync_path):
    with open(async_path, "r") as in_file:
        with open(sync_path, "r") as out_file:
            line = 0
            for in_line, out_line in zip(in_file.readlines(), out_file.readlines()):
                line += 1
                expected = unasync_line(in_line)
                if out_line != expected:
                    print(f'Mismatch in: {sync_path}:{line}')
                    print(f'Expected: {expected!r}')
                    print(f'Actual:   {out_line!r}')
                    sys.exit(1)

if __name__ == "__main__":
    import sys

    if 'check' not in sys.argv:
         for async_, sync_ in FILES:
              unasync_file(async_, sync_)
    else:
         for async_, sync_ in FILES:
              unasync_file_check(async_, sync_)