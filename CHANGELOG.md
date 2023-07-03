# Changelog

## 0.0.11 (3/7/2023)

- Use `getmac` package for mac address detecting.
- Add `send`, `disable` and `spoof` commands for the CLI. (#33)
- Make the `interface` argument for the `build_arp_packet` function optional. (#32)

## 0.0.10 (1/7/2023)

- Add `Packet` base class. (#28)
- Change `Protocol` to `ProtocolType`. (#30)
- Validate `sender_ip` of the ARP response packet.

# 0.0.9 (27/6/2023)

- Make `interface` argument optional. (#23)
- Move `Stream` creation from `request` to `sync_send_arp`. (#24)

# 0.0.8 (21/6/2023) 

- Add `wait_response` argument to `sync_send_arp` and `async_send_arp`. (#13)

# 0.0.7 (16/6/2023)

- Add basic API documentation. (#7)

# 0.0.5 (12/6/2023)

- Add simple cli.

# 0.0.3 (5/6/2023)

- Add `sock` argument to `request` and `arequest` functions.
- Add `timeout` argument to `request` and `arequest` functions.
- Add `MockSocket` class for better unit testing.
- Change signature of `sync_send_arp` and `async_send_arp` functions, now they accept the `stream` argument.
