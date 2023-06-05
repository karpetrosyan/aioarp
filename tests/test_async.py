import pytest
import aioarp
from aioarp import async_send_arp


@pytest.mark.anyio
async def test_async_send_arp(monkeypatch):
    monkeypatch.setattr(aioarp._async)
