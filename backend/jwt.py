import time


def generate_jwt(email, audience, expiry_length: int = 3600):
    now = int(time.time())

