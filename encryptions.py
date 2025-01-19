from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import ChaCha20_Poly1305

# AES Functions
def aes_encrypt(data, key):
    iv = get_random_bytes(12)  # 96-bit IV
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, iv, tag

def aes_decrypt(ciphertext, iv, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

# RSA Functions
def rsa_generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt(data, public_key):
    recipient_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(recipient_key)
    ciphertext = cipher.encrypt(data)
    return ciphertext

def rsa_decrypt(ciphertext, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# ChaCha20-Poly1305 Functions
def chacha_encrypt(data, key):
    nonce = get_random_bytes(12)  # 96-bit nonce
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, nonce, tag

def chacha_decrypt(ciphertext, nonce, tag, key):
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext
