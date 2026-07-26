from src.ingestion.dataset_loader import load_dataset

df = load_dataset("datasets/dataset.csv")

print(df.head())
print()
print(df.shape)
print()
print(df.columns.tolist())