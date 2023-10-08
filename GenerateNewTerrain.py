#loads a blank template of a size, imports an array/image, and sets the heighs
#of the terrain file accordingly.

from ParseMap import parse_map
import cv2
import numpy as np
import json
from os import popen, path, makedirs, getcwd

def load_image(image_filename, squish_vertical, template_data, blur_factor):
    #input: image filepath
    #output: grayscale height array normalized 1-64.

    image_data = cv2.imread(image_filename)
    assert type(image_data) != None, "Error: Image probably not found"

    gray_image = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)

    #normalize from 0 to 1.
    gray_image_max = np.amax(gray_image)
    gray_image_min = np.amin(gray_image)
    gray_image_normalized = (gray_image - gray_image_min)/(gray_image_max-gray_image_min)

    #chunk the image from 2 to 64*squish_vertical
    min_level = 2 #not 1 because 1 is reserved for the overall image-black.
    max_level = int(64 * squish_vertical)
    gray_image_scaled = np.array(gray_image_normalized * (max_level - min_level) + min_level,dtype = np.uint8)
    print(gray_image_scaled)

    #setting the lowest level to 1.
    min_mask = gray_image == gray_image_min
    gray_image_scaled[min_mask] = 1
    
    #rescale the image to fit the template map.
    template_size = template_data["Singletons"]["MapSize"]["Size"]
    x_size = template_size["X"]
    y_size = template_size["Y"]
    image_shape = gray_image_scaled.shape

    if image_shape != (y_size, x_size):
        print(f"Image size is not same as map size. Rescaling.")
    if image_shape[0]/image_shape[1] != y_size/x_size:
        print(f"Image aspect ratio is not same as map aspect ratio. This may cause poor results. Rescaling.")
        
    gray_image_scaled = cv2.resize(gray_image_scaled, (y_size, x_size), interpolation=cv2.INTER_AREA)
    radius = max(1, 1+int(blur_factor/2))
    gray_image_blurred = cv2.bilateralFilter(gray_image_scaled,radius,75,75)

    return gray_image_blurred

def write_new_map(template_data, base_image):

    #injecting new data.
    linearized = np.reshape(base_image, (len(base_image)*len(base_image[0])))
    linearized_string = ' '.join([str(i) for i in list(linearized)])
    #print(linearized_string)
    template_data["Singletons"]["TerrainMap"]["Heights"]["Array"] = linearized_string

    return template_data

def export_map(modified_template_data, output_filename, output_folder_name, temp_folder):
    #makes output folder
    try:
        if not path.exists(output_folder_name):
            makedirs(output_folder_name)
    except Exception as error:
        print(f"An error occurred: {str(error)}")

    #copy over version.txt
    current_dir = getcwd()
    try:
        try:
            command = f'copy {path.join(current_dir,temp_folder)}\\version.txt {path.join(current_dir,output_folder_name)}\\version.txt'
            popen(command) #windows
            print(command)
        except Exception as error:
            print(f"An error occurred: {str(error)})\n Trying linux compatability.")
            popen('cp {temp_folder}/version.txt {output_folder_name}/version.txt') #linux
    except Exception as error:
        print(f"An error occurred: {str(error)})")

    #writes new json.
    with open(f'{output_folder_name}/world.json', 'w', encoding='utf-8') as out_json:
        json.dump(modified_template_data, out_json, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    template_filename = "Blank_512_512.timber"
    temp_folder = "extracted_map"
    output_filename = "Output.timber"
    output_folder_name = "Output"
    image_filename = "Iceland_01_512x512.png"
    blur_factor = 5 #should be an odd number as the radius (eg. 1, 3, 5)
    squish_vertical = 0.5 #value from 0 to 1. 0 is flat, 1 is normalized scale.
    #loads template.
    template_data = parse_map(template_filename, temp_folder)
    #loads input image, rescales input image to correct size / resolution / heights.
    base_image = load_image(image_filename, squish_vertical, template_data, blur_factor)
    #writes new map.
    modified_template_data = write_new_map(template_data, base_image)
    #zips up new map back into the .timber format.
    export_map(modified_template_data, output_filename, output_folder_name, temp_folder)
