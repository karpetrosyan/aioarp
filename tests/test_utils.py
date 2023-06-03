from aioarp import enforce_ip, enforce_mac, parse_ip, parse_mac


def test_enforce_mac():
    encoded = enforce_mac('00:00:00:00:00:00')
    assert False not in [byte == 0 for byte in encoded]


def test_enforce_ip():
    encoded = enforce_ip('127.0.0.1')
    assert encoded == bytes([127, 0, 0, 1])


def test_parse_mac():
    mac = parse_mac(bytes([0, 0, 0, 0, 0, 0]))
    assert mac == '00:00:00:00:00:00'


def test_parse_ip():
    parsed = parse_ip(bytes([127, 0, 0, 1]))
    assert parsed == '127.0.0.1'
