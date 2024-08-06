def find_large_files(file_info, size_threshold):
    large_files = []
    for file_path, size, _ in file_info:
        if size > size_threshold:
            large_files.append(file_path)
    return large_files
