# file_encryption_AES256

This project contains CLI tools to interactively encrypt files with AES256 in CTR mode.

⚠️ Security Warning: Hazmat! These tools are not the right tools to use for a complete or standard solution. They implement well tested libraries, but the use of those libraries is not a generic or standardized solution.

WARNING: AES in CTR mode does not provide non-malleability, so the ciphertext is not tamper resistent. Use with additional hashing and/or signing if malleability is a concern.

More to be added to this document soon!

## Nonces

The rust version has a stronger nonce, but both versions use a unix epoch nanoseconds truncated, combined with random bits.
This is an area of security risk, but also a neat feature. The files contain time data at the start of the ciphertext.

## Key material

The key material for these tools comes from combining two components, a key file on the disk, and CLI input from the user. Those
inputs are combined and input to a SHAKE256 XOF of the required length for AES256. This use of SHAKE might more optimally be
Aargon2 or HMAC, but these tools use the less security optimized but faster XOF, relying more on the security of having
two distinct key inputs.

WARNING: If bad passwords are used and bad sample files (key files) are used, the encryption is weak. 

TIP: I'm using `gold` from https://github.com/jpegleg/dwarven-toolbox/ to make a strong sample file, and then using different sample files for different use-cases/scopes. We can rotate the sample files and passwords independantly, changing either or both generates a new symmetric secret. We never need to observe or store the symmetric secret directly. Having a strong sample file helps make up for weaker human-used passwords. Enforcement is out of the scope of this tool and would likely be done by a wrapper script.

## Python

The python script version uses pycryptodome library (module).

## Rust

The rust program version uses the "aes" and "ctr" libraries (crates).
