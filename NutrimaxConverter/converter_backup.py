import os
import csv

output_dir = os.path.join('..', 'NIR')
os.makedirs(output_dir, exist_ok=True)

def clean_cell(cell):
    # Remove leading/trailing spaces and all surrounding quotes
    return cell.strip().strip('"').replace('""', '"').replace('"""', '"')

for filename in os.listdir('../'):
    if filename.endswith('.csv'):
        input_path = os.path.join('./', filename)
        output_filename = filename.replace('.csv', '_qc.csv')
        output_path = os.path.join(output_dir, output_filename)

        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', newline='', encoding='utf-8') as outfile:

            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL, doublequote=True, delimiter=';')

            for line in infile:
                # Split the row by commas first
                raw_cells = line.strip().split(';')

                # Clean each cell manually
                cleaned_row = [clean_cell(cell) for cell in raw_cells]

                # Remove the last cell if it's empty
                if cleaned_row and cleaned_row[-1] == "":
                    cleaned_row.pop()
                # Write to new CSV
                writer.writerow(cleaned_row)

        print(f"Formatted: {filename} → {output_path}")
