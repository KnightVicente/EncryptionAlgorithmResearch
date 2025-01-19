# A Comparative Study of AES, RSA, and ChaCha20-Poly1305 Encryption Algorithms Performance

## Description
This repository contains the code, datasets, and results for a comparative study of the performance of three encryption algorithms: AES, RSA (Hybrid), and ChaCha20-Poly1305. The study evaluates their encryption and decryption times, memory usage, key sizes, and security levels across datasets of varying sizes.

## Features
- **Algorithms Evaluated**:
  - AES (256-bit, GCM mode)
  - RSA (Hybrid, 2048-bit key)
  - ChaCha20-Poly1305 (256-bit)
- **Performance Metrics**:
  - Encryption time
  - Decryption time
  - Memory usage
  - Security level
- **Dataset Sizes**:
  - 100, 1,000, 10,000, and 100,000 rows (sourced from [Datablist](https://www.datablist.com/learn/csv/download-sample-csv-files)).

## Contents
1. **Code**:
   - Python scripts for running encryption experiments, measuring performance, and generating results.
   - Individual modules for AES, RSA, and ChaCha20-Poly1305 implementations.
2. **Datasets**:
   - Sample CSV files used for testing (not included due to size; link provided for downloading).
3. **Results**:
   - CSV files containing performance metrics.
   - Figures visualizing encryption and decryption times and memory usage.
   - 
## How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/KnightVicente/EncryptionAlgorithm
2. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Run experiments
  ```bash
  python main.py
  ```
4. View results:
  - CSV files in the results/ folder.
  - Encrypted files in the encrypted_files/ folder.
