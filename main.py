from experiment import experiment

# Define datasets
datasets = [
    "data/customers-100.csv",
    "data/customers-1000.csv",
    "data/customers-10000.csv",
    "data/customers-100000.csv",
]

if __name__ == "__main__":
    for dataset in datasets:
        try:
            experiment(dataset)
        except ValueError as e:
            print(f"Skipping {dataset}: {e}")
