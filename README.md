# file_encryption_AES256

This project contains CLI tools to interactively encrypt files with AES256 in CTR mode.

WARNING: AES in CTR mode does not provide non-malleability, so the ciphertext is not tamper resistent. Use with additional hashing and/or signing if malleability is a concern.

More to be added to this document soon!

## Nonces

## Key material

## Python

The python script version uses pycryptodome library (module).

## Rust

The rust program version uses the "aes" and "ctr" libraries (crates).
