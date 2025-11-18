#!/usr/bin/env python3
"""Quick data exploration script."""

import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from ingestion.data_loader import DataLoader

# Load data
loader = DataLoader(encoding='utf-8', language='uk', create_translations=True)
df = loader.load_csv('data/raw/answers.csv')

print(f"\n{'='*80}")
print("DATA EXPLORATION")
print(f"{'='*80}\n")

print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

print("Columns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print(f"\n{'-'*80}\n")

print("First few rows (sample data):")
print(df.head(3).T)

print(f"\n{'-'*80}\n")

print("Data Dictionary:")
data_dict = loader.get_data_dictionary()
print(data_dict.to_string())

print(f"\n{'='*80}\n")
