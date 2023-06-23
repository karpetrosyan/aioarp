# aioarp

[![PyPI - Version](https://img.shields.io/pypi/v/aioarp.svg)](https://pypi.org/project/aioarp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioarp.svg)](https://pypi.org/project/aioarp)
[![coverage](https://img.shields.io/codecov/c/github/karosis88/aioarp/master)](https://app.codecov.io/gh/karosis88/aioarp)
![license](https://img.shields.io/github/license/karosis88/aioarp)

-----

**Table of Contents**

- [Installation](#installation)
- [Documentation](#documentation)
- [ARP requests](#how-to-send-arp-requests)
- [License](#license)

## Installation

```console
pip install aioarp
```

## Documentation
[Click here](https://karosis88.github.io/aioarp/)

## How to send ARP requests

### Sync
```py
import aioarp
response = aioarp.request('10.0.2.2', 'enp0s3')
print(response.sender_mac)
# ee:xx:aa:mm:pp:le mac address
```

### Async [trio or asyncio]
```py
import trio
import aioarp
response = trio.run(aioarp.arequest, '10.0.2.2', 'enp0s3')
```

```py
import asyncio
import aioarp
response = asyncio.run(aioarp.arequest('10.0.2.2', 'enp0s3'))
```

Or without specifying an interface parameter

```
response = aioarp.request('10.0.2.2')
```

## License

`aioarp` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

