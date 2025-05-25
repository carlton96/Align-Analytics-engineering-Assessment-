import pandas as pd
import os

# Set file paths and delimiter
txt_file_path = "health_products.txt"

csv_file_path = 'health_products.csv'
delimiter = ' '

# Error handling
try:
    # Check if file exists
    if not os.path.isfile(txt_file_path):
        raise FileNotFoundError(f"Input file not found: {txt_file_path}")

    # Read the TXT file into a DataFrame
    df = pd.read_csv(txt_file_path, delimiter=delimiter,encoding='UTF-8')

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("Input file is empty or improperly formatted.")

    # Write to CSV
    df.to_csv(csv_file_path, index=False)
    print(f"File successfully converted to CSV: {csv_file_path}")

except FileNotFoundError as fnf_err:
    print(f"Error: {fnf_err}")
except pd.errors.ParserError as parse_err:
    print(f"Parsing error: {parse_err}")
except ValueError as val_err:
    print(f"Error: {val_err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
