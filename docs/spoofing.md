
# Arp spoofing

In computer networking, ARP spoofing, ARP cache poisoning, or ARP poison routing, is a technique by which an attacker sends Address Resolution Protocol messages onto a local area network. Generally, the aim is to associate the attacker's MAC address with the IP address of another host, such as the default gateway, causing any traffic meant for that IP address to be sent to the attacker instead.

ARP spoofing is supported by default in `aioarp`, either through the cli or the `aioarp`'s API.

To perform simple ARP spoofing, we must first understand how the `spoof` command works.

Assume our IP address in our local network is **192.168.0.85**, and our target IP address in the same network is **192.168.0.81**.

The target IP address recognizes **192.168.0.1** as our gateway and uses that IP to connect to the internet.

But how did he get **192.168.0.1**'s mac address? He simply makes an ARP request. 

So he sends the ARP request and waits for an ARP response, but ARP responses can also be sent in the absence of any ARP requests, which is known as `Gratuitous ARP`.

ARP spoofing employs Gratuitous ARP to convince our target IP that the mac address for the gateway is what we sent in the ARP response.


Example:
```shell title="spoof command"
$ aioarp spoof 192.168.0.81 192.168.0.1 11:11:11:11:11:11 --seconds 10
```

Where...

- **192.168.0.81** is a target IP
- **192.168.0.81** is a gateway
- **11:11:11:11:11:11* fake mac address


In other words, `#!shell aioarp spoof arg1 arg2 arg3` means "tell arg1 that arg2's mac address is arg3".

Now the 192.168.0.81 will think that mac address of 192.168.0.1 is "11:11:11:11:11:11" so any traffic he tries to send via that mac address gonna be dropped, and the target ip address will not have access to the internet. We can also use more meaningfull fake mac addresses, such as our mac address, to see any traffic sent by the target ip.

Also, if you just want to disable internet access for a specific IP address, you can use a special command that is similar to the spoof command but does not require the mac address.

```shell title="disable command"
$ aioarp disable 192.168.0.81 192.168.0.1 enp0s3 --seconds 10
```

If you send a broadcast ARP message, you can also disable internet access for the entire network, as shown here.

```py title="Broadcast ARP Spoofing" linenums="1"
import aioarp

arp_packet = aioarp.build_arp_request('0.0.0.0')
arp_packet.sender_mac = '11:11:11:11:11:11'
arp_packet.sender_ip = '192.168.0.1'
arp_packet.target_mac = 'ff:ff:ff:ff:ff:ff'

aioarp.sync_send_arp(arp_packet)
```

or using aioarp's cli

```
$ aioarp spoof 0.0.0.0 192.168.0.1 11:11:11:11:11:11 --seconds 10
```

As you can see, we simply want to set the target IP to **0.0.0.0**, which is a wildcard for broadcast requests.