import time
import jwt

def generate_jwt(user_uuid, signer, expiry_length=3600):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        'exp': now + expiry_length,
        # sub should match the service account's email address
        # 'sub': sa_email,
        'user_uuid': user_uuid
    }

    token = jwt.encode(signer, payload)

    return token
