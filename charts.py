import pandas as pd
import matplotlib.pyplot as plt

# Input the provided dataset (customers-100_metrics.csv)
data_100 = {
    "Run": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10],
    "Algorithm": [
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
        "AES", "RSA (Hybrid)", "ChaCha20-Poly1305",
    ],
    "Key Size (bits)": [256, 2048, 256] * 10,
    "Encryption Time (s)": [
        0.000304, 0.0013451, 0.0001547, 9.61E-05, 0.0010894, 0.0001085,
        9.33E-05, 0.0010024, 0.0001194, 0.0001011, 0.0010004, 0.0001024,
        8.96E-05, 0.001013, 0.000109, 9.50E-05, 0.0010116, 0.0001039,
        9.26E-05, 0.001065, 0.0001076, 9.45E-05, 0.0010436, 0.0001094,
        9.58E-05, 0.0010128, 0.0001097, 9.72E-05, 0.0010174, 0.0001065,
    ],
    "Decryption Time (s)": [
        0.0001972, 0.0399664, 0.0001258, 0.0104654, 0.0400108, 0.000116,
        0.0001003, 0.0402635, 0.0001113, 9.97E-05, 0.0385694, 0.000106,
        9.54E-05, 0.0414358, 0.0001134, 0.0001018, 0.0399524, 0.0001105,
        9.83E-05, 0.0427222, 0.0001125, 0.0001024, 0.0403528, 0.0001136,
        0.0001044, 0.0416478, 0.0001169, 0.0001018, 0.042361, 0.0001118,
    ],
    "Memory Usage (MB)": [
        63.5234375, 63.8046875, 63.8671875, 63.8671875, 63.87109375, 63.890625,
        63.890625, 63.890625, 63.89453125, 63.89453125, 63.89453125, 63.8984375,
        63.8984375, 63.90234375, 63.90234375, 63.90234375, 63.90625, 63.90625,
        63.90625, 63.90625, 63.91015625, 63.91015625, 63.9140625, 63.91796875,
        63.91796875, 63.91796875, 63.91796875, 63.91796875, 63.91796875, 63.921875,
    ],
}

# Convert to DataFrame
df_100 = pd.DataFrame(data_100)

# Calculate averages for each algorithm
averages = df_100.groupby("Algorithm").mean().reset_index()

# Bar Chart: Encryption and Decryption Times
plt.figure(figsize=(10, 6))
plt.bar(averages["Algorithm"], averages["Encryption Time (s)"], color="skyblue", label="Encryption Time")
plt.bar(averages["Algorithm"], averages["Decryption Time (s)"], color="orange", alpha=0.7, label="Decryption Time")
plt.title("Average Encryption and Decryption Times (Customers-100 Dataset)", fontsize=14)
plt.ylabel("Time (s)", fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

# Bar Chart: Memory Usage
plt.figure(figsize=(10, 6))
plt.bar(averages["Algorithm"], averages["Memory Usage (MB)"], color=["blue", "orange", "green"])
plt.title("Average Memory Usage (Customers-100 Dataset)", fontsize=14)
plt.ylabel("Memory Usage (MB)", fontsize=12)
plt.tight_layout()
plt.show()


