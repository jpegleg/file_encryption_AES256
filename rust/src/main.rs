use aes::Aes256;
use ctr::cipher::{KeyIvInit, StreamCipher};
use ctr::Ctr64BE;
use rand::{RngCore, rngs::OsRng};
use rpassword::read_password;
use sha3::{Shake256, digest::{Update, ExtendableOutput, XofReader}};
use std::env;
use std::fs::File;
use std::io::{Read, Write};
use std::process;
use std::time::{SystemTime, UNIX_EPOCH};

type Aes256Ctr = Ctr64BE<Aes256>;

fn derive_key(password: &[u8], salt: &[u8], length: usize) -> Vec<u8> {
    let mut hasher = Shake256::default();
    hasher.update(password);
    hasher.update(salt);
    let mut reader = hasher.finalize_xof();
    let mut key = vec![0u8; length];
    XofReader::read(&mut reader, &mut key);
    key
}

fn generate_nonce() -> [u8; 16] {
    let mut nonce = [0u8; 16];

    // Reduce the chance of nonce re-use by using time + random data
    let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap();
    let timestamp_nanos = now.as_nanos();
    nonce[0..8].copy_from_slice(&timestamp_nanos.to_le_bytes()[0..8]);
    OsRng.fill_bytes(&mut nonce[8..16]);

    nonce
}

fn encrypt_file(input_file: &str, output_file: &str, key: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
    let mut file = File::open(input_file)?;
    let mut data = Vec::new();
    file.read_to_end(&mut data)?;

    let nonce = generate_nonce();

    let mut cipher = Aes256Ctr::new(key.into(), &nonce.into());
    cipher.apply_keystream(&mut data);

    let mut output = File::create(output_file)?;
    output.write_all(&nonce)?;
    output.write_all(&data)?;

    Ok(())
}

fn decrypt_file(input_file: &str, output_file: &str, key: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
    let mut file = File::open(input_file)?;
    let mut nonce = [0u8; 16];
    file.read_exact(&mut nonce)?;
    let mut data = Vec::new();
    file.read_to_end(&mut data)?;

    let mut cipher = Aes256Ctr::new(key.into(), &nonce.into());
    cipher.apply_keystream(&mut data);

    let mut output = File::create(output_file)?;
    output.write_all(&data)?;

    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 5 {
        eprintln!("Usage: {} <input_file> <output_file> <sampler_file> <-d or -e>", args[0]);
        process::exit(1);
    }

    let input_file = &args[1];
    let output_file = &args[2];
    let sampler_file = &args[3];
    let flag = &args[4];

    let mut skey = Vec::new();
    File::open(sampler_file)?.read_to_end(&mut skey)?;

    print!("Enter password: ");
    std::io::stdout().flush()?;
    let password = read_password()?;

    let key = derive_key(password.as_bytes(), &skey, 32);

    match flag.as_str() {
        "-d" => decrypt_file(input_file, output_file, &key)?,
        "-e" => encrypt_file(input_file, output_file, &key)?,
        _ => {
            eprintln!("Invalid flag. Use -d for decryption or -e for encryption.");
            process::exit(1);
        }
    }

    Ok(())
}
