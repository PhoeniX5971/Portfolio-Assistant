import jwt

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz8ao5b1fwvfvo2y/AlqM
G9Kkmqp+QM8xASCYuSDmv8c5XPhIhtdm9DJEyvqtedlvC4JZowzd+Y0DaQkjHlE5
QgrqGkroNATIZDG0tq5e0gK0ViFv2jbQIJDyE8rS2EHRkzOFzneA0ormcEN1PY+G
LnFxDZwTHNMlUYEHhfTIwX9cTvmcZta40ychZrfz9Cp4GvWsCc9YeAUdI7M8r4lC
Y2QGeoywipjE3SWCYF48rRV7dWiMNw+RKyz+MP0WEZWLwGs8fJvlFq+Tvxwq8jGQ
8G88ixXo0q/4onSuU/dmGkwwkCisbwMolpNzJnDEsiz+JcEn2XuHoRXjulKKVjbj
BwIDAQAB
-----END PUBLIC KEY-----"""


# You don’t need to import InvalidTokenError separately, just catch jwt.PyJWTError
def verify_token(token: str) -> bool:
    try:
        jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer="next-app",
            options={"verify_aud": False},  # only if you don’t have audience
        )
        return True
    except jwt.PyJWTError as e:  # catch all decode/validation errors
        print(f"Auth Error: {e}")
        return False
