import os
import pandas as pd
from encryptions import aes_encrypt, rsa_generate_keys, rsa_encrypt, chacha_encrypt
from Crypto.Random import get_random_bytes


def save_encrypted_files():
    datasets = [
        "data/customers-100.csv",
        "data/customers-1000.csv",
        "data/customers-10000.csv",
        "data/customers-100000.csv",
    ]
    output_folder = "encrypted_files"
    os.makedirs(output_folder, exist_ok=True)

    for dataset_path in datasets:
        dataset_name = os.path.basename(dataset_path).split(".")[0]
        print(f"Encrypting dataset: {dataset_path}")

        # Read and prepare the data
        data = pd.read_csv(dataset_path).to_csv(index=False).encode('utf-8')

        # AES Encryption
        print("\nAES Encryption")
        aes_key = get_random_bytes(32)  # 256-bit AES key
        aes_ciphertext, aes_iv, aes_tag = aes_encrypt(data, aes_key)
        aes_output_path = os.path.join(output_folder, f"{dataset_name}_aes.enc")
        with open(aes_output_path, "wb") as f:
            f.write(aes_ciphertext)
        print(f"Saved AES-encrypted file: {aes_output_path}")

        # RSA Encryption (Hybrid - Encrypt only the AES key)
        print("\nRSA Encryption (Hybrid)")
        rsa_private_key, rsa_public_key = rsa_generate_keys()
        rsa_encrypted_key = rsa_encrypt(aes_key, rsa_public_key)
        rsa_output_path = os.path.join(output_folder, f"{dataset_name}_rsa_aeskey.enc")
        with open(rsa_output_path, "wb") as f:
            f.write(rsa_encrypted_key)
        print(f"Saved RSA-encrypted AES key: {rsa_output_path}")

        # ChaCha20-Poly1305 Encryption
        print("\nChaCha20-Poly1305 Encryption")
        chacha_key = get_random_bytes(32)  # 256-bit ChaCha20 key
        chacha_ciphertext, chacha_nonce, chacha_tag = chacha_encrypt(data, chacha_key)
        chacha_output_path = os.path.join(output_folder, f"{dataset_name}_chacha.enc")
        with open(chacha_output_path, "wb") as f:
            f.write(chacha_ciphertext)
        print(f"Saved ChaCha20-encrypted file: {chacha_output_path}")

    print("\nAll files encrypted and saved in the 'encrypted_files' folder.")


if __name__ == "__main__":
    save_encrypted_files()
