import os
import pandas as pd
import psutil
import time
from encryptions import aes_encrypt, aes_decrypt, rsa_generate_keys, rsa_encrypt, rsa_decrypt, chacha_encrypt, chacha_decrypt
from Crypto.Random import get_random_bytes

def measure_time_and_memory(operation):
    """Measure time and memory usage of an operation."""
    process = psutil.Process()
    mem_before = process.memory_info().rss / (1024 ** 2)  # Memory in MB

    start_time = time.perf_counter()
    result = operation()
    elapsed_time = time.perf_counter() - start_time

    mem_after = process.memory_info().rss / (1024 ** 2)  # Memory in MB
    peak_memory = max(mem_before, mem_after)

    return result, elapsed_time, peak_memory

def experiment(file_path, num_runs=10):
    dataset_name = os.path.basename(file_path).split(".")[0]
    print(f"Testing encryption algorithms on dataset: {file_path}")
    data = pd.read_csv(file_path).to_csv(index=False).encode('utf-8')
    results_folder = "results"
    os.makedirs(results_folder, exist_ok=True)

    all_metrics = []

    for run in range(1, num_runs + 1):
        print(f"\nRun {run}/{num_runs}")

        # AES Experiment
        print("\nAES Encryption")
        aes_key = get_random_bytes(32)  # 256-bit AES key
        aes_key_size = 256  # bits

        operation = lambda: aes_encrypt(data, aes_key)
        aes_result, aes_enc_time, aes_mem = measure_time_and_memory(operation)

        operation = lambda: aes_decrypt(*aes_result, aes_key)
        _, aes_dec_time, aes_dec_mem = measure_time_and_memory(operation)

        all_metrics.append({
            "Run": run,
            "Algorithm": "AES",
            "Key Size (bits)": aes_key_size,
            "Encryption Time (s)": aes_enc_time,
            "Decryption Time (s)": aes_dec_time,
            "Memory Usage (MB)": aes_mem,
            "Security Level": "High (128-bit security)",
        })

        # RSA Experiment (Hybrid Encryption)
        print("\nRSA Encryption (Hybrid)")
        rsa_private_key, rsa_public_key = rsa_generate_keys()
        rsa_key_size = 2048  # bits

        aes_key = get_random_bytes(32)  # Generate a 256-bit AES key

        operation = lambda: rsa_encrypt(aes_key, rsa_public_key)
        rsa_encrypted_key, rsa_enc_time, rsa_mem = measure_time_and_memory(operation)

        operation = lambda: aes_encrypt(data, aes_key)
        aes_result, aes_enc_time_2, aes_mem_2 = measure_time_and_memory(operation)

        operation = lambda: rsa_decrypt(rsa_encrypted_key, rsa_private_key)
        rsa_decrypted_key, rsa_dec_time, rsa_dec_mem = measure_time_and_memory(operation)

        operation = lambda: aes_decrypt(*aes_result, rsa_decrypted_key)
        _, aes_dec_time, aes_dec_mem = measure_time_and_memory(operation)

        all_metrics.append({
            "Run": run,
            "Algorithm": "RSA (Hybrid)",
            "Key Size (bits)": rsa_key_size,
            "Encryption Time (s)": rsa_enc_time + aes_enc_time_2,
            "Decryption Time (s)": rsa_dec_time + aes_dec_time,
            "Memory Usage (MB)": max(rsa_mem, aes_mem_2),
            "Security Level": "High (based on key size + AES strength)",
        })

        # ChaCha20-Poly1305 Experiment
        print("\nChaCha20-Poly1305 Encryption")
        chacha_key = get_random_bytes(32)  # 256-bit key
        chacha_key_size = 256  # bits

        operation = lambda: chacha_encrypt(data, chacha_key)
        chacha_result, chacha_enc_time, chacha_mem = measure_time_and_memory(operation)

        operation = lambda: chacha_decrypt(*chacha_result, chacha_key)
        _, chacha_dec_time, chacha_dec_mem = measure_time_and_memory(operation)

        all_metrics.append({
            "Run": run,
            "Algorithm": "ChaCha20-Poly1305",
            "Key Size (bits)": chacha_key_size,
            "Encryption Time (s)": chacha_enc_time,
            "Decryption Time (s)": chacha_dec_time,
            "Memory Usage (MB)": chacha_mem,
            "Security Level": "High (128-bit security)",
        })

    # Save Results
    results_file = os.path.join(results_folder, f"{dataset_name}_metrics.csv")
    pd.DataFrame(all_metrics).to_csv(results_file, index=False)
    print(f"Results saved in {results_file}")
