"""
converter.py

This script converts an XML file into a JSON file by extracting specific data fields
and transforming them into a structured JSON format.

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

# Load XML file
import sys

xml_file = "input.XML"
try:
    if not os.path.exists(xml_file):
        raise FileNotFoundError(f"The file '{xml_file}' does not exist.")
    tree = ET.parse(xml_file)
    root = tree.getroot()
except FileNotFoundError as e:
    print(e)
    sys.exit(1)

# Define XML namespaces
ns = {"rsm": "LOR_gg_v17p01", "ram": "ReusableAggregateBusinessInformationEntity_12p0_LOR_gg_v17p01"}

# Extract sample data
samples = []
for sample in root.findall("rsm:AgriculturalSample", ns):
    sample_code =  sample.find("ram:Information", ns).text if sample.find("ram:Information", ns) is not None else None
    # customer_code = sample.find("ram:SenderAssignedID", ns).text if sample.find("ram:SenderAssignedID", ns) is not None else None
    ingredient_code = sample.find("ram:IntakeID", ns).text if sample.find("ram:IntakeID", ns) is not None else None
    sampling_date = sample.find("ram:SamplingDateTime", ns).text if sample.find("ram:SamplingDateTime", ns) is not None else None
    description_text = sample.find("ram:Information", ns).text if sample.find("ram:Information", ns) is not None else None

    # Extract translations
    description = []
    if description_text:
        description.append({"LanguageCode": "EN", "Description": description_text})

    # Extract analysis values
    analysis = []
    for observation in sample.findall("ram:SpecifiedSampleObservationResult/ram:ObservedValueSpecifiedSampleObservationResultCharacteristic", ns):
        nutrient_code = observation.find("ram:MethodParameterID", ns).text if observation.find("ram:MethodParameterID", ns) is not None else None
        nutrient_description = observation.find("ram:ParameterValue", ns).text if observation.find("ram:ParameterValue", ns) is not None else None
        value = float(observation.find("ram:MeasuredValueMeasure", ns).text) if observation.find("ram:MeasuredValueMeasure", ns) is not None else None
        unit_code = observation.find("ram:MeasuredValueMeasure", ns).attrib.get("unitCode") if observation.find("ram:MeasuredValueMeasure", ns) is not None else None

        if unit_code == "GRMKGM":
            unit_code = "%"
            value = round((value/10), 4)
            
            
        if  unit_code[:2] == "P1":
            unit_code = "%"
        
        if nutrient_code and nutrient_description and "months" not in nutrient_description  and "1991" not in nutrient_description and "hr" not in nutrient_description and "hours" not in nutrient_description:
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
            # "CustomerCode": customer_code,
            "SampleCode": sample_code,
            "Description": description,
            "Analysis": analysis
        })

# Build final JSON structure
json_output = {
    "Samples": samples
}

# Save to JSON file
output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=4)

print(f"JSON data saved to {output_file}")
