import sys
import os
import subprocess

from RedStakeGUI.constants import DATA_DIRECTORY

BASE_URL = "https://vector.express/api/v2/public/convert"


def convert_dwg_to_pdf(dwg_file, pdf_file, batch_file_path):
    # You can add other options according to your requirements
    cmd = [
        batch_file_path,
        "-o",
        pdf_file,  # Output file
        "-a",  # Auto fit and center drawing to paper
        "-l",  # Landscape mode
        dwg_file,  # Input DWG file
    ]

    try:
        subprocess.run(cmd, check=True, shell=True)
        print(f"Converted {dwg_file} to {pdf_file}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")


if __name__ == "__main__":
    batch_file_name = "dwg2pdf.bat"
    current_directory = os.path.dirname(os.path.realpath(__file__))
    batch_file_path = os.path.join(current_directory, batch_file_name)
    print(DATA_DIRECTORY)
    input_file = "test.dwg"
    print(input_file)
    output_file = "test.pdf"
    compressed_file = DATA_DIRECTORY / "test.zip"

    # convert_dwg_to_pdf(input_file, output_file)
    convert_dwg_to_pdf(input_file, output_file, batch_file_path)
