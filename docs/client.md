# Requests

## Sending requests

```py title="request"
import aioarp

aioarp.request("enp0s3", "10.0.2.2")
```

This is simply sending the arp packet that searches the network for a mac address of the `10.0.2.2` ip using the interface that you provided.
You can also use a `timeout` to ensure that waiting for a response does not go on indefinitely.

```py title="timeout request"
aioarp.request("enp0s3", "10.0.2.2", timeout=0.5)
```

This method can also take the `sock` argument, which is a socket connection that will be used for IO operations. (useful for mocking)

## Asynchronous requests

It is very simple to switch from synchronous to asynchronous aioarp; simply use the await keyword and change request to arequest.

```py title="async request"
await arequest("enp0s3", "10.0.2.2")
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
aioarp.sync_send_arp(arp_packet, Stream("enp0s3"))
```

If the `ArpPacket` is too complicated for you, you can use the `build_arp_packet` function to generate an `ArpPacket` for you, which you can then modify.

```py title="build_arp_packet"
arp_packet = build_arp_packet('enp0s3', '10.0.2.2')
arp_packet.sender_ip
'10.0.2.2' 
```

`build_arp_packet` accepts only two arguments: interface and target IP address.