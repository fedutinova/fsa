import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from analyzer.file_info import get_file_info


def traverse_directory(directory):
    file_info = []
    #ThreadPoolExecutor is used to speed up the process by handling I/O-bound tasks.
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                futures.append(executor.submit(get_file_info, file_path))
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                file_info.append(result)
  
    return file_info
