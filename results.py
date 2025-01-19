import pandas as pd
import time
import base64
import os
from encryptions import aes_encrypt, aes_decrypt, rsa_generate_keys, rsa_encrypt, rsa_decrypt, chacha_encrypt, chacha_decrypt

# Function to save results
def save_results(algorithm, dataset_name, ciphertext, folder="results"):
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
    output_file = os.path.join(folder, f"{algorithm}_{dataset_name}_ciphertext.txt")
    with open(output_file, "w") as f:
        f.write(ciphertext)
    print(f"Saved {algorithm} ciphertext for {dataset_name} in {output_file}")

# Read CSV file and convert to bytes
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_csv(index=False).encode('utf-8')

# Experiment function
def experiment(file_path):
    dataset_name = os.path.basename(file_path).split(".")[0]
    print(f"Testing encryption algorithms on dataset: {file_path}")
    data = read_csv(file_path)

    # AES Experiment
    print("\nAES Encryption")
    aes_ciphertext, aes_key, aes_iv, aes_tag = aes_encrypt(data)
    aes_ciphertext_base64 = base64.b64encode(aes_ciphertext).decode('utf-8')  # Convert to Base64
    save_results("AES", dataset_name, aes_ciphertext_base64)

    aes_plaintext = aes_decrypt(aes_ciphertext, aes_key, aes_iv, aes_tag)
    assert aes_plaintext == data, "AES decryption failed!"

    # RSA Experiment (Hybrid Encryption)
    print("\nRSA Encryption")
    rsa_private_key, rsa_public_key = rsa_generate_keys()
    rsa_encrypted_key, rsa_ciphertext, rsa_iv, rsa_tag = rsa_encrypt(data, rsa_public_key)
    rsa_ciphertext_base64 = base64.b64encode(rsa_ciphertext).decode('utf-8')  # Convert to Base64
    save_results("RSA", dataset_name, rsa_ciphertext_base64)

    rsa_plaintext = rsa_decrypt(rsa_encrypted_key, rsa_ciphertext, rsa_iv, rsa_tag, rsa_private_key)
    assert rsa_plaintext == data, "RSA decryption failed!"

    # ChaCha20-Poly1305 Experiment
    print("\nChaCha20-Poly1305 Encryption")
    chacha_ciphertext, chacha_key, chacha_nonce, chacha_tag = chacha_encrypt(data)
    chacha_ciphertext_base64 = base64.b64encode(chacha_ciphertext).decode('utf-8')  # Convert to Base64
    save_results("ChaCha20-Poly1305", dataset_name, chacha_ciphertext_base64)

    chacha_plaintext = chacha_decrypt(chacha_ciphertext, chacha_key, chacha_nonce, chacha_tag)
    assert chacha_plaintext == data, "ChaCha20 decryption failed!"

# Main script
if __name__ == "__main__":
    datasets = ["data/customers-100.csv", "data/customers-1000.csv", "data/customers-10000.csv"]

    for dataset in datasets:
        experiment(dataset)
