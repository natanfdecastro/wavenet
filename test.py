# RSA_cryptography.py
# Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

# The message to be encrypted
message = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x00\x011\x9a\xc4\xc9\x87jm\x10W\x11|\xa4\xed\xab\xe2\xb8\x00\x00\x00\x00\x00\xfa6T\xf4Vpu\x0c\t\xde(j\x80=\x1d\x00\x1da\xacw\xeb\xd3\xab6|\x96\xb0\x81\x92\x83\x91it\xe4&H}\xd9\x99\x9c\xd2\xa6\x1e\xd5\xc8\xc76\xa8i\xea\x1d\xfes\xe1\xbb\x17\'xL\xd9\x05v\xf5\xd2\xc5NF,\xf1\xfc\x8d\xad\xd8\xdc\xf3\x8f\xbb\x83\x19k\xb1~j3\x99\xb7\x98\n\xaf\x9d\\\x0esf\xe3&G\x86\t\xd8#b\xf5\xe1cK\x1a_\xa4t\xe3\xf8\xb8\x01\x8a\xa9\xf1\x9a\xf4\x17\xb81\'\xed\x8d\x83\x90\x9a\xef\x82W\x83\x0eIj\xf2\x87l\xd6|\xf5\xad\xec\x19\x8f\xc7\r\xe3\x89\x00\xa5\xd0\xa8\x0e\x8a*\xe1,\x96R\x87\x18\xf9\xde\x0f(\x1d\xa67w\xd8\xcc\x0c\xfa\x8d\xe4\xbb\xeb\\\x1a\xd8\x9c\x80\x11\xa8\xf4I\xfc\xde\x7f\x1dD\xd6\x0cz\x1e\xbb=\xb2\x9b\x8aK\xe6\xc4\xc8*~N\x1c\x00\xde\xc7\xf9\x83\rK\x0c\xe2.\xdd\x832p\xd48\x9f\xd33nw\xecR\x9d\xd6T\xf2\xce\x0bz\xb6}b7c\xda\x93"\xe0F.\xf3'
# Generating private key (RsaKey object) of key length of 1024 bits
private_key = RSA.generate(4096)
private_key2 = RSA.generate(4096)
# Generating the public key (RsaKey object) from the private key
public_key = private_key.publickey()
public_key2 = private_key2.publickey()
print(type(private_key), type(public_key))
# Converting the RsaKey objects to string
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()
print(type(private_pem), type(public_pem))

# Importing keys from files, converting it into the RsaKey object
pr_key = private_key
pu_key = public_key
# Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key=pu_key)
# Encrypting the message with the PKCS1_OAEP object
cipher_text = cipher.encrypt(message)
print(cipher_text)
# Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key=pr_key)
# Decrypting the message with the PKCS1_OAEP object
decrypted_message = decrypt.decrypt(cipher_text)
print(decrypted_message)