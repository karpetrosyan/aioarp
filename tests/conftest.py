import pytest

import aioarp
from aioarp._mock import mock_get_default_interface
from aioarp._mock import mock_get_ip
from aioarp._mock import mock_get_mac

@pytest.fixture(scope='function', autouse=True)
def mock_ip_and_mac(monkeypatch):
    monkeypatch.setattr(aioarp._client, 'get_ip', mock_get_ip('127.0.0.1'))
    monkeypatch.setattr(aioarp._client, 'get_mac', mock_get_mac('11:11:11:11:11:11'))
    monkeypatch.setattr(aioarp, 'get_default_interface', mock_get_default_interface('enp0s3'))
    yield