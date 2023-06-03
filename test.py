from aioarp._arp import *
from aioarp._client import request

response = request(
    'enp0s3',
    target_ip='10.0.2.2',
)

print(response)
print(response.sender_ip)