import json

def find_empty_material_code(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    unique_lines = set()
    
    def check_empty_material_code(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "MaterialCode" and value == "":
                    unique_lines.add(json.dumps(obj, indent=4))
                check_empty_material_code(value)
        elif isinstance(obj, list):
            for item in obj:
                check_empty_material_code(item)
    
    check_empty_material_code(data)
    
    check_empty_material_code(data)
    
    parsed_lines = set()
    for line in unique_lines:
        obj_lines = line.split('\n')
        for i, obj_line in enumerate(obj_lines):
            if '"MaterialCode": ""' in obj_line and i + 1 < len(obj_lines):
                parsed_lines.add(obj_lines[i + 1])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in parsed_lines:
            decoded_line = line.encode('utf-8').decode('unicode_escape')
            f.write(decoded_line + '\n')
            
if __name__ == "__main__":
    json_file = 'recepturyPetfood_all_BM4.json'  # Replace with your JSON file path
    output_file = 'output.txt'  # Replace with your desired output file path
    find_empty_material_code(json_file, output_file)