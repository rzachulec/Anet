from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import re
import os

surowce_tables = [
    "Weende analysis", "Minerals and trace elements", "Fermentation products", "DVE/OEB 2007",
    "Feeding values ruminants", "Feeding values rabbits", "Feeding values horses",
    "Feeding values roosters/laying hens", "Feeding values broilers", "Feeding values pigs",
    "Amino acid contents", "Fatty acids", "Miscellaneous"
]
    
matryce_tables = [
    "Digestibility coefficients ruminants", "Digestibility coefficients pigs", "Digestibility coefficients roosters and laying hens",
    "Digestibility coefficients broilers", "Digestibility coefficients rabbits", "Digestibility coefficients horses",
    "Standardized digestibility coefficients amino acids pigs", "Amino acid contents"
    , "Standardized ileal digestibility coefficients amino acids poultry"
    , "Fatty acids"
]

SDCAAP = [
    "CAL_%idAA", "sta%idLYSpig", "sta%idMETpig", "sta%idCYSpig", "sta%idTHRpig", "sta%idTRPpig", "sta%idILEpig", "sta%idARGpig", "sta%idPHEpig", "sta%idHISpig", "sta%idLEUpig", "sta%idTYRpig", "sta%idVALpig", "sta%idALApig", "sta%idASPpig", "sta%idGLUpig", "sta%idGLYpig", "sta%idPROpig", "sta%idSERpig"
]

SIDCAAP = [
    "%dLYSpoultry", "%dMETpoultry", "%dCYSpoultry", "%dTHRpoultry", "%dTRPpoultry", "%dILEpoultry", "%dARGpoultry", "%dPHEpoultry", "%dHISpoultry", "%dLEUpoultry", "%dTYRpoultry", "%dVALpoultry", "%dALApoultry", "%dASPpoultry", "%dGLUpoultry", "%dGLYpoultry", "%dPROpoultry", "%dSERpoultry"
]

DCRUM = {
    "DCCP":     "%dCPrum",
    "DCCFAT":   "%dCFATrum",
    "DCCF":	    "%dCFIBRErum",
    "DCNFE":	"%dNFErum",
    "DCOM":	    "%dOMrum",
}

DCP = {
    "DCCP":	    "%dCPpig",
    "DCCFATh":  "%dCFAThpig",		
    "DCCF":	    "%dCFIBREpig",
    "DCNFE":	"%dNFEpig",
    "DCOM":	    "%dOMpig",
    "DCNSPh":	"%dNSPpig",
    "DCiSTA":	"%idSTARCH"
}

DCRLH = {
    "DCCP":	    "%dCPpoultry",
    "DCCFAT":   "%dCFATpoultry",
    "DCNFE":    "%dNFEpoultry",
    "DCPpo":    "%dPpoultry"
}

DCB = {
    "DCCP":     "%dCPbroiler",
    "DCCFATh":  "%dCFAThbroiler"
}

DCRAB = {
    "DCCP":     "%dCPrabbit",
    "DCCFAT":   "%dCFATrabbit",
    "DCCF":     "%dCFIBRErabbit",
    "DCNFE":    "%dNFErabbit"
}

DCH = {
    "DCCP":	    "%dCPhorse",
    "DCOM":	    "%dOMhorse"
}

def sanitize_filename(filename):
    """Removes invalid characters from filenames."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def save_to_csv(filename, data):
    """Saves extracted data into a CSV file with a sanitized filename."""
    filename = sanitize_filename(filename)  # Sanitize filename
    file_path = os.path.join(os.getcwd(), filename)  # Ensure valid path

    print(f"Saving data to {file_path}...")
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Label", "Value", "Unit"])
        writer.writerows(data)
    print(f"Data saved to {file_path} successfully.")

def extract_table_data(table):
    """Extracts relevant data from the table."""
    data = []
    for row in table.find_elements(By.TAG_NAME, "tr"):
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 4:
            label = cells[0].text.strip()
            value = cells[1].text.strip()
            unit = cells[3].text.strip()
            data.append([label, value, unit])
    return data

def process_product(product_name, driver, wait, subclass_cnt):
    print("Clicking 'Get values' button...")
    get_values_btn = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Cp1_ucVwCalc_BtnFillGrid_input")))
    get_values_btn.click()

    wait.until(EC.staleness_of(get_values_btn))
    time.sleep(0.5)
        
    product_code = driver.find_element(By.ID, "ctl00_Cp1_ucVwCalc_txtProductcode")
    product_code = product_code.text.strip()
    print(f"Product code: {product_code}")

    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"Found {len(tables)} tables.")

    surowce_data = []
    matryca_data = []
    prev_title = ""
    aa_cnt = 0
    
    for table in tables:
        try:
            title_element = table.find_element(By.XPATH, "preceding-sibling::h2[1]")
            title = title_element.text.strip()
        except:
            continue
        extracted_data = extract_table_data(table)
        
        # print(f"Prev title: \t {prev_title}, \ntitle: \t\t {title}")
        if title in surowce_tables and title != 'Amino acid contents' and title != 'Fatty acids':
            surowce_data.extend(extracted_data)
            print(f"Processing surowce table: {title}...\n")
                
        elif title in matryce_tables and title != 'Amino acid contents' and title != 'Fatty acids':
            if title == 'Standardized digestibility coefficients amino acids pigs':
                for row in extracted_data:
                    for code in SDCAAP:
                        if row[0].lower() in code.lower():
                            row[0] = code
                            break
            if title == 'Standardized ileal digestibility coefficients amino acids poultry':
                for row in extracted_data:
                    for code in SIDCAAP:
                        if row[0].lower() in code.lower():
                            row[0] = code
                            break
            if title == 'Digestibility coefficients ruminants':
                for row in extracted_data:
                    key = row[0]
                    if key in DCRUM:
                        row[0] = DCRUM[key]
            if title == 'Digestibility coefficients pigs':
                for row in extracted_data:
                    key = row[0]
                    if key in DCP:
                        row[0] = DCP[key]
            if title == 'Digestibility coefficients roosters and laying hens':
                for row in extracted_data:
                    key = row[0]
                    if key in DCRLH:
                        row[0] = DCRLH[key]
                        if key == 'DCCFAT':
                            extracted_data.append(['%dCFATlayer', row[1], row[2]])
            if title == 'Digestibility coefficients broilers':
                for row in extracted_data:
                    key = row[0]
                    if key in DCB:
                        row[0] = DCB[key]
            if title == 'Digestibility coefficients rabbits':
                for row in extracted_data:
                    key = row[0]
                    if key in DCRAB:
                        row[0] = DCRAB[key]
            if title == 'Digestibility coefficients horses':
                for row in extracted_data:
                    key = row[0]
                    if key in DCH:
                        row[0] = DCH[key]
            
            matryca_data.extend(extracted_data)
            print(f"Processing matryca table: {title}...\n")
                
        if title == 'Amino acid contents':
            if prev_title == 'Amino acid contents':
                surowce_data.extend(extracted_data)
                print(f"Processing surowce table: {title}...\n")
            else:
                matryca_data.extend(extracted_data)
                print(f"Processing matryca table: {title}...\n")
                
        if title == 'Fatty acids':
            if prev_title == 'Fatty acids':
                matryca_data.extend(extracted_data)
                print(f"Processing matryca table: {title}...\n")
            else:
                surowce_data.extend(extracted_data)
                print(f"Processing surowce table: {title}...\n")
                
        prev_title = title
    
    if subclass_cnt > 0:
        filename = f"{product_name[:-1]}{subclass_cnt}{product_name[-1:]}"
    else:
        filename = product_name
        
    if surowce_data:
        save_to_csv(f"{filename}_surowce.csv", surowce_data)
    if matryca_data:
        save_to_csv(f"{filename}_matryca.csv", matryca_data)
        
    print(f"Finished processing {filename}.")    

def scrape_vwcalc():
    url = "https://vvdb.cvbdiervoeding.nl/Manage/Tools/VwCalc.aspx"
    print("Launching Chrome WebDriver...")
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    print("Waiting for page to load...")
    time.sleep(1)

    print("Fetching product list...")
    dropdown_arrow = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Cp1_ucVwCalc_ddlProducten_Arrow")))
    dropdown_arrow.click()
    time.sleep(0.2)

    dropdown_options = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.rcbList li"))
    )
    product_names = [option.text.strip() for option in dropdown_options if option.text.strip()]
    print(f"Found {len(product_names)} products: {product_names}")
    
    dropdown_arrow.click()
    time.sleep(0.2)
    
    failed_products = []

    # product_names = []
    for product_name in product_names:
        # Skip processing if file already exists for this product
        existing_files = os.listdir(os.getcwd())
        product_first_two = " ".join(sanitize_filename(product_name).split()[:2]).lower()
        should_skip = any(
            os.path.splitext(sanitize_filename(f))[0].lower().startswith(product_first_two)
            for f in existing_files
        )
        if should_skip:
            print(f"Skipping {product_name} as file already exists.")
            continue
        print(f"Processing product: {product_name}...")
        dropdown_arrow = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_Cp1_ucVwCalc_ddlProducten_Arrow")))
        dropdown_arrow.click()
        time.sleep(0.5)

        print(f"Selecting {product_name} from dropdown using JavaScript...")
        driver.execute_script("""
            let dropdown = document.getElementById('ctl00_Cp1_ucVwCalc_ddlProducten_Input');
            dropdown.value = arguments[0];
            dropdown.dispatchEvent(new Event('input', { bubbles: true }));
            dropdown.dispatchEvent(new Event('change', { bubbles: true }));
        """, product_name)


        dropdown_arrow.click()
        # Check for subclass dropdown options§
        subclass_dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctl00_Cp1_ucVwCalc_ddlKlasse")))
        time.sleep(0.1)

        # Check if the subclass dropdown is already open
        is_open = driver.execute_script("""
            let dropdown = document.getElementById('ctl00_Cp1_ucVwCalc_ddlKlasse_DropDown');
            if (!dropdown) return false;
            return dropdown.style.display === 'block' && dropdown.style.visibility === 'visible';
        """)
        if not is_open:
            try:
                subclass_dropdown.click()
                time.sleep(0.4)
            except:
                print(f"Product {product_name} failed.")
                failed_products.append(product_name)
                print(failed_products)


        print("Getting subclass options using JavaScript...")
        subclass_options = driver.execute_script("""
            let dropdown = document.getElementById('ctl00_Cp1_ucVwCalc_ddlKlasse_DropDown');
            let popup = dropdown.querySelector('.rddlPopup');
            console.log("Popup element:", popup);
            if (!popup) return [];
            let items = popup.querySelectorAll("li");
            console.log("Found subclass items:", items.length);
            return Array.from(items).map(i => i.textContent.trim());
        """)
        time.sleep(0.2)
        print("Subclass options: ", subclass_options)
        subclass_names = [name for name in subclass_options if name]
        print("Subclass names: ", subclass_names)

        # If only the default option is present, process as usual
        if len(subclass_names) <= 1:
            time.sleep(0.2)
            
            process_product(product_name, driver, wait, 0)
        else:
            subclass_cnt = 1
            for subclass_name in subclass_names:
                print(f"Selecting subclass: {subclass_name}...")
                driver.execute_script("""
                    let dropdown = document.getElementById('ctl00_Cp1_ucVwCalc_ddlKlasse_DropDown');
                    let popup = dropdown.querySelector('.rddlPopup');
                    if (!popup) return;
                    let items = popup.querySelectorAll("li");
                    for (let item of items) {
                        if (item.textContent.trim() === arguments[0]) {
                            item.click();
                            break;
                        }
                    }
                """, subclass_name)
                
                time.sleep(0.1)
                # Update subclass_name to be filename-safe
                safe_subclass_name = subclass_name.replace('<', 'less than').replace('>', 'greater than').replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('|', '_')
                # Insert safe_subclass_name before the product code in brackets
                match = re.match(r"^(.*?)(\s*\([^)]+\))$", product_name)
                if match:
                    name_part, code_part = match.groups()
                    full_product_name = f"{name_part}, {safe_subclass_name}{code_part}"
                else:
                    full_product_name = f"{product_name}, {safe_subclass_name}"
                process_product(full_product_name, driver, wait, subclass_cnt)
                subclass_cnt += 1;
                
    print(failed_products)

    print("Closing WebDriver...")
    driver.quit()
    print("Scraping complete.")

if __name__ == "__main__":
    scrape_vwcalc()
