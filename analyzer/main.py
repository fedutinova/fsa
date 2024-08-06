import argparse
import sys
import time

from analyzer.directory_traversal import traverse_directory
from analyzer.file_categorization import categorize_files, calculate_total_size
from analyzer.file_permissions import categorize_permissions
from analyzer.large_files import find_large_files

MEGABYTE = 1048576

def create_parser():
    parser = argparse.ArgumentParser(description='Directory analysis tool')
    parser.add_argument('directory', type=str, help='Directory to analyze')
    parser.add_argument('-c', '--categorize', action='store_true', help='Categorize files by type')
    parser.add_argument('-s', '--size_analysis', action='store_true', help='Calculate total size for each file type')
    parser.add_argument('-p', '--permissions_report', action='store_true', help='Report files with unusual permissions')
    parser.add_argument('-l', '--large_files', type=int, nargs='?', const=10485760,
                        help='Identify files larger than specified size (in bytes), default is 10485760 bytes')
    return parser

def main():
    parser = create_parser()

    try:
        args = parser.parse_args(sys.argv[1:])
    except SystemExit:
        print("Invalid input. Please provide the directory and at least one argument.")
        return

    if not (args.categorize or args.size_analysis or args.permissions_report or args.large_files is not None):
        print("Please provide at least one argument: --categorize, --size_analysis, --permissions_report, --large_files")
        return

    # start_time = time.time()
    file_info = traverse_directory(args.directory)
    # end_time = time.time()
    # time_difference = end_time - start_time
    # print(f"Time taken for traversal: {time_difference:.2f} seconds")

    if args.categorize:
        categorized_files = categorize_files(file_info)
        print("Categorized files:")
        for category, files in categorized_files.items():
            print(f"{category}: {len(files)} files")

    if args.size_analysis:
        categorized_files = categorize_files(file_info)
        total_sizes = calculate_total_size(categorized_files)
        print("Total size for each file type:")
        for category, size in total_sizes.items():
            print(f"{category}: {size / MEGABYTE:.2f} MB")

    if args.permissions_report:
        permissions_categories = categorize_permissions(file_info)
        found_any = False
        for category, files in permissions_categories.items():
            if files:
                found_any = True
                print(f"{category}: {len(files)} files")
                for file_path in files:
                    print(f"  {file_path}")
        if not found_any:
            print("No files with unusual permission settings found.")

    if args.large_files is not None:
        large_files = find_large_files(file_info, args.large_files)
        if large_files:
            print(f"Files larger than {args.large_files / MEGABYTE:.2f} MB:")
            for file_path in large_files:
                print(file_path)
        else:
            print(f"No files larger than {args.large_files / MEGABYTE:.2f} MB found.")


if __name__ == '__main__':
    main()
