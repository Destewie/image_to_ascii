import sys
from utils import get_file_format_by_header, file_exists

if __name__ == "__main__":

    #----------------------- initial checks -----------------------
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <image path>")
        exit(1)

    file_path = sys.argv[1]

    if not file_exists(file_path):
        print("File not found")
        exit(1)
    else:
        #print filename
        print(file_path.split("/")[-1])
    
    if get_file_format_by_header(file_path) != "JPEG":
        print("Unsupported file format")
        exit(1)

    #----------------------- main code -----------------------
    
    
    