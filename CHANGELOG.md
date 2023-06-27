# Changelog

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
