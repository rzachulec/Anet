import pandas as pd

# Load sheet 3 without headers
df = pd.read_excel("comp.xlsx", sheet_name=3, header=None)

# Clean up External DB column: drop NaNs and strip spaces
col_c = df[1].dropna().astype(str).str.strip()

# Clean up Local DB column too
col_a = df[2].dropna().astype(str).str.strip()

# Check which items from column C are not in column A
missing_items = col_c[~col_c.isin(col_a)]

# Output results
if missing_items.empty:
    print("✅ All items from External DB are present in Local DB.")
else:
    print("❌ Some items from External DB are missing in Local DB:")
    print(missing_items.unique())
