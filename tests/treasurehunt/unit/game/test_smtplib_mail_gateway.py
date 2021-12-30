from uuid import uuid4

import pytest

from tests.mailhog_client import MailHogClient
from treasurehunt.game.mail_gateway import SMTPlibMailGateway
from treasurehunt.game.schemas import Hunter


@pytest.mark.asyncio
async def test_send_mail_ok(mailhog_client: MailHogClient, test_hunter: Hunter):
    # given
    given_subject = "Test mail"
    given_message = f"Message body {uuid4()}"
    gateway = SMTPlibMailGateway()
    # when
    await gateway.send_mail(
        subject=given_subject, message=given_message, recipient=test_hunter.email
    )
    # then
    messages = await mailhog_client.get_messages()
    assert len(messages.items) == 1, "More than one message was send"
    assert test_hunter.email in messages.items[0].raw.recipients
    assert given_subject in messages.items[0].raw.data
    assert given_message in messages.items[0].raw.data
