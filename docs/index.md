# Introduction

# aioarp

[![PyPI - Version](https://img.shields.io/pypi/v/aioarp.svg)](https://pypi.org/project/aioarp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioarp.svg)](https://pypi.org/project/aioarp)
[![coverage](https://img.shields.io/codecov/c/github/karosis88/aioarp/master)](https://app.codecov.io/gh/karosis88/aioarp)
![license](https://img.shields.io/github/license/karosis88/aioarp)

-----

**Table of Contents**

- [Installation](#installation)
- [ARP request](#how-to-send-arp-requests)
- [ARP response](#arp-response)

## Installation

```console
pip install aioarp
```

## How to send ARP requests

```py title="Sync" linenums="1" 
import aioarp
response = aioarp.request('10.0.2.2', 'enp0s3')
print(response.sender_mac)
ee:xx:aa:mm:pp:le  # mac address
```

```py title="trio" linenums="1"
import trio
import aioarp
response = trio.run(aioarp.arequest, '10.0.2.2', 'enp0s3')
```

```py title="asyncio" linenums="1"
import asyncio
import aioarp
response = asyncio.run(aioarp.arequest('10.0.2.2', 'enp0s3'))
```

This is the packet that was sent over the network.
```
Ethernet II, Src: PcsCompu (YOUR MAC), Dst: Broadcast (ff:ff:ff:ff:ff:ff)
    Destination: Broadcast (ff:ff:ff:ff:ff:ff)
    Source: PcsCompu (YOUR MAC)
    Type: ARP (0x0806)
Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: PcsCompu (YOUR MAC)
    Sender IP address: 10.0.2.15
    Target MAC address: Broadcast (ff:ff:ff:ff:ff:ff)
    Target IP address: 10.0.2.2
```

If you want, you can explicitly set all of the **ARP** headers. To do so, create the `ArpPacket` instance yourself and then ask `aioarp` to send that request.

```py title="Sending ARP packet directly" linenums="1"
import aioarp

arp_packet = aioarp.ArpPacket(
    hardware_type=aioarp.HardwareType.ethernet,
    protocol_type=aioarp.Protocol.ip,
    sender_mac='11:11:11:11:11:11',
    sender_ip='127.0.0.1',
    target_mac='11:11:11:11:11:11',
    target_ip='127.0.0.1')

response = aioarp.sync_send_arp(arp_packet)
```

This sends the same ARP request as your `ArpPacket` instance.

!!! note

    The **Hardware Size** and **Protocol Size** headers are automatically set depending on the hardware type and protocol used.

```
Address Resolution Protocol (request/gratuitous ARP)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    [Is gratuitous: True]
    Sender MAC address: Private_11:11:11 (11:11:11:11:11:11)
    Sender IP address: 127.0.0.1
    Target MAC address: Private_11:11:11 (11:11:11:11:11:11)
    Target IP address: 127.0.0.1
```

As you can see, the packet that was sent over the network was **identical** to
the packet that we created; you can pass **whatever** you want and build your own arp packet.

## ARP response

Let's try again with another arp request and see what we can do with the respone object.

```py linenums="1"
import aioarp
response = aioarp.request('10.0.2.2', 'enp0s3')
# The `sender_mac` header for arp responses, as we know, 
# indicates the actual answer to our question "Who has 10.0.2.2?" 
# That is the protocol implementation; 
# the other computer that responds should 
# set the sender_mac to the computer's mac address that we are looking for.
print(response.sender_mac)
# ee:xx:aa:mm:pp:le  # mac address of 10.0.2.2
```

Other headers such as `hardware_type`, `protocol_type`, and `operation` can also be seen. 

```py linenums="1"
response.opcode  # operation header
# Opcode.response  # This indicates that this is an arp response rather than a request.
response.protocol_length
# 4  This indicates that 4 bytes were used for the sender and target ips because we used ipv4, which is actually 4 bytes.
```
Each one has a distinct meaning, which can be found in [wikipedia](https://en.wikipedia.org/wiki/Address_Resolution_Protocol).

## Failed Responses

If the response is not received, aioarp should throw a `aioarp.NotFoundError` exception. 

This occurs when the default arp request `timeout expires`. The timeout is set to 5 by default, but it can be changed by passing the `timeout` argument to the `request` function.

```py title="Without timeout" linenums="1"
response = aioarp.request('10.0.2.25', 'enp0s3')
```

```py title="With timeout" linenums="1"
response = aioarp.request('10.0.2.25', 'enp0s3', timeout=0.5)
```
