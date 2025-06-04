import csv
import json
import os
from datetime import datetime

# Define input/output directories
input_dir = "Input_files"
output_dir = "Bestmix_files"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(input_dir, exist_ok=True)

nutrient_codes = [
    10, 100, 110, 120, 40, 30, 4000, 4010, 4020, 4030, 4040, 4050, 4060, 4510, 4530, 4540, 4560, 20, 500, 60, 50, 5050, 5060, 5070, 5110, 5120, 2010, 2060, 2070, 2080, 2090, 2100, 2030, 2110, 2140, 2150, 2170, 70, 2160, 4310, 2210, 2260, 2270, 2280, 2290, 2300, 2310, 2360, 2350, 2370, 2510, 2560, 2570, 2580, 2590, 2600, 2610, 2660, 2640, 2650, 2670, 5080, 2340, 2200, 2500, 2000, 2020, 2040, 2050, 2120, 2130, 2230, 2530, 2220, 2240, 2250, 2320, 2330, 2520, 2540, 2550, 2620, 2630, 2700, 2400, 2190, 55, 1150, 65, 860, 870, 880, 885, 900, 1840, 1206, 1207, 1255, 1285, 1800, 1810, 1850, "2890CVB", "2900CVB", 4345, 4420, 4430, 6000, 6020, 1000, 1005, 1010, 1015, 1020, 1025, 1140, 1155, 1300, 1305, 4360, 4370, 6010, 2199, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2958, 2959, 2960, 2963, 2964, 2965, 2966, 2969, 2961, 2962, 5195, 1310, 1315, 1316, 1900, 4315, 5235, 5236, 5090, 5100, 5030, 5040, 5130, 5160, 5190, 5180, 1700, 810, 5000, 5280, 830, 840, 800, 580, 1710, 1711, 121, 581, 2151, 5001, 5031, 5041, 5051, 5061, 5071, 5091, 5101, 5111, 5121, 5281, 831, 841, 2101, 2091, 2011, 2141, 2081, 2071, 2171, 2061, 2111, 811, 801, 1701, 5191, 5161, 5131, 5181, 5176, 5175, "0580CNCPS", "0581CNCPS", 5216, 4340, 4350, 5200, 5210, 5220, 5230, 2180, 2380, 4400, 2680, 9601, 505, 6701, 6721, "1701NRC", "1701CNCPS", "1711NRC", "1711CNCPS", 2645, 2655, 2675, 2575, 2515, 2615, 2565, 2585, 2605, 2705, 2715, 4015, 4761, 4711, 4741, 4731, 1721, 5052, 4011
    , 40, 50, 70, 'FW_01', 55
]

nutrient_names = [
    "DM", "NDF", "ADF", "Lignin", "CP", "Ash", "Ca", "P", "Mg", "K", "Na", "Cl", "S", "Cu", "Fe", "Mn", "Zn", "Moisture", "Sugar", "Starch", "Fat (EE)", "C16:0", "C16:1", "C18:0", "C18:2", "C18:3", "ARG", "HIS", "ILE", "LEU", "LYS", "MET", "CYS", "PHE", "THR", "TRP", "VAL", "Crude fiber", "Tyr", "Phytate P", "AID Arg", "AID His", "AID Ile", "AID Leu", "AID Lys", "AID Met", "AID Phe", "AID Tyr", "AID Trp", "AID Val", "SID Arg", "SID His", "SID Ile", "SID Leu", "SID Lys", "SID Met", "SID Phe", "SID Tyr", "SID Thr", "SID Trp", "SID Val", "C18:1", "AID Thr", "AID Ala", "SID Ala", "Ala", "Asp", "Glu", "Gly", "Pro", "Ser", "AID Cys", "SID Cys", "AID Asp", "AID Glu", "AID Gly", "AID Pro", "AID Ser", "SID Asp", "SID Glu", "SID Gly", "SID Pro", "SID Ser", "SID Met+Cys", "AID Met+Cys", "Met+Cys", "Acid ether extract", "NEs, CVB", "Starch-Ewers", "NSP", "DMref", "NFE", "NFEh", "RNSP", "CPin", "FOMr", "FOMr-2", "VEVI", "VEM", "DVE", "RNB", "RNB-2", "LYS, metabolizable, CVB", "MET, metabolizable, CVB", "dEB", "S-inorganic", "S-organic", "SV rum, CVB", "Bypass Starch rum, CVB", "AME-broiler", "AME-broiler", "AME-layers", "AME-poultry", "AME-poultry", "AME-layers", "Energy Value (EV), CVB", "NEs, CVB", "ME-Rabbit", "ME-Rabbit", "Dig.P-pigs, CVB", "Ret.P-poultry, CVP", "VW rum, CVB (FIC)", "Sum_AA, total", "AFD ALAp", "AFD ARGp", "AFD ASPp", "AFD CYSp", "AFD GLUp", "AFD GLYp", "AFD HISp", "AFD ILEp", "AFD LEUp", "AFD LYSp", "AFD METp", "AFD PHEp", "AFD THRp", "AFD TRPp", "AFD TYRp", "AFD VALp", "AFD M+Cp", "AFD PROp", "AFD SERp", ">=C20", "Energy Value-horses", "NEm-horse", "NEm-horse", "Dig.protein horses", "NPP", "PUFA n-3", "PUFA n-6", "C18:1t", "C18:1c", "C12:0", "C14:0", "C18:4", "C20:5,n-3 (EPA)", "C22:6,n-3 (DHA)", "C22:5 (DPA)", "RDP", "SP", "TFA", "Other Lipids", "NDIP", "ADIP", "NPN", "peNDF", "RUP", "RUP %CP", "Lignin %NDF", "peNDF %NDF", "TRP %CP", "TFA %EE", "C12:0 (TFA)", "C14:0 (TFA)", "C16:0 (TFA)", "C16:1 (TFA)", "C18:0 (TFA)", "C18:1t (TFA)", "C18:1c (TFA)", "C18:2 (TFA)", "C18:3 (TFA)", "Other Lipids (TFA)", "NDIP %CP", "ADIP %CP", "MET %CP", "LYS %CP", "ARG %CP", "THR %CP", "LEU %CP", "ILE %CP", "VAL %CP", "HIS %CP", "PHE %CP", "SP %CP", "NPN %SP", "RDP (%CP)", "C22:6,n-3 (DHA) %TFA", "C20:5,n-3 (EPA) %TFA", "C18:4 (TFA)", "C22:5 (DPA) %TFA", "C22:0 %TFA", "C22:0", "peNDF CNCPS", "peNDF %aNDFom CNCPS", "UFA CNCPS (Sum)", "DCAD1", "DCAD2", "SFA (Sum)", "UFA (Sum)", "MUFA (Sum)", "PUFA (Sum)", "SAA", "AID SAA", "Salt (calculated)", "SID SAA", "DM Sum", "Sugar + Starch", "Ferm Starch %Starch", "Ferm Sugar %Sugar", "RDP NRC (%CP)", "RDP CNCPS (%CP)", "RUP NRC (%CP)", "RUP CNCPS (%CP)", "SID Thr:Lys", "SID Trp:Lys", "SID Val:Lys", "SID Ile:Lys", "SID Arg:Lys", "SID Phe:Lys", "SID His:Lys", "SID Leu:Lys", "SID Met:Lys", "SID Met+Cys:Lys", "SID Phe+Tyr:Lys", "Ca/P", "Org Zn (%Zn)", "Org Cu (%Cu)", "Org Mn (%Mn)", "Org Fe (%Fe)", "L1_RUP_1X %CP", "C16:0 to C18:1 c+t ratio", "Pphyt : P"
    , "Crude Protein", "Fat (Ether Extract)", "Crude Fibre", "AMEn", "Fat (Acid Hydrolysis)"
]

nutrient_dict = [
    {"name": name, "code": code}
    for code, name in zip(nutrient_codes, nutrient_names)
]


# Get today's date prefix
date_prefix = datetime.now().strftime("%Y%m%d")

# Get list of CSV files
csv_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".csv")]

if not csv_files:
    print("No CSV files found in 'Input_files'. Please place input files in the directory.")
else:
    for filename in csv_files:
        input_path = os.path.join(input_dir, filename)
        print(f"Processing {input_path}...")

        with open(input_path, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            if not reader:
                continue
            df_columns = reader[0].keys()

            output = {"Samples": []}

            for row in reader:
                sample_code = row.get("Sample ID", "")
                description = row.get("Measurement Description", "")

                sample_entry = {
                    "SampleCode": sample_code,
                    "Description": [
                        {
                            "LanguageCode": "EN",
                            "Description": description
                        }
                    ],
                    "Analysis": []
                }

                # Identify nutrient pairs (value + unit columns)
                for col in df_columns:
                    if col.startswith("Result - ") and not col.endswith("_unit"):
                        nutrient_desc = col[9:]  # strip 'Result - '
                        unit_col = f"{col}_unit"

                        value = row.get(col, "")
                        unit = row.get(unit_col, "")

                        # Try to find the nutrient code by matching the description (case-insensitive)
                        nutrient_code = 0
                        for item in nutrient_dict:
                            if item["name"].lower() == nutrient_desc.lower():
                                nutrient_code = item["code"]
                                break

                        if nutrient_code != 0:
                            if type(nutrient_code) is int:
                                nutrient_code = f"{int(nutrient_code):04d}"
                        else:
                            nutrient_code = ""

                        nutrient = {
                            "NutrientCode": nutrient_code,
                            "NutrientDescription": nutrient_desc,
                            "UnitCode": unit,
                            "Value": value
                        }
                        sample_entry["Analysis"].append(nutrient)

                output["Samples"].append(sample_entry)

        output_filename = f"{date_prefix}_{os.path.splitext(filename)[0]}.json"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        print(f"Saved to {output_path}")

