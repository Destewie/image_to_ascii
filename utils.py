def get_file_format_by_header(file_path):
    with open(file_path, 'rb') as f:
        header = f.read(4)  # Read the first 4 bytes of the file
        if header.startswith(b'\xFF\xD8'):
            return "JPEG"
        elif header.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
            return "PNG"
        elif header.startswith(b'\x47\x49\x46\x38\x37\x61') or header.startswith(b'\x47\x49\x46\x38\x39\x61'):
            return "GIF"
        elif header.startswith(b'\x42\x4D'):
            return "BMP"
        elif header.startswith(b'\x49\x49\x2A\x00') or header.startswith(b'\x4D\x4D\x00\x2A'):
            return "TIFF"
        else:
            return "Unknown"
        
def file_exists(file_path):
    try:
        with open(file_path, "r") as file:
            pass
    except FileNotFoundError:
        return False
    return True
