# Changelog

## development

- Add `sock` argument to `request` and `arequest` functions.
- Add `timeout` argument to `request` and `arequest` functions.
- Add `MockSocket` class for better unit testing.
- Change signature of `sync_send_arp` and `async_send_arp` functions, now they accept the `stream` argument.