#loads a blank template of a size, imports an array/image, and sets the heighs
#of the terrain file accordingly.

from ParseMap import parse_map
import cv2
import numpy as np

def load_image(image_filename, squish_vertical, template_data):
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
    gray_image_scaled = gray_image_normalized * (max_level - min_level) + min_level

    #rescale the image to fit the template map.
    template_size = template_data["Singletons"]["MapSize"]["Size"]
    x_size = template_size["X"]
    y_size = template_size["Y"]
    print(x_size, y_size)

if __name__ == "__main__":
    template_filename = "Blank_128_128.timber"
    image_filename = "Iceland_01_512x512.png"
    squish_vertical = 0.2 #value from 0 to 1. 0 is flat, 1 is normalized scale.
    #loads template.
    template_data = parse_map(template_filename)
    print(template_data)
    #loads input image.
    load_base_image = load_image(image_filename, squish_vertical, template_data)
    #rescales input image to correct size / resolution / heights.
    #writes new map.
    #zips up new map back into the .timber format.
