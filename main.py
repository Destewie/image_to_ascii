import sys
from PIL import Image
from utils import get_file_format_by_header, file_exists, valid_folder

SYMBOLS = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi}C{fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
SYMBOL_BRIGHTNESS = [0, 0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037, 0.9999]

PRECISIONS = [50, 40, 30, 25, 20, 15, 10, 5]

if __name__ == "__main__":

    #----------------------- initial checks -----------------------
    if len(sys.argv) not in [3, 4]:
        print(f"Usage: python3 main.py <image path> <output path> <optional: detail (min=1 ; max={len(PRECISIONS)})> ")
        exit(1)

    input_file_path = sys.argv[1]
    input_file_name = ""

    save_file = True
    output_file_path = sys.argv[2]

    if not file_exists(input_file_path):
        print("File not found")
        exit(1)
    else:
        input_file_name = input_file_path.split("/")[-1]
        print(input_file_name)
    
    if get_file_format_by_header(input_file_path) not in ["JPEG", "PNG"]:
        print("Unsupported file format, JPEG works best.")
        exit(1)
    
    #check that final folder exists
    if(not valid_folder(output_file_path)):
        save_file = False
        print("Output folder not found as second parameter. No file will be saved.")
        

    precision = 4
    if len(sys.argv) == 4 and sys.argv[3].isdigit() and 1 <= int(sys.argv[3]) <= len(PRECISIONS):
        precision = int(sys.argv[3])
    else:
        print(f"You can define a custom precision from 1 to {len(PRECISIONS)} after the file path")
        print("Using default precision: 3")

    #----------------------- main code -----------------------
    
    #take the dimension in pixels of the image
    img = Image.open(input_file_path)
    width, height = img.size
    pixel_group_side = PRECISIONS[precision-1] #take every nxn pixel group of the image
    width_groups = width // pixel_group_side
    height_groups = height // pixel_group_side
    ascii_image = []

    #scorro per blocchi nxn
    for i in range(height_groups): #dall'alto in basso
        for j in range(width_groups): #da sinistra a destra

            #qui prendo la luminosità media del blocco di pixel
            current_block_average_brightness = 0
            for a in range(pixel_group_side):
                for b in range(pixel_group_side):
                    try:
                        r, g, b = img.getpixel((b + pixel_group_side * j, a + pixel_group_side * i))
                    except:
                        r, g, b = 0, 0, 0
                    current_block_average_brightness += (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
            current_block_average_brightness /= (pixel_group_side ** 2)

            #qui trovo il simbolo corrispondente alla luminosità media
            symbol_index = 0
            for k in range(len(SYMBOL_BRIGHTNESS)):
                if current_block_average_brightness > SYMBOL_BRIGHTNESS[k]:
                    symbol_index = k
            ascii_image.append(SYMBOLS[symbol_index])
        ascii_image.append("\n")
    
    print("".join(ascii_image))


    #save the ascii image to a file
    if save_file:
        if not output_file_path.endswith("/"):
            output_file_path += "/"
        
        if "." in input_file_name:
            output_file_name = input_file_name.split(".")[0] + "_ascii.txt"
        else:
            output_file_name = input_file_name + "_ascii.txt"

        output_file_path = output_file_path + output_file_name

        with open(output_file_path, "w") as file:
            #write the ascii image to the file
            file.write("".join(ascii_image))
        
        print(f"File saved as {output_file_path}")



        
       
    