import mimetypes
from collections import defaultdict


def categorize_files(file_info):
    categorized_files = defaultdict(list)
    for file_path, size, mode in file_info:
        # I could use the mimetypes or magic library, but chose mimetypes because it is faster.
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            category = mime_type.split('/')[0]
        else:
            category = 'unknown'
        categorized_files[category].append((file_path, size, mode))
    return categorized_files


def calculate_total_size(categorized_files):
    total_sizes = {}
    for category, files in categorized_files.items():
        total_sizes[category] = sum(size for _, size, _ in files)
    return total_sizes
