import pandas as pd
import os

datas = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["New York", "Los Angeles", "Chicago"],
}

df = pd.DataFrame(datas)

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
file_path = os.path.join(data_dir, "data.csv")
df.to_csv(file_path, index=False)
print(f"Data saved to {file_path}")
