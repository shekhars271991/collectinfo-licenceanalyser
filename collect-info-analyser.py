import subprocess
import re
import sys
from pathlib import Path
import openpyxl

def run_summary(file_path: Path):
    """Run asadm summary command on a collectinfo file and return cluster name + license usage in GB"""
    cmd = ['asadm', '-c', '-f', str(file_path), '-e', 'summary']
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"❌ Failed to process {file_path.name}, error: {stderr.strip()}")
            return None, None

        # Extract cluster name
        cluster_match = re.search(r"Cluster Name\s*\|\s*(.*)", stdout)
        cluster_name = cluster_match.group(1).strip() if cluster_match else "Unknown"

        # Extract license usage latest and convert to GB
        license_match = re.search(r"License Usage Latest\s*\|\s*([\d\.]+)\s*([A-Z]+)", stdout)
        if license_match:
            value = float(license_match.group(1))
            unit = license_match.group(2).upper()
            
            # Convert to GB
            if unit == "B":
                license_usage_gb = value / (1024 ** 3)
            elif unit == "KB":
                license_usage_gb = value / (1024 ** 2)
            elif unit == "MB":
                license_usage_gb = value / 1024
            elif unit == "GB":
                license_usage_gb = value
            elif unit == "TB":
                license_usage_gb = value * 1024
            elif unit == "PB":
                license_usage_gb = value * (1024 ** 2)
            else:
                print(f"⚠️ Unknown unit '{unit}' for {file_path.name}, treating as bytes")
                license_usage_gb = value / (1024 ** 3)
            
            # Round to 2 decimal places
            license_usage_gb = round(license_usage_gb, 2)
        else:
            license_usage_gb = None

        return cluster_name, license_usage_gb

    except Exception as e:
        print(f"⚠️ Error running summary on {file_path}: {e}")
        return None, None


def main():
    if len(sys.argv) != 2:
        print("Usage: python collectinfo_summary.py <path>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Path does not exist: {input_path}")
        sys.exit(1)

    # Create Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "License Usage"
    ws.append(["File", "Cluster Name", "License Usage (GB)"])

    # Process all files
    for file in input_path.iterdir():
        if file.is_file():
            print(f"🔍 Processing {file.name}...")
            cluster_name, license_usage_gb = run_summary(file)
            if cluster_name and license_usage_gb is not None:
                ws.append([file.name, cluster_name, license_usage_gb])

    # Save results
    output_file = input_path / "collectinfo_license_usage.xlsx"
    wb.save(output_file)
    print(f"✅ Results written to {output_file}")


if __name__ == "__main__":
    main()
