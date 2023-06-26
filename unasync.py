import re

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
    with (open(async_path, "r") as in_file, \
          open(sync_path, "w", newline="") as sync_file):
            for line in in_file.readlines():
                line = unasync_line(line)
                sync_file.write(line)

unasync_file("aioarp/_async.py", "aioarp/_sync.py")
unasync_file("tests/test_async.py", "tests/test_sync.py")
