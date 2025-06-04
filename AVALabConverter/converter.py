"""
converter.py

This script converts all XML files in the current directory into JSON files by extracting specific data fields
and transforming them into a structured JSON format. The output files are named after the input files with
the suffix '_Bestmix' added.

Copyright (c) 2025 Jan Narożny

Licensed under the MIT License. You may obtain a copy of the License at:
https://opensource.org/licenses/MIT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import xml.etree.ElementTree as ET
import json
import os
import datetime
# Define XML namespaces
ns = {"rsm": "LOR_gg_v17p01", "ram": "ReusableAggregateBusinessInformationEntity_12p0_LOR_gg_v17p01"}

# accepted_codes= []
accepted_codes = ["VBDS", "VAPH", "VARAS", "VBFOS", "VBFOP2", "VBOEB", "VBOEP2", "VAVCOS", "VARVET", "VBSW", "VBVEM", "VBVEVI", "VBME", "VBREIN", "VARE", "VBNH3F", "VBDVE", "VARC", "VASUIK", "VBVOS", "VANDF", "VBVCW", "VAADF", "VAADL", "VANO3"]

# include_desc = [ "CFAT", "C12:0", "TFA", "DM (%)", "DMI", "C14:0", "C16:0", "C16:1", "C18:0", "C18:2", "C18:3", "Other Lipids", "Yeast", "Monensin", "Niacin, total, %", "Biotin, total", "Choline, total", "Cr", "Toxin_Binders", "DM", "NDF", "ADF", "ADL", "CP", "NDIP", "ADIP", "Ash", "Prt-A ", "Prt-C ", "Prt-B ", "Kd ", "dcRUP", "Ca", "P-total", "Mg", "K", "LA", "Cl", "S", "Co", "Cu", "J", "Fe", "Mn", "Se", "Zn", "Vit-A, total, kIU", "Vit-D, total, kIU", "Vit-E, total, IU", "Moisture", "NDF Digest", "ME rum", "NEl (from VEM)", "NEm", "NEg", "Conc", "ARG", "HIS", "ILE", "LEU", "LYS", "MET", "VAL", "TRP", "THR", "PHE", "CYS", "NPN", "peNDF", "SP", "Rumen NH3 %Req", "Ferm NDF", "SUG", "Starch-AG", "AC", "PR", "BU", "Soluble Fiber", "Other OAs", "LA", "Prt pool A1", "Prt pool A2", "Prt pool B1", "Prt pool B2", "Prt pool C", "MUN", "Forage NDF", "aNDFom", "CFIBRE", "C18:1", "U:S Ratio", "Vit D3", "Vit E", "Beta-Carotene", "Vit K3", "Vit B1(thiamin)", "Vit B2 (riboflavin)", "Vit B6 (pyridoxine)", "Vit B12 (cyanocobalamin)", "Vit H-Biotin", "Vit B9-Folic acid", "Vit B3-Niacin", "Vit B5-Pantothenic acid", "Choline", "Betain", "Vit C", "RDP", "MP", "RUP", "eNDF", "Vit A", "Starch-total", "CPin", "FOMr", "FOMr-2", "VEVI", "VEM", "DVE", "OEB", "OEB+", "OEB-2", "LYS, metabolizable", "MET, metabolizable", "dEB", "SV rum, CVB", "Bypass Starch", "NH3-fr", "PUFA n-3", "PUFA n-6", "Ca/P", "Lignin %NDF", "peNDF %NDF", "SP %CP", "NPN %SP", "OM digestibility", "RDP (%CP)", "DCAD", "RUFAL", "VEM/DM", "DVE/DM", "SW/DM", "LYSm%DVE", "METm%DVE", "SW", "Choline chloride", "CFU 1*10^9/g" ]
include_desc = []

input_dir = "Input_files"
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    print("Please place input files in Input_files folder.")

# Process all XML files in the current directory
for xml_file in os.listdir(input_dir):
    if xml_file.lower().endswith(".xml"):
        try:
            # Parse the XML file
            tree = ET.parse(os.path.join(input_dir, xml_file))
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing '{xml_file}': {e}")
            continue

        # Extract sample data
        samples = []
        for sample in root.findall("rsm:AgriculturalSample", ns):
            # sample_code = sample.find("ram:Information", ns).text if sample.find("ram:Information", ns) is not None else None
            sample_code = sample.find("ram:IntakeID", ns).text if sample.find("ram:IntakeID", ns) is not None else None
            ingredient_code = sample.find("ram:IntakeID", ns).text if sample.find("ram:IntakeID", ns) is not None else None
            sampling_date = sample.find("ram:SamplingDateTime", ns).text if sample.find("ram:SamplingDateTime", ns) is not None else None
            description_text = sample.find("ram:Information", ns).text if sample.find("ram:Information", ns) is not None else None

            # Extract translations
            description = []
            if description_text:
                description.append({"LanguageCode": "EN", "Description": description_text})

            # Extract analysis values
            analysis = []
            dm_value = 0
            for observation in sample.findall("ram:SpecifiedSampleObservationResult/ram:ObservedValueSpecifiedSampleObservationResultCharacteristic", ns):
                nutrient_code = observation.find("ram:MethodParameterID", ns).text if observation.find("ram:MethodParameterID", ns) is not None else None
                nutrient_description = observation.find("ram:ParameterValue", ns).text if observation.find("ram:ParameterValue", ns) is not None else None
                value = float(observation.find("ram:MeasuredValueMeasure", ns).text) if observation.find("ram:MeasuredValueMeasure", ns) is not None else None
                unit_code = observation.find("ram:MeasuredValueMeasure", ns).attrib.get("unitCode") if observation.find("ram:MeasuredValueMeasure", ns) is not None else None
                
                if unit_code == "GRMKGM":
                    unit_code = "%"
                    value = round((value / 10), 4)
                    
                if nutrient_code == "VBDS":
                    dm_value = value

                if unit_code[:2] == "P1":
                    unit_code = "%"
                    
                if unit_code == "MINLOG":
                    unit_code = "-"
                    
                if unit_code == "BLNC":
                    unit_code = "/kg"
                    
                if unit_code == "VEMKGM":
                    unit_code = "/kg"
                    
                if nutrient_code != "VAPH" and dm_value:
                    if nutrient_code != "VBDS" and nutrient_code != "VAVCOS":
                        product_value = value * ( dm_value / 100 )
                        value = round(product_value, 2)
                    
                if str(nutrient_description) in set(include_desc) or nutrient_code in accepted_codes:
                    analysis.append({
                        "NutrientCode": nutrient_code,
                        "NutrientDescription": nutrient_description,
                        "UnitCode": unit_code,
                        "Value": value if value else None
                    })    

            # Build sample entry
            if sample_code:
                samples.append({
                    "IngredientCode": ingredient_code,
                    "SampleCode": sample_code,
                    "Description": description,
                    "Analysis": analysis
                })

        # Build final JSON structure
        json_output = {
            "Samples": samples
        }
        
        # Create output directory if it doesn't exist
        base_output_dir = "Bestmix_files"
        if not os.path.exists(base_output_dir):
            os.makedirs(base_output_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(base_output_dir, f"{timestamp}_{os.path.splitext(xml_file)[0]}_Bestmix.json")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(json_output, f, indent=4)

        print(f"Processed '{xml_file}' and saved to '{output_file}'")
        
# DONE make sample code ingredient code, <ram:ID schemeID="EUROFINS-AGRO">00027544-402252</ram:ID> 

# DONE: convert reported values in % to percentage of product not DM: value = value in DM * dm percentage / 100 