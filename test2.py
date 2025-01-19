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

def measure_cpu_and_memory(operation, interval=0.2):
    """
    Measure process-specific CPU and memory usage during an operation.
    """
    process = psutil.Process()
    num_cores = psutil.cpu_count(logical=True)  # Total logical cores

    # Start measurements
    cpu_start = process.cpu_percent(interval=None)
    mem_start = process.memory_info().rss / (1024 ** 2)  # Memory in MB

    # Perform the operation
    start_time = time.time()
    result = operation()
    elapsed_time = time.time() - start_time

    # Sample after operation
    cpu_end = process.cpu_percent(interval=interval)
    mem_end = process.memory_info().rss / (1024 ** 2)

    # Normalize CPU usage to a single core
    avg_cpu = ((cpu_start + cpu_end) / 2) / num_cores if elapsed_time > 0 else 0

    # Average memory usage
    avg_mem = (mem_start + mem_end) / 2

    return result, avg_cpu, avg_mem, elapsed_time



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

# Read CSV file and convert to bytes
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_csv(index=False).encode('utf-8')


# Experiment function
def experiment(file_path, chunk_size=1024):
    dataset_name = os.path.basename(file_path).split(".")[0]
    print(f"Testing encryption algorithms on dataset: {file_path}")
    data = read_csv(file_path)

    # Split data into chunks
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    results_folder = "results"

    first_run = True  # Ensure CSV headers are written only once

    # AES Experiment
    print("\nAES Encryption")
    operation = lambda: [
        aes_encrypt(chunk) or time.sleep(0.01) for chunk in chunks  # Add delay during encryption
    ]
    aes_result, aes_cpu_enc, aes_mem_enc, aes_enc_time = measure_cpu_and_memory(operation)

    operation = lambda: [
        aes_decrypt(*chunk) or time.sleep(0.01) for chunk in aes_result  # Add delay during decryption
    ]
    _, aes_cpu_dec, aes_mem_dec, aes_dec_time = measure_cpu_and_memory(operation)

    log_metrics(results_folder, dataset_name, "AES", {
        "Algorithm": "AES",
        "Encryption Time (s)": aes_enc_time,
        "Decryption Time (s)": aes_dec_time,
        "Encryption CPU (%)": aes_cpu_enc,
        "Decryption CPU (%)": aes_cpu_dec,
        "Encryption Memory (MB)": aes_mem_enc,
        "Decryption Memory (MB)": aes_mem_dec,
    }, first_run=first_run)
    first_run = False

    # Similar adjustments for RSA and ChaCha20-Poly1305
    print("\nRSA Encryption")
    rsa_private_key, rsa_public_key = rsa_generate_keys()

    operation = lambda: [
        rsa_encrypt(chunk, rsa_public_key) or time.sleep(0.01) for chunk in chunks
    ]
    rsa_result, rsa_cpu_enc, rsa_mem_enc, rsa_enc_time = measure_cpu_and_memory(operation)

    operation = lambda: [
        rsa_decrypt(*chunk, rsa_private_key) or time.sleep(0.01) for chunk in rsa_result
    ]
    _, rsa_cpu_dec, rsa_mem_dec, rsa_dec_time = measure_cpu_and_memory(operation)

    log_metrics(results_folder, dataset_name, "RSA", {
        "Algorithm": "RSA",
        "Encryption Time (s)": rsa_enc_time,
        "Decryption Time (s)": rsa_dec_time,
        "Encryption CPU (%)": rsa_cpu_enc,
        "Decryption CPU (%)": rsa_cpu_dec,
        "Encryption Memory (MB)": rsa_mem_enc,
        "Decryption Memory (MB)": rsa_mem_dec,
    })

    print("\nChaCha20-Poly1305 Encryption")
    operation = lambda: [
        chacha_encrypt(chunk) or time.sleep(0.01) for chunk in chunks
    ]
    chacha_result, chacha_cpu_enc, chacha_mem_enc, chacha_enc_time = measure_cpu_and_memory(operation)

    operation = lambda: [
        chacha_decrypt(*chunk) or time.sleep(0.01) for chunk in chacha_result
    ]
    _, chacha_cpu_dec, chacha_mem_dec, chacha_dec_time = measure_cpu_and_memory(operation)

    log_metrics(results_folder, dataset_name, "ChaCha20-Poly1305", {
        "Algorithm": "ChaCha20-Poly1305",
        "Encryption Time (s)": chacha_enc_time,
        "Decryption Time (s)": chacha_dec_time,
        "Encryption CPU (%)": chacha_cpu_enc,
        "Decryption CPU (%)": chacha_cpu_dec,
        "Encryption Memory (MB)": chacha_mem_enc,
        "Decryption Memory (MB)": chacha_mem_dec,
    })


# Main script
if __name__ == "__main__":
    datasets = ["data/customers-100.csv", "data/customers-1000.csv", "data/customers-10000.csv"]

    for dataset in datasets:
        experiment(dataset)
