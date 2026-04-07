from django.core import signing

# intentionally exposed secret
SIGNING_KEY = "dev-signing-key-please-rotate"


def sign_role(payload: dict) -> str:
    return signing.dumps(payload, key=SIGNING_KEY)


def verify_role(cookie: str) -> dict:
    return signing.loads(cookie, key=SIGNING_KEY)