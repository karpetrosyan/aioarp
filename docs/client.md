# Requests

## Sending requests

```py title="request"
import aioarp

aioarp.request("10.0.2.2", "enp0s3")
```

This is simply sending the arp packet that searches the network for a mac address of the `10.0.2.2` ip using the interface that you provided.
You can also use a `timeout` to ensure that waiting for a response does not go on indefinitely.

```py title="timeout request"
aioarp.request("10.0.2.2", "enp0s3", timeout=0.5)
```

This function accepts the network interface that will be used to send the ARP request as the second argument.
However, interface is an optional parameter that can be ignored. if it is not passed, aioarp will look up your system's default interface and use it.

Example:

```py title="without specifying interface"
aioarp.request("10.0.2.2")
```

!!! note

    If the default network interface is not specified, Aioarp will use the `ip` command to find it.

You can also use the `wait_response` parameter to tell aioarp whether you need the response or not.
```py title="without waiting for a response"
aioarp.request("10.0.2.2", "enp0s3", wait_response=False)
```

!!! note

    When the `wait_response` argument is false, the `timeout` argument has no effect.

This method can also take the `sock` argument, which is a socket connection that will be used for IO operations. (useful for mocking)

## Asynchronous requests

It is very simple to switch from synchronous to asynchronous aioarp; simply use the await keyword and change request to arequest.

```py title="async request"
await arequest("10.0.2.2", "enp0s3")
```

Because the synchronous and asynchronous interfaces shared the same function signatures, all synchronous features worked as expected in asynchronous.

## Building requests

You may need to build your own ARP packet and set each ARP header to whatever you want; aioarp supports that behavior, and you can pass not only the target ip, but also the source ip, source mac, desctination mac, and so on.

```py
arp_packet = aioarp.ArpPacket(
         hardware_type=aioarp.HardwareType.ethernet,
         protocol_type=aioarp.Protocol.ip,
         sender_mac='11:11:11:11:11:11',
         sender_ip='127.0.0.1',
         target_mac='11:11:11:11:11:11',
         target_ip='127.0.0.1')
```

Now that you have your arp packet with all of the required headers, you can ask `aioarp` to send that request.

```py
aioarp.sync_send_arp(arp_packet, "enp0s3")
```

If the `ArpPacket` is too complicated for you, you can use the `build_arp_packet` function to generate an `ArpPacket` for you, which you can then modify.

```py title="build_arp_packet"
arp_packet = build_arp_packet('10.0.2.2', 'enp0s3')
arp_packet.sender_ip
'10.0.2.2' 
```

`build_arp_packet` accepts only two arguments: interface and target IP address.