import sys
import hashlib
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def derive_key(password, salt, length=32):
    """Derives a cryptographic key from the password and salt using SHAKE-256."""
    return hashlib.shake_256(password + salt).digest(length)

def encrypt_file(input_file, output_file, key):
    """Encrypts the input file and writes the ciphertext to the output file."""
    nonce = get_random_bytes(8)
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
        cipherd = AES.new(key, AES.MODE_CTR, nonce=nonce)
        plaintext = cipherd.decrypt(ciphertext)
        with open(output_file, "wb") as w:
            w.write(plaintext)
    except (ValueError, OSError) as e:
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

    password = skey + getpass().encode()
    key = derive_key(password, skey, 32)

    if dflag == "-d":
        decrypt_file(ftarget, wtarget, key)
    else:
        encrypt_file(ftarget, wtarget, key)

if __name__ == "__main__":
    main()
