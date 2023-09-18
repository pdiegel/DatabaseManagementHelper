import sys
import os
import subprocess

from RedStakeGUI.constants import DATA_DIRECTORY

BASE_URL = "https://vector.express/api/v2/public/convert"


def convert_dwg_to_pdf(dwg_file, pdf_file):
    if getattr(sys, "frozen", False):
        # Running as a bundled application
        base_path = sys._MEIPASS
    else:
        # Running as a normal Python script
        base_path = os.path.dirname(__file__)

    batch_file_path = os.path.join(base_path, "dwg2pdf.bat")

    command = f"cmd.exe /c {batch_file_path} {dwg_file} {pdf_file}"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully converted {dwg_file} to {pdf_file}.")
    except subprocess.CalledProcessError:
        print("Conversion failed.")


if __name__ == "__main__":
    print(DATA_DIRECTORY)
    input_file = DATA_DIRECTORY / "test.dwg"
    output_file = DATA_DIRECTORY / "test.pdf"
    compressed_file = DATA_DIRECTORY / "test.zip"

    # convert_dwg_to_pdf(input_file, output_file)
    convert_dwg_to_pdf(input_file, output_file)
