from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

key_length = 1024


def generate_keys():
    # Generating private key (RsaKey object) of key length of 1024 bits
    private_key = RSA.generate(key_length)
    # Generating the public key (RsaKey object) from the private key
    public_key = private_key.publickey()
    print(type(private_key), type(public_key))
    # Converting the RsaKey objects to string
    private_pem = private_key.exportKey().decode()
    public_pem = public_key.export_key().decode()
    print(type(private_pem), type(public_pem))
    return private_pem, public_pem
