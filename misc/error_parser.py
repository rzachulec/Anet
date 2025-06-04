import re

def parse_errors(file_path):
    surowiec_set = set()
    skladnik_set = set()
    cennik_set = set()
    
    def remove_trailing_pipe(value):
        return value.rstrip('|')

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            surowiec_match = re.search(r'Surowiec <(.*?)>', line)
            skladnik_match = re.search(r'Składnik pokarmowy <(.*?)>', line)
            cennik_match = re.search(r'Cennik surowcowy <(.*?)>', line)
            
            if surowiec_match:
                surowiec_value = surowiec_match.group(1)
                if surowiec_value:
                    surowiec_set.add(surowiec_value)
                    
            if skladnik_match:
                skladnik_value = skladnik_match.group(1)
                if skladnik_value:
                    skladnik_set.add(skladnik_value)
            
            if cennik_match:
                cennik_value = cennik_match.group(1)
                if cennik_value:
                    cennik_set.add(cennik_value)

    return surowiec_set, skladnik_set, cennik_set

def save_to_file(surowiec_set, skladnik_set, cennik_set, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("Unique Surowiec:\n")
        for surowiec in sorted(surowiec_set):
            file.write(f"{surowiec}\n")
            
        file.write("Unique Składnik pokarmowy:\n")
        for skladnik in sorted(skladnik_set):
            file.write(f"{skladnik}\n")
        
        file.write("\nUnique Cennik surowcowy:\n")
        for cennik in sorted(cennik_set):
            file.write(f"{cennik}\n")

if __name__ == "__main__":
    input_file_path = '/Users/jan/OS IMAGES/Win 11/Shared/bledy10.txt'
    output_file_path = '/Users/jan/OS IMAGES/Win 11/Shared/unique_values10.txt'
    
    surowiec_set, skladnik_set, cennik_set = parse_errors(input_file_path)
    save_to_file(surowiec_set, skladnik_set, cennik_set, output_file_path)