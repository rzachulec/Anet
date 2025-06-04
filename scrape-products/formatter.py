import os
import pandas as pd
import re

surowce_file = 'Surowce BM3.xlsx'
dfS = pd.read_excel(surowce_file, header=None)
matryca_file = 'Matryca BM3.xlsx'
dfM = pd.read_excel(matryca_file, header=None)

# format nutrient codes in the first row of dfS (except first two columns)
for col in dfS.columns[2:]:
    value = dfS.at[0, col]
    try:
        num = int(str(value).strip())
        dfS.at[0, col] = f"C{num:03d}"
    except (ValueError, TypeError):
        pass  #leave as is if not a number
    
column_codesS = {index: str(value).replace('-', '').replace(' ', '') for index, value in dfS.iloc[1].items()} 
column_codesM = {index: str(value).replace('-', '').replace(' ', '') for index, value in dfM.iloc[0].items()} 

csv_dir = './produkty_info'
# csv_dir = './test'

new_rows = []
new_rowsM = []
new_cols = 0

# Iterate through each CSV file in the directory that ends with '_surowce.csv'
for filename in os.listdir(csv_dir):
    if filename.endswith('_surowce.csv'):
        # Parse the filename for code and description
        bracketed_parts = re.findall(r'\((.*?)\)', filename)  # Find all bracketed parts
        
        if len(bracketed_parts) >= 2:
            code = bracketed_parts[-1]  # Take the last bracketed part as the code
            description = filename.split(f'({bracketed_parts[-1]})')[0].strip()  # Everything before the second bracket
        elif len(bracketed_parts) == 1:
            code = bracketed_parts[0]
            description = filename.split(f'({code})')[0].strip()
        else:
            print(f"Warning: No bracketed code found in filename '{filename}', skipping...")
            continue

        # Load the CSV file
        csv_file_path = os.path.join(csv_dir, filename)
        csv_dfS = pd.read_csv(csv_file_path)

        # Create an empty row with all columns from dfS
        new_row = pd.Series({col: pd.NA for col in dfS.columns})

        # Set code and description in the first and second row
        new_row.iloc[0] = code
        new_row.iloc[1] = description
        
        cntNEm = 0
        cntMEpo = 0
        cntMEla = 0

        # Fill values according to matching Labels
        for _, row in csv_dfS.iterrows():
            label = str(row['Label'])
            value = row['Value']
            unit = row['Unit']
            
            if '%' in unit:
                unit = '%'
            elif 'kcal/kg' in unit:
                unit = 'kcal'
            elif '/kg' in unit:
                unit = 'g'
            elif '16gN' in unit:
                unit = 'g/16gN'
            elif 'MJ' in unit:
                unit = 'MJ'
            elif '- -' in unit or '- in Prod' in unit:
                unit = '-'
                
            label = label.removesuffix('-07').replace('-', '').replace(' ', '')

            if label == 'MErab':
                if unit == 'MJ': label = 'OEk'
                else: label = 'OEkKC'
            elif label == 'NEm':
                print(label, ", ", unit)
                if unit == 'kcal': label = 'NEmKC'
            elif label == 'EW2015': label = 'EW'
            elif label == 'NE2015':
                if unit == 'kcal': label = 'NEvKC'
                else: label = 'NEv'
            elif label == 'MEla':
                if unit == 'MJ': label = 'OElh'
                else: label = 'OElhKC'
            elif label == 'MEpo':
                if unit == 'MJ': label = 'OEpl'
                else: label = 'OEplKC'
            elif label == 'DPpo': label = 'DPp'
            elif label == 'MEbr':
                if unit == 'MJ': label = 'OEslk'
                else: label = 'OEslkKC'
            elif label == '%RUSTA': label = 'DRUSTA'
            
            # Find the matching column by checking second-row codes
            matching_column = None
            for col_index, col_code in column_codesS.items():
                if str(col_code) == label:
                    matching_column = col_index
                    break

            if matching_column:
                new_row[matching_column] = value
            elif label != 'nan':
                dfS[label] = pd.NA 
                dfS.iloc[0, dfS.columns.get_loc(label)] = f"BX{new_cols%1000:03d}"
                dfS.iloc[1, dfS.columns.get_loc(label)] = label 
                dfS.iloc[2, dfS.columns.get_loc(label)] = unit 
                new_row[label] = value  # Set the value in the new column
                new_cols += 1
        new_rows.append(new_row)
        
    if filename.endswith('_matryca.csv'):
        bracketed_parts = re.findall(r'\((.*?)\)', filename)  # Find all bracketed parts
        
        if len(bracketed_parts) >= 2:
            code = bracketed_parts[-1]  # Take the last bracketed part as the code
            description = filename.split(f'({bracketed_parts[-1]})')[0].strip()  # Everything before the second bracket
        elif len(bracketed_parts) == 1:
            code = bracketed_parts[0]
            description = filename.split(f'({code})')[0].strip()
        else:
            print(f"Warning: No bracketed code found in filename '{filename}', skipping...")
            continue
        
        # Load the CSV file
        csv_file_path = os.path.join(csv_dir, filename)
        csv_dfS = pd.read_csv(csv_file_path)

        # Create an empty row with all columns from dfM
        new_row = pd.Series({col: pd.NA for col in dfM.columns})

        # Set code and description in the first and second row
        new_row.iloc[0] = code
        new_row.iloc[1] = description

        # Fill values according to matching Labels
        for _, row in csv_dfS.iterrows():
            label = str(row['Label'])
            value = row['Value']
            unit = row['Unit']
            
            if '%' in unit:
                unit = '%'
            elif 'kcal/kg' in unit:
                unit = 'kcal/kg'
            elif '/kg' in unit:
                unit = 'g'
            elif '16gN' in unit:
                unit = 'g/16gN'
            elif 'MJ' in unit:
                unit = 'MJ'
            elif '- -' in unit or '- in Prod' in unit:
                unit = '-'
            
            label = label.removesuffix('-07').replace('-', '').replace(' ', '')

            # Find the matching column by checking second-row codes
            matching_column = None
            for col_index, col_code in column_codesM.items():
                if str(col_code) == label:  # Ensure comparison works for strings/numbers
                    matching_column = col_index
                    break

            if matching_column:
                new_row[matching_column] = value
                
            elif label != 'nan':
                # print(f"Alert: not found. Adding new matryce column for: \t '{label}' ")
                dfM[label] = pd.NA
                dfM.iloc[1, dfM.columns.get_loc(label)] = f"BX{new_cols%1000:03d}"
                dfM.iloc[0, dfM.columns.get_loc(label)] = label
                dfM.iloc[2, dfM.columns.get_loc(label)] = unit
                new_row[label] = value
                new_cols += 1
                
        new_rowsM.append(new_row)
        

# Convert list of rows to DataFrame and append to dfS
if new_rows:
    dfS = pd.concat([dfS, pd.DataFrame(new_rows)], ignore_index=True)
if new_rowsM:
    dfM = pd.concat([dfM, pd.DataFrame(new_rowsM)], ignore_index=True)
    
output_file = 'Processed_Surowce_BM3.xlsx'
output_file_csv = 'Processed_Surowce_BM3.csv'

dfS.to_csv(output_file_csv, index=False, sep=';', encoding='cp1252')
dfS.to_excel(output_file, index=False, header=False)

output_fileM = 'Processed_Matryce_BM3.xlsx'
output_fileM_csv = 'Processed_Matryce_BM3.csv'

dfM.to_csv(output_fileM_csv, index=False, sep=';', encoding='cp1252')
dfM.to_excel(output_fileM, index=False, header=False)

print(f"Processing complete. Outputs saved to {output_file} and {output_fileM}.")
