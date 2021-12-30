from uuid import uuid4

import pytest
from fastapi import HTTPException, status

from treasurehunt.auth.handlers import AuthHandler


def test_auth_handler_hash_flow_ok():
    # given
    auth_handler = AuthHandler()
    given_password = f"given-password-{uuid4()}"
    # when
    received_hash = auth_handler.get_password_hash(given_password)
    password_verified = auth_handler.verify_password(given_password, received_hash)
    # then
    assert password_verified


def test_auth_handler_hash_flow_fake_password():
    # given
    auth_handler = AuthHandler()
    given_password = f"given-password-{uuid4()}"
    given_fake_password = f"given-password-{uuid4()}"
    # when
    received_hash = auth_handler.get_password_hash(given_password)
    password_verified = auth_handler.verify_password(given_fake_password, received_hash)
    # then
    assert not password_verified


def test_auth_handler_token_flow_ok():
    # given
    auth_handler = AuthHandler()
    given_user_id = f"given-user-id-{uuid4()}"
    # when
    received_token = auth_handler.encode_token(given_user_id)
    received_user_id = auth_handler.decode_token(received_token)
    # then
    assert received_user_id == given_user_id


def test_auth_handler_token_flow_fake_token():
    # given
    auth_handler = AuthHandler()
    given_user_id = f"given-user-id-{uuid4()}"
    given_fake_user_id = f"given-user-id-{uuid4()}"
    # when
    received_fake_token = auth_handler.encode_token(given_fake_user_id)
    received_user_id = auth_handler.decode_token(received_fake_token)
    # then
    assert received_user_id != given_user_id


def test_auth_handler_token_flow_invalid_token():
    # given
    auth_handler = AuthHandler()
    given_fake_token = "given_fake_token"
    # when
    with pytest.raises(HTTPException) as err:
        auth_handler.decode_token(given_fake_token)
    # then
    assert err.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid" in err.value.detail


def test_auth_handler_token_flow_signature_has_expired():
    # given
    auth_handler = AuthHandler()
    given_expired_token = (
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDA3NjQyNjQsImlhdCI6MTY0MDc2Mzk"
        "2NCwic3ViIjoiZ2l2ZW4tdXNlci1pZC1hYzZkNGVjNC1iMjcwLTQ3YWItYjE4NC0xNWEwZjBmYmMyYWY"
        "ifQ.a_lsB5N91oNwKNx7tU-QrFcngtT_noY1ncn-2pYt-lA"
    )
    # when
    with pytest.raises(HTTPException) as err:
        auth_handler.decode_token(given_expired_token)
    # then
    assert err.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "expired" in err.value.detail
