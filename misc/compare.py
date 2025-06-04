import pandas as pd

# Load the CSV files
codes1 = pd.read_csv("codes1.csv")
codes2 = pd.read_csv("codes2.csv")

# Merge both dataframes on 'Code'
merged = codes2.merge(codes1, on="Code", how="left", suffixes=("_codes2", "_codes1"))

# Find codes not in codes1 (i.e., NaN in Description_codes1)
not_in_codes1 = merged[merged["Description_codes1"].isna()].copy()
not_in_codes1["Reason"] = "Missing in Reference"

# Find codes where descriptions differ
desc_diff = merged[
    (~merged["Description_codes1"].isna()) & 
    (merged["Description_codes1"] != merged["Description_codes2"])
].copy()
desc_diff["Reason"] = "Different Description"

# Combine results and sort (missing first)
result = pd.concat([not_in_codes1, desc_diff]).sort_values(by="Reason", ascending=False)

# Save results to CSV
result[["Code", "Description_codes2", "Description_codes1", "Reason"]].to_csv("codes_difference.csv", index=False)

print("Differences saved to 'codes_difference.csv'.")
