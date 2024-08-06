import os


def get_file_info(file_path):
    try:
        size = os.path.getsize(file_path)
        mode = os.stat(file_path).st_mode
        return (file_path, size, mode)
    except OSError as e:
        print(f"Error accessing {file_path}: {e}")
        return None
