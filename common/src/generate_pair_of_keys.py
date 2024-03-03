import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_pair_of_keys():
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Extract public key
    public_key = private_key.public_key()

    # Serialize keys to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    try:
        os.remove('private_access_jwt_key.pem')
        os.remove('public_access_jwt_key.pem')
    except FileNotFoundError:
        pass
    open('private_access_jwt_key.pem', 'w').write(private_pem.decode())
    open('public_access_jwt_key.pem', 'w').write(public_pem.decode())

    print('JWT Keys generated successfully')


if __name__ == '__main__':
    generate_pair_of_keys()
