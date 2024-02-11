import uuid


def validate_uuid(_uuid: str) -> bool:
    try:
        uuid.UUID(_uuid)
    except Exception:
        return False
    else:
        return True
