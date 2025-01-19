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

# Read CSV file and convert to bytes
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_csv(index=False).encode('utf-8')


# Experiment function
def experiment(file_path, chunk_size=1024):
    dataset_name = os.path.basename(file_path).split(".")[0]
    print(f"\nTesting encryption algorithms on dataset: {file_path}")
    data = read_csv(file_path)

    # Split data into chunks
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    results_folder = "results"

    first_run = True  # Ensure CSV headers are written only once

    # AES Experiment
    print("AES Encryption")
    operation = lambda: [aes_encrypt(chunk) for chunk in chunks]  # Artificial load by chunk processing
    aes_result, aes_cpu_enc = measure_cpu_during_operation(operation)

    operation = lambda: [aes_decrypt(*chunk) for chunk in aes_result]
    _, aes_cpu_dec = measure_cpu_during_operation(operation)

    log_metrics(results_folder, dataset_name, "AES", {
        "Algorithm": "AES",
        "Encryption CPU (%)": aes_cpu_enc,
        "Decryption CPU (%)": aes_cpu_dec,
    }, first_run=first_run)
    first_run = False

    # RSA Experiment
    print("RSA Encryption")
    rsa_private_key, rsa_public_key = rsa_generate_keys()
    operation = lambda: [rsa_encrypt(chunk, rsa_public_key) for chunk in chunks]
    rsa_result, rsa_cpu_enc = measure_cpu_during_operation(operation)

    operation = lambda: [rsa_decrypt(*chunk, rsa_private_key) for chunk in rsa_result]
    _, rsa_cpu_dec = measure_cpu_during_operation(operation)

    log_metrics(results_folder, dataset_name, "RSA", {
        "Algorithm": "RSA",
        "Encryption CPU (%)": rsa_cpu_enc,
        "Decryption CPU (%)": rsa_cpu_dec,
    })

    # ChaCha20-Poly1305 Experiment
    print("ChaCha20-Poly1305 Encryption")
    operation = lambda: [chacha_encrypt(chunk) for chunk in chunks]
    chacha_result, chacha_cpu_enc = measure_cpu_during_operation(operation)

    operation = lambda: [chacha_decrypt(*chunk) for chunk in chacha_result]
    _, chacha_cpu_dec = measure_cpu_during_operation(operation)

    log_metrics(results_folder, dataset_name, "ChaCha20-Poly1305", {
        "Algorithm": "ChaCha20-Poly1305",
        "Encryption CPU (%)": chacha_cpu_enc,
        "Decryption CPU (%)": chacha_cpu_dec,
    })

# Main script
if __name__ == "__main__":
    datasets = ["data/customers-100.csv", "data/customers-1000.csv", "data/customers-10000.csv"]

    for dataset in datasets:
        experiment(dataset)
