#loads a blank template of a size, imports an array/image, and sets the heighs
#of the terrain file accordingly.

from ParseMap import parse_map


if __name__ == "__main__":
    template_filename = "Blank_128_128.timber"
    image_filename = ""
    #loads template.
    template_data = parse_map(template_filename)
    #loads input image.
    load_base_image = image_filename
    #rescales input image to correct size / resolution / heights.
    #writes new map.
    #zips up new map back into the .timber format.
