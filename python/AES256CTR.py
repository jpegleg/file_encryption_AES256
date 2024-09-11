import sys
import hashlib
import time
import os
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def derive_key(password, salt, length=32):
    """Derives a cryptographic key from the password and salt using SHAKE-256."""
    return hashlib.shake_256(password + salt).digest(length)

def generate_nonce():
    """Generates an 8-byte nonce using timestamp and random data."""
    timestamp = int(time.time() * 1000)
    timestamp_bytes = timestamp.to_bytes(6, byteorder='little')
    random_bytes = os.urandom(2)
    return timestamp_bytes + random_bytes

def encrypt_file(input_file, output_file, key):
    """Encrypts the input file and writes the ciphertext to the output file."""
    nonce = generate_nonce()
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    with open(input_file, "rb") as f:
        data = f.read()
    ciphertext = cipher.encrypt(data)
    with open(output_file, "wb") as w:
        w.write(nonce)
        w.write(ciphertext)

def decrypt_file(input_file, output_file, key):
    """Decrypts the input file and writes the plaintext to the output file."""
    with open(input_file, "rb") as f:
        nonce = f.read(8)
        ciphertext = f.read()
    try:
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        with open(output_file, "wb") as w:
            w.write(plaintext)
    except (ValueError, KeyError) as e:
        print(f"Decryption failed: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 5:
        print("Usage: <script> <input_file> <output_file> <sampler_file> <-d or -e>")
        sys.exit(1)

    ftarget = sys.argv[1]
    wtarget = sys.argv[2]
    sampler = sys.argv[3]
    dflag = sys.argv[4]

    with open(sampler, "rb") as s:
        skey = s.read()

    password = skey + getpass("Enter password: ").encode()
    key = derive_key(password, skey, 32)

    if dflag == "-d":
        decrypt_file(ftarget, wtarget, key)
    else:
        encrypt_file(ftarget, wtarget, key)

if __name__ == "__main__":
    main()
