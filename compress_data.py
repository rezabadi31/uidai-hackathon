import pandas as pd
import os

# Read the CSV file
df = pd.read_csv("data/merged_data_clean.csv")

# Calculate original file size in MB
original_size = os.path.getsize("data/merged_data_clean.csv") / (1024 * 1024)
print(f"Original size: {original_size:.2f} MB")

# Drop unnecessary columns if they exist
columns_to_drop = ['raw_id', 'uuid', 'remarks']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

# Convert numeric columns to lower precision
# int64 to int32
for col in df.select_dtypes(include=['int64']).columns:
    df[col] = df[col].astype('int32')

# float64 to float32
for col in df.select_dtypes(include=['float64']).columns:
    df[col] = df[col].astype('float32')

# Convert repeated string columns to category
category_cols = ['state', 'district', 'update_type']
for col in category_cols:
    if col in df.columns:
        df[col] = df[col].astype('category')

# Save the compressed CSV
df.to_csv("data/merged_data_compressed.csv", index=False)

# Calculate compressed file size in MB
compressed_size = os.path.getsize("data/merged_data_compressed.csv") / (1024 * 1024)
print(f"Compressed size: {compressed_size:.2f} MB")