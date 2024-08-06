# File System Analyzer
![Coverage](https://github.com/fedutinova/fsa/coverage.svg)
[![Pipeline](https://github.com/fedutinova/fsa/actions/workflows/analyzer.yml/badge.svg)](https://github.com/fedutinova/fsa/actions/workflows/analyzer.yml)

It is a command-line tool for analyzing directories. It provides functionality to categorize files by MIME type, calculate total sizes of files in each category, report files with unusual permissions, and find large files exceeding a specified size threshold.

## Features

- **Directory Traversal**: Traverse through a specified directory recursively.
- **File Type Categorization**: Classify files into categories (e.g., text, image, executable, etc.) based on their extensions.
- **Size Analysis**: Calculates the total size of files in each category.
- **Permission Analysis**: Reports files with unusual permissions such as world-writable, SUID, SGID, and sticky bit set.
- **Large File Detection**: Identifies files larger than a threshold.   

## Requirements

- Python 3.3 or higher
- futures3
- invoke


## Usage

To use the tool, run the script and provide the directory and desired arguments. For example:

```bash
# Clone the repository
git clone https://github.com/fedutinova/fsa.git

# Change to the project directory
cd fsa

# Build the project
invoke build

# Run the executable
cd dist
./fsa /path/to/directory -h
```

### Arguments

```text
positional arguments:
  directory             Directory to analyze

options:
  -h, --help            show this help message and exit
  -c, --categorize      Categorize files by type
  -s, --size_analysis   Calculate total size for each file type
  -p, --permissions_report
                        Report files with unusual permissions
  -l [LARGE_FILES], --large_files [LARGE_FILES]
                        Identify files larger than specified size (in bytes), default is 10485760 bytes
```

## Running Tests

Unit tests are provided to ensure the correctness of the script. To run the tests, use the following command:

```bash
invoke test
```
