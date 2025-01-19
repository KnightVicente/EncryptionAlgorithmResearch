import pandas as pd
import time
import base64
import os
import psutil
import threading
from encryptions import aes_encrypt, aes_decrypt, rsa_generate_keys, rsa_encrypt, rsa_decrypt, chacha_encrypt, chacha_decrypt

# Function to monitor performance
def monitor_performance():
    process = psutil.Process()
    cpu_usage = process.cpu_percent(interval=None)  # CPU usage
    memory_usage = process.memory_info().rss / (1024 ** 2)  # Convert to MB
    print(f"Monitoring - CPU: {cpu_usage:.2f}%, Memory: {memory_usage:.2f} MB")  # Debug print
    return cpu_usage, memory_usage

def monitor_cpu_usage(interval=0.1):
    """Continuously measure CPU usage."""
    cpu_samples = []

    def sample():
        while running[0]:
            cpu_samples.append(psutil.cpu_percent(interval=None))
            time.sleep(interval)

    running = [True]
    thread = threading.Thread(target=sample)
    thread.start()
    return cpu_samples, running, thread

def measure_cpu_during_operation(operation, interval=0.1):
    """
    Measure system-wide average CPU usage during the execution of an operation.
    """
    num_cores = psutil.cpu_count(logical=True)  # Total logical cores

    # Start measuring before operation
    cpu_start = psutil.cpu_percent(interval=None)

    start_time = time.time()

    # Perform the operation
    result = operation()

    # Briefly sample CPU usage after operation
    elapsed_time = time.time() - start_time
    cpu_end = psutil.cpu_percent(interval=interval)

    # Calculate average CPU usage
    avg_cpu = ((cpu_start + cpu_end) / 2) / num_cores if elapsed_time > 0 else 0

    return result, avg_cpu

# Save metrics and results
def log_metrics(folder, dataset_name, algorithm, metrics, first_run=False):
    os.makedirs(folder, exist_ok=True)
    log_file = os.path.join(folder, f"{dataset_name}_metrics.csv")
    df = pd.DataFrame([metrics])

    # Write header only if this is the first run
    if first_run or not os.path.exists(log_file):
        df.to_csv(log_file, index=False, mode='w')  # Overwrite if first run
    else:
        df.to_csv(log_file, index=False, mode='a', header=False)  # Append data
    print(f"Metrics saved in {log_file}")

# Read CSV file and convert to bytes
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_csv(index=False).encode('utf-8')


# Experiment function
def experiment(file_path):
    dataset_name = os.path.basename(file_path).split(".")[0]
    print(f"Testing encryption algorithms on dataset: {file_path}")
    data = read_csv(file_path)
    results_folder = "results"

    # AES Experiment
    print("\nAES Encryption")
    operation = lambda: aes_encrypt(data)
    (aes_ciphertext, aes_key, aes_iv, aes_tag), aes_cpu_enc = measure_cpu_during_operation(operation)

    operation = lambda: aes_decrypt(aes_ciphertext, aes_key, aes_iv, aes_tag)
    aes_plaintext, aes_cpu_dec = measure_cpu_during_operation(operation)

    assert aes_plaintext == data, "AES decryption failed!"
    log_metrics(results_folder, dataset_name, "AES", {
        "Algorithm": "AES",
        "Encryption CPU (%)": aes_cpu_enc,
        "Decryption CPU (%)": aes_cpu_dec,
        # Other metrics (time, memory) can be added here
    })

    # RSA Experiment
    print("\nRSA Encryption")
    rsa_private_key, rsa_public_key = rsa_generate_keys()

    operation = lambda: rsa_encrypt(data, rsa_public_key)
    (rsa_encrypted_key, rsa_ciphertext, rsa_iv, rsa_tag), rsa_cpu_enc = measure_cpu_during_operation(operation)

    operation = lambda: rsa_decrypt(rsa_encrypted_key, rsa_ciphertext, rsa_iv, rsa_tag, rsa_private_key)
    rsa_plaintext, rsa_cpu_dec = measure_cpu_during_operation(operation)

    assert rsa_plaintext == data, "RSA decryption failed!"
    log_metrics(results_folder, dataset_name, "RSA", {
        "Algorithm": "RSA",
        "Encryption CPU (%)": rsa_cpu_enc,
        "Decryption CPU (%)": rsa_cpu_dec,
        # Other metrics (time, memory) can be added here
    })

    # ChaCha20-Poly1305 Experiment
    print("\nChaCha20-Poly1305 Encryption")
    operation = lambda: chacha_encrypt(data)
    (chacha_ciphertext, chacha_key, chacha_nonce, chacha_tag), chacha_cpu_enc = measure_cpu_during_operation(operation)

    operation = lambda: chacha_decrypt(chacha_ciphertext, chacha_key, chacha_nonce, chacha_tag)
    chacha_plaintext, chacha_cpu_dec = measure_cpu_during_operation(operation)

    assert chacha_plaintext == data, "ChaCha20 decryption failed!"
    log_metrics(results_folder, dataset_name, "ChaCha20-Poly1305", {
        "Algorithm": "ChaCha20-Poly1305",
        "Encryption CPU (%)": chacha_cpu_enc,
        "Decryption CPU (%)": chacha_cpu_dec,
        # Other metrics (time, memory) can be added here
    })

# Main script
if __name__ == "__main__":
    datasets = ["data/customers-100.csv", "data/customers-1000.csv", "data/customers-10000.csv"]

    for dataset in datasets:
        experiment(dataset)
