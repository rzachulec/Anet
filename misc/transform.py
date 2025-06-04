#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import sys
import csv
import os

import xml.etree.ElementTree as ET
import json

def convert_xml_to_json(xml_file, json_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    recipes = []
    compounds = root.find('Compounds')
    if compounds is None:
        print("No compounds found in the XML file.")
        return
    
    for compound in compounds.findall('Compound'):
        compound_header = compound.find('CompoundHeader')
        if compound_header is None:
            print("CompoundHeader not found for a compound; skipping.")
            continue
        
        recipe = {}
        recipe_code = compound_header.findtext('Code', default="")
        description = compound_header.findtext('Description', default="No description").strip()
        recipe["RecipeCode"] = generate_recipe_code(description) if recipe_code == "" else recipe_code
        recipe["RecipeTemplateCode"] = "AD_Default"
        recipe["RecipeSiteCode"] = compound_header.findtext('PlantCode', default="1")
        recipe["RecipeVersion"] = 1
        recipe["CompositionStateIncName"] = "Free"
        recipe["Dimensions"] = []
        recipe["ListIngredientSettings"] = []
        recipe["InclusionRate"] = 100.0
        recipe["InclusionRateDM"] = 100.0
        recipe["EvaporationFactor"] = 1.0
        recipe["WeightUnitCode"] = compound_header.findtext('WeightUnitCode', default="kg")
        recipe["PriceUnitCode"] = compound_header.findtext('PriceUnitCode', default="PLN")
        price_weight_unit_code = compound_header.findtext('WeightUnitCode', default="kg")
        recipe["PriceWeightUnitCode"] = price_weight_unit_code
        recipe["FolderCode"] = "B" if price_weight_unit_code == "kg" else "" 
        
                # Define the required language codes
        required_languages = ["EN", "BG", "CS", "D", "DK", "ES", "FR", "FA", "FI", "HU", 
                            "IT", "KOR", "NL", "NO", "PL", "PT", "RO", "RU", "SK", "SW", 
                            "TR", "VI", "ZH"]

        # Parse descriptions from the <Descriptions> element (child of <Compound>)
        descriptions_element = compound.find('Descriptions')
        parsed_desc = {}
        if descriptions_element is not None:
            for desc in descriptions_element.findall('Description'):
                lang = desc.findtext('LanguageCode', default="EN").strip()
                desc_text = desc.findtext('DescriptionShort', default="No description").strip()
                if lang:
                    parsed_desc[lang] = desc_text

        # If no descriptions were found, fallback to using CompoundHeader/Description
        if not parsed_desc:
            header_desc = compound_header.findtext('Description', default="No description").strip()
            parsed_desc["EN"] = header_desc

        # Build the final description list, ensuring all required languages are included.
        final_descriptions = []
        for lang in required_languages:
            if lang in parsed_desc:
                final_descriptions.append({"LanguageCode": lang, "Description": parsed_desc[lang]})
            elif "EN" in parsed_desc:
                final_descriptions.append({"LanguageCode": lang, "Description": parsed_desc["EN"]})
            elif parsed_desc:
                # Use any available description if EN is not found
                any_desc = next(iter(parsed_desc.values()))
                final_descriptions.append({"LanguageCode": lang, "Description": any_desc})
            else:
                final_descriptions.append({"LanguageCode": lang, "Description": "No description"})

        recipe["Description"] = final_descriptions

        
        recipe["DescriptionExtended"] = []
        recipe["CreatedBy"] = compound_header.findtext('CreatedBy', default="")
        recipe["CreatedOn"] = str(compound_header.findtext('CreatedOn', default="") + "+01:00")
        recipe["ModifiedBy"] = compound_header.findtext('ChangedBy', default="")
        recipe["ModifiedOn"] = str(compound_header.findtext('ChangedOn', default="") + "+01:00")
        recipe["ActiveVersion"] = False
        recipe["DomainSubTypeName"] = "PercentualRecipe"
        recipe["AnimalTypeCode"] = compound_header.findtext('AnimalTypeCode', default="Unknown")
        recipe["IngredientPricelistCode"] = compound_header.findtext('PricelistCode', default="Unknown")
        recipe["BatchWeight"] = float(compound_header.findtext('BatchWeight', default="1000"))
        # Nutrient reference values (set to defaults if not present)
        recipe["ReferenceNutrientCode"] = "BX_PA01"
        recipe["ReferenceNutrientUnitCode"] = "%"
        recipe["ReferenceNutrientValue"] = 100.0
        recipe["OptimizeMinPricePerRefNutr"] = False
        recipe["AutocorrectHighestAmount"] = True
        recipe["CurrencyCode"] = recipe["PriceUnitCode"]
        recipe["CompositionStateName"] = "Free"
        recipe["LoadingSheetCompositionByName"] = "BatchWeight"
        recipe["LoadingSheetAmountFed"] = 100.0
        recipe["LoadingSheetRefusal"] = 0.0
        recipe["LoadingSheetPrintAmounts"] = False
        recipe["LoadingSheetPrintAccumulatedAmounts"] = False
        recipe["LoadingSheetPrintTotals"] = False
        recipe["TotalPrice"] = 999999900.0
        recipe["TotalWeight"] = 100.0
        recipe["TotalPercentage"] = 100.0
        recipe["PricePerRefNutr"] = 9999999.0
        recipe["Price"] = 9999999.0
        recipe["ParameterValues"] = []
        recipe["Analysis"] = []
        
        # Parse Composition from Constraints/Materials
        composition_list = []
        results = compound.find('Results')
        if results is not None:
                periods = results.find('Periods')
                if periods is not None:
                    for period in periods.findall('Period'):
                        materials = period.find('Materials')
                        if materials is not None:
                            for mat in materials.findall('Material'):
                                ingredient = {}
                                ingredient["MaterialCode"] = mat.findtext('MaterialCode', default="")
                                ingredient["MaterialDescription"] = mat.findtext('MaterialDescription', default="")
                                # ingredient["Id"] = int(mat.findtext('IngId', default="0"))
                                # Map MaterialType "0" to "Ingredient"; otherwise, use the tag value
                                material_type = mat.findtext('MaterialType', default="0")
                                ingredient["MaterialTypeName"] = "Ingredient" if material_type == "0" else material_type
                                weight = float(mat.findtext('Weight', default="0"))
                                ingredient["IngoingWeight"] = weight
                                # ingredient["DM"] = weight
                                # ingredient["OnRef"] = weight
                                # ingredient["Percentage"] = weight
                                # ingredient["PercentageDM"] = weight
                                # ingredient["PercentageRef"] = weight
                                # ingredient["RoundedBatch"] = weight*10
                                ingredient["Type"] = "Percentage"
                                composition_list.append(ingredient)
        recipe["Composition"] = composition_list
        
        constraints_element = compound.find('Constraints')
        if constraints_element is not None:
            nutrient_constraints = []
            nutrient_constraints_element = constraints_element.find('Nutrients')
            if nutrient_constraints_element is not None:
                seen_nutrient_codes = set()
                for nutr in nutrient_constraints_element.findall('Nutrient'):
                    nutrient_code = nutr.findtext('NutrientCode', default="")
                    if nutrient_code in seen_nutrient_codes:
                        continue
                    seen_nutrient_codes.add(nutrient_code)
                    
                    nutrient = {}
                    nutrient["NutrientCode"] = nutrient_code
                    nutrient["NutrientDescription"] = nutr.findtext('NutrientDescription', default="")
                    nutrient["UnitCode"] = nutr.findtext('UnitCode', default="%")
                    nutrient["Use"] = True
                    min = nutr.findtext('Minimum', default="")
                    if min != "":
                        nutrient["Minimum"] = float(min)
                    
                    nutrient["MinimumFromEquation"] = False
                    max = nutr.findtext('Maximum', default="")
                    if max != "":
                        nutrient["Maximum"] = float(max)
                    
                    nutrient["MaximumFromEquation"] = False
                    nutrient["LowerLimitFromEquation"] = False
                    nutrient["UpperLimitFromEquation"] = False
                    nutrient["ConstraintTypeName"] = "OnProduct"
                    if nutr.findtext("ValueType", default="") == "Product":
                        nutrient_constraints.append(nutrient)
            
            material_constraints = []
            material_constraints_element = constraints_element.find('Materials')
            if material_constraints_element is not None:
                for mat in material_constraints_element.findall('Material'):
                    material = {}
                    material["MaterialCode"] = mat.findtext('MaterialCode', default="")
                    material["MaterialDescription"] = mat.findtext('MaterialDescription', default="")
                    material_type = mat.findtext('MaterialType', default="0")
                    material["MaterialTypeName"] = "Ingredient" if material_type == "0" else "Unknown"
                    material["Use"]= True
                    min = mat.findtext('Minimum', default="")
                    if min != "":
                        material["Minimum"]= float(min)
                    
                    max = mat.findtext('Maximum', default="")
                    if max != "":
                        material["Maximum"]= float(max)
                    material["ConstraintTypeName"]= "Percentage"
                    material_constraints.append(material)
            recipe["MaterialConstraints"] = material_constraints
            recipe["NutrientConstraints"] = nutrient_constraints
        recipe["ExternalMaterialConstraints"] = []
        recipe["MaterialInfos"] = []
        recipe["ConcentrateRatioConstraints"] = []
        recipe["ConsolidatedMaterialConstraints"] = []
        recipe["InternalMaterialConstraints"] = []
        recipe["MainMaterialConstraints"] = []
        
        recipes.append(recipe)
    
    final_data = {"Recipes": recipes}
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"Conversion complete. JSON saved to {json_file}")

def generate_recipe_code(description):
    csv_file = 'RECIPE_CODES.csv'
    
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Code', 'Description'])
            writer.writerow(['BF_0001', description])
            return 'BF_0001'
    
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        codes = list(reader)
    
    # Check if the description already exists
    for code, desc in codes[1:]:  # Skip header
        if desc == description:
            return code
    
    if len(codes) <= 1:
        new_code = 'BF_0001'
    else:
        last_code = codes[-1][0]
        prefix = last_code[:-4]
        number = int(last_code[-4:]) + 1
        new_code = f"{prefix}{number:04d}"
    
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_code, description])
    
    return new_code

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python transform.py input.xml")
    else:
        input_xml = sys.argv[1]
        output_json = str(input_xml+"_BM4.json")
        convert_xml_to_json(input_xml, output_json)