import pandas as pd

df = pd.read_excel("./Surowce_BX3_all.xlsx")

df.to_csv("./Surowce_BX3_all_updated.csv", sep=";")

bx4_cols = [col for col in df.columns if type(col) == int and col > 1000 and col < 2000]

selected_rows = df.iloc[1:5][bx4_cols]

# print(selected_rows)

other_units = selected_rows.iloc[3][(selected_rows.iloc[3] != "g/kg") & (selected_rows.iloc[3] != "mg/kg") & (selected_rows.iloc[3] != "g") & (selected_rows.iloc[3] != "%")]

print(other_units)