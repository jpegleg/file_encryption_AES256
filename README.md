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

Usage example of encrypting a package list:

```
19:39:21 <@x://home/linux
0 > AES256CTR packages_installed_20241109193916.dpkg.out packages_installed_20241109193916.dpkg.out.enc 092963537.sample -e
Enter password:
```

And then collecting checksums of ciphertext and plaintext, then removing the original file

```
19:41:04 <@x://home/linux
0 > sha384sum packages_installed_20241109193916.dpkg.out.enc packages_installed_20241109193916.dpkg.out | tee packages_installed_20241109193916.dpkg.chksums.txt
30db19f6c916ed277d23769f543d73e165ba263d9fd47802f016fe00cf2324fc4d73bba7fb05e166fb6805a5e7b30013  packages_installed_20241109193916.dpkg.out.enc
453621d43940020efb4dba3be7156c7b4b173a03d86247cf9aadf82d711680958700c0c20e7a99322eb7faa1a0af56a6  packages_installed_20241109193916.dpkg.out
19:42:20 <@x://home/linux
0 > sha256sum packages_installed_20241109193916.dpkg.out.enc packages_installed_20241109193916.dpkg.out | tee -a packages_installed_20241109193916.dpkg.chksums.txt
73b669d17c8320abc00be3e1adc0e99eb3e445d5bcf705be8964b35feb87038b  packages_installed_20241109193916.dpkg.out.enc
f16af258683130d18cb1ee1c678cbf2b821ce6f21ab71aa636c630f2a1793d3d  packages_installed_20241109193916.dpkg.out
19:43:32 <@x://home/linux
0 > b2sum packages_installed_20241109193916.dpkg.out.enc packages_installed_20241109193916.dpkg.out | tee -a packages_installed_20241109193916.dpkg.chksums.txt
e825e0cfed8c8196e8758121049ffe3e7523be5665cbd208484d3c2f7c14389f8b7824daa1f8f9193bc52894bfe38550d1f349da434b08276f39218d940c8e46  packages_installed_20241109193916.dpkg.out.enc
e6e57ea8f707f0afc3f3e974558be9329ecc8622377f40d735d96bc80116cf278b2d3d200c42e2748e3a51ac8e80b64dc4f855a398a33a1411ae7fd4f5386b5b  packages_installed_20241109193916.dpkg.out
19:44:10 <@x://home/linux
0 > bat packages_installed_20241109193916.dpkg.chksums.txt
───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: packages_installed_20241109193916.dpkg.chksums.txt
───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ 30db19f6c916ed277d23769f543d73e165ba263d9fd47802f016fe00cf2324fc4d73bba7fb05e166fb6805a5e7b30013  packages_installed_20241109193916.dpkg.out.enc
   2   │ 453621d43940020efb4dba3be7156c7b4b173a03d86247cf9aadf82d711680958700c0c20e7a99322eb7faa1a0af56a6  packages_installed_20241109193916.dpkg.out
   3   │ 73b669d17c8320abc00be3e1adc0e99eb3e445d5bcf705be8964b35feb87038b  packages_installed_20241109193916.dpkg.out.enc
   4   │ f16af258683130d18cb1ee1c678cbf2b821ce6f21ab71aa636c630f2a1793d3d  packages_installed_20241109193916.dpkg.out
   5   │ e825e0cfed8c8196e8758121049ffe3e7523be5665cbd208484d3c2f7c14389f8b7824daa1f8f9193bc52894bfe38550d1f349da434b08276f39218d940c8e46  packages_installed_20241109193916.dpkg.out.enc
   6   │ e6e57ea8f707f0afc3f3e974558be9329ecc8622377f40d735d96bc80116cf278b2d3d200c42e2748e3a51ac8e80b64dc4f855a398a33a1411ae7fd4f5386b5b  packages_installed_20241109193916.dpkg.out
───────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
19:45:54 <@x://home/linux
0 > rm packages_installed_20241109193916.dpkg.out
```

The `packages_installed_20241109193916.dpkg.chksums.txt` file is to be archived or stored elsewhere so we can confirm the ciphertext and plaintext are not tampered with later. 

To decrypt the example:

```
19:39:21 <@x://home/linux
0 > AES256CTR packages_installed_20241109193916.dpkg.out.enc packages_installed_20241109193916.dpkg.out 092963537.sample -d
Enter password:
```


#### Password and sample file management

The password isn't the secret to decrypt the file for these tools, the password is only part of the key material. The input password is combined with the sample file (salt file), and sent through SHAKE256. If either the password or the input sample are wrong, the data will not be decrypted. In CTR mode we want to rotate keys regularly because of the probabilities of exposure involved. Outside of the issue of secret management, the nonce is more likely to become a problem before the CTR key itself. The nonce cannot repeat, otherwise the security of that use is weakened. 

When using this dual input approach, we must select which input is to be considered the secret and which is to be considered the salt because we can do either with these tools. We can have the sample file be the secret while the password is a simple memorized phrase that the team knows, for example. Or we can have the sample files be a scheme generated based on age/work requests, even exposing these files to some extent, while the passwords used are strong and protected, managed from smartcards.

One approach is to generate a sample file for each dataset, so if we have 10 computers and 3 datasets, we might generate 3 sample files centrally then distribute the sample files to each of the 10 computers. Each dataset can have it's own sample file, separating the secret usage at the data level. The password can be the same or different between computers or datasets and can change on a separate interval than the sample files, reducing wasteful password resetting. Having two different mechanisms to effectively rotate the secret used in the symmetric encryption is a useful property.


