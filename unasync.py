import os
import re

SUBS = [
    ('async def async_send_arp', 'def sync_send_arp'),
    ('async def', 'def'),
    ('from ..backends._async import AsyncSocket', 'from ..backends._sync import Socket'),
    ('AsyncSocket', 'Socket'),
    ('await ', ''),
    ('async_send_arp', 'sync_send_arp')
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

def unasync(async_dir, sync_dir):
    for dirpath, _dirnames, filenames in os.walk(async_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                rel_dir = os.path.relpath(dirpath, async_dir)
                async_path = os.path.normpath(os.path.join(async_dir, rel_dir, filename))
                sync_path = os.path.normpath(os.path.join(sync_dir, rel_dir, filename))
                unasync_file(async_path, sync_path)


unasync("aioarp/_async", "aioarp/_sync")
