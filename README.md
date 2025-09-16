# Collect Info Analyser

A Python script that processes Aerospike collectinfo files to extract cluster names and license usage information.

## Features

- Processes multiple collectinfo files in a directory
- Extracts cluster name and license usage from each file
- Automatically converts license usage to GB (from any unit: B, KB, MB, GB, TB, PB)
- Outputs results to an Excel file for easy analysis

## Requirements

- Python 3.6+
- `asadm` (Aerospike Admin tool) installed and available in PATH
- Required Python packages:
  - `openpyxl`

## Installation

Install the required Python package:

```bash
pip install openpyxl
```

## Usage

```bash
python collect-info-analyser.py <path_to_directory>
```

Where `<path_to_directory>` is the directory containing your collectinfo files.

## Example

```bash
python collect-info-analyser.py /path/to/collectinfo/files/
```

## Output

The script creates an Excel file named `collectinfo_license_usage.xlsx` in the input directory with the following columns:

- **File**: Name of the collectinfo file
- **Cluster Name**: Extracted cluster name
- **License Usage (GB)**: License usage converted to GB (rounded to 2 decimal places)

## Notes

- The script uses `asadm summary` command to extract information from collectinfo files
- License usage is automatically converted to GB regardless of the original unit
- Files that cannot be processed will show error messages but won't stop the script
- Only files (not subdirectories) in the specified path are processed
