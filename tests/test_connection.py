import asyncio
import os
from asyncio import ensure_future
from ssl import SSLContext
from tempfile import TemporaryDirectory

import pytest
from aapns.api import create_client
from aapns.config import Server
from aapns.errors import BadDeviceToken
from aapns.models import Alert, Notification
from tests.fake_apns_server import start_fake_apns_server
from tests.fake_client_cert import create_client_cert

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def auto_close(event_loop):
    closeables = []
    try:
        yield lambda x: closeables.append(x) or x
    finally:
        for closeable in closeables:
            await closeable.close()


@pytest.fixture
def client_cert_path():
    with TemporaryDirectory() as workspace:
        path = os.path.join(workspace, "cert.pem")
        with open(path, "wb") as fobj:
            fobj.write(create_client_cert())
        yield path


async def test_bad_device_id(client):
    with pytest.raises(BadDeviceToken):
        await client.send_notification("does not exist", Notification(Alert("test")))
