"""
converter.py

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
import os
from datetime import datetime

def parse_date(date_str):
    """Convert various date formats to ISO format"""
    try:
        # Try parsing different common formats
        for fmt in ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y']:
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%dT00:00:00')
            except ValueError:
                continue
        # If no format matches, return original with added time
        if 'T' not in date_str:
            return f"{date_str}T00:00:00"
        return date_str
    except:
        return date_str

def scan_files(dir):
    base_output_dir = "Bestmix_files"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
        
    for xml_file in os.listdir(dir):
        print(xml_file)
        if xml_file.lower().endswith(".xml"):
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(base_output_dir, f"{timestamp}_{os.path.splitext(xml_file)[0]}_Bestmix.xml")
                data = parse_lab_report(xml_file)
                generate_qc_xml(data, output_file)
                print(f"Generated QC XML: {output_file}")
            except ET.ParseError as e:
                print(f"Error parsing '{xml_file}': {e}")
                continue
        

def parse_lab_report(report_file):
    tree = ET.parse(report_file)
    root = tree.getroot()
    
    customer_no = root.find(".//BETRNR").text
    order_no = root.find(".//AUFTRAGSNUMMER").text
    analysis_no = root.find(".//ANALYSENNUMMER").text
    sample_name = root.find(".//PROBENBEZEICHNUNG").text.strip()
    sample_arrival_date = parse_date(root.find(".//EINDAT_A").text)
    report_date = parse_date(root.find(".//TERMIN_A").text)
    
    parameters = []
    for param in root.findall(".//PARAMETER"):
        prop_id = param.find(".//PARAMETER_ID").text
        prop_name = param.find(".//NAME_EXTERN").text
        result = param.find(".//ERG_E").text
        unit = param.find(".//EINHEIT_DB").text
        method = param.find(".//METHODE_PG").text if param.find(".//METHODE_PG") is not None else "Unknown"
        
        parameters.append({
            "PropertyID": prop_id,
            "PropertyName": prop_name,
            "Result": result,
            "Unit": unit,
            "MethodName": method
        })
    
    return {
        "LaboratoryName": "AGROLAB LUFA GmbH",
        "RequesterName": customer_no,
        "ReportDate": report_date,
        "Sample": {
            # "SamplingDate": report_date,
            "SampleIDLab": analysis_no,
            "SampleIDRequester": order_no,
            "SampleArrivalDate": sample_arrival_date,
            "ArticleName": sample_name,
            "Properties": parameters
        }
    }

def generate_qc_xml(data, output_file):
    root = ET.Element("Transaction")
    ET.SubElement(root, "MessageType").text = "BML_LABRES"
    ET.SubElement(root, "MessageVersion").text = "1.0"
    ET.SubElement(root, "LaboratoryName").text = data["LaboratoryName"]
    ET.SubElement(root, "RequesterName").text = data["RequesterName"]
    ET.SubElement(root, "ReportDate").text = data["ReportDate"]
    
    sample = ET.SubElement(root, "Sample")
    # ET.SubElement(sample, "SamplingDate").text = data["Sample"]["SamplingDate"]
    ET.SubElement(sample, "SampleIDLab").text = data["Sample"]["SampleIDLab"]
    ET.SubElement(sample, "SampleIDRequester").text = data["Sample"]["SampleIDRequester"]
    ET.SubElement(sample, "SampleArrivalDate").text = data["Sample"]["SampleArrivalDate"]
    ET.SubElement(sample, "ArticleName").text = data["Sample"]["ArticleName"]
    
    for prop in data["Sample"]["Properties"]:
        prop_el = ET.SubElement(sample, "Property")
        ET.SubElement(prop_el, "PropertyID").text = prop["PropertyID"]
        ET.SubElement(prop_el, "PropertyName").text = prop["PropertyName"]
        ET.SubElement(prop_el, "ResultN").text = prop["Result"]
        ET.SubElement(prop_el, "Unit").text = prop["Unit"]
        ET.SubElement(prop_el, "MethodName").text = prop["MethodName"]
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    input_dir = "Input_files"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print("Please place input files in Input_files folder.")
    scan_files(input_dir)



