from datetime import datetime, timedelta

from app.security import hash_password, verify_password


def test_password_hash_round_trip() -> None:
    stored = hash_password("StrongPass123!")
    assert stored != "StrongPass123!"
    assert verify_password("StrongPass123!", stored)
    assert not verify_password("wrong", stored)


def test_deadline_math() -> None:
    accepted = datetime.utcnow()
    assert accepted + timedelta(days=7) > accepted