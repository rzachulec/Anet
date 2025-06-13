import os
import csv
import sys

# Get the input filename from argument
if len(sys.argv) < 2:
    print("Usage: python converter.py <input_csv_file>")
    sys.exit(1)

input_path = sys.argv[1]

# Ensure the input path is valid
if not os.path.isfile(input_path):
    print(f"Error: File not found - {input_path}")
    sys.exit(1)

# Resolve full path of input and output
input_path = os.path.abspath(input_path)
input_dir = os.path.dirname(input_path)
filename = os.path.basename(input_path)

# Output directory: QC/NIR
output_dir = os.path.abspath(os.path.join(input_dir, 'NIR'))
os.makedirs(output_dir, exist_ok=True)

output_filename = filename.replace('.csv', '_qc.csv')
output_path = os.path.join(output_dir, output_filename)


def clean_cell(cell):
    # Remove leading/trailing spaces and all surrounding quotes
    return cell.strip().strip('"').replace('""', '"').replace('"""', '"')


with open(input_path, 'r', encoding='utf-8') as infile, \
     open(output_path, 'w', newline='', encoding='utf-8') as outfile:

    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=';')

    for line in infile:
        raw_cells = line.strip().split(';')
        cleaned_row = [clean_cell(cell) for cell in raw_cells]

        if cleaned_row and cleaned_row[-1] == "":
            cleaned_row.pop()

        writer.writerow(cleaned_row)

print(f"Formatted: {filename} → {output_path}")
