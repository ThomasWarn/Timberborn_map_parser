#extracts and processes the .timber map designated.
import zipfile
from os import getcwd, path, makedirs
import json

def extract_map(map_filename):
    #extracts the map file to a zip.
    #inputs: map filename
    #outputs: extracted file, filepath.

    temp_folder = "extracted_map"
    current_dir = getcwd()
    abs_path = path.join(current_dir, map_filename)
    
    #makes output folder
    try:
        if not path.exists(temp_folder):
            makedirs(temp_folder)
    except Exception as error:
        print(f"An error occurred: {str(error)}")
    
    #extracts zip
    try:
        with zipfile.ZipFile(map_filename,"r") as zip_source:
            zip_source.extractall(temp_folder)
    except Exception as error:
        print(f"An error occurred: {str(error)}")

    #returns the extraction location.
    return path.join(current_dir, temp_folder)
    
def convert_json(map_extract_location):
    map_json_filename = "world.json"
    abs_map_filename = path.join(map_extract_location, map_json_filename)
    try:
        with open(abs_map_filename, "r") as json_in:
            data = json.load(json_in)
    except Exception as error:
        print(f"An error occurred: {str(error)}")
    #for key, value in data.items():
    #    print(key)
    
    return data

def parse_map(map_filename):
    #extracts map file from zip into new folder.
    map_extract_location = extract_map(map_filename)

    #parses map into json
    map_data = convert_json(map_extract_location)

if __name__ == "__main__":
    filename = "Blank_128_128.timber"
    parse_map(filename)
