# LandSurveyWorkflowSuite

This repository contains a Python-based suite designed to automate and streamline various tasks in land surveying. The suite offers multiple functionalities such as database management, quoting, and AutoCAD file handling.

## Overview

The aim of this project is to provide an all-in-one Python interface for land surveying operations, benefiting land surveyors and support staff. The suite features multiple tabs, each catering to specific needs:

1. **Close-Job Finder**: Utilizes `close_job_search.py` to perform fuzzy searches in a Microsoft Access database.
2. **File Entry**: Powered by `file_entry.py`, this allows direct entries into the database.
3. **Intake Sheet**: Uses `intake_sheet.py` to generate and email quotes.
4. **Website Search**: Facilitated by `website_search.py`, it automates property-related web searches.
5. **AutoCAD File Opener**: `cad_opener.py` and `dwg_file_opener.py` facilitate the search and opening of AutoCAD files.

The suite leverages various helper modules like `data_collection.py`, `encryption_manager.py`, and `settings_manager.py` to provide a seamless user experience.

## Usage

To utilize the suite, follow these steps:

1. **Clone the repository and navigate to its root directory.**

    ``` bash
    git clone https://github.com/pdiegel/LandSurveyWorkflowSuite.git
    cd LandSurveyWorkflowSuite
    ```

2. **Install the necessary dependencies.**

    ``` bash
    pip install -r requirements.txt
    ```

3. **Run the main script.**

    ``` bash
    python -m RedStakeGUI.main
    ```

Detailed usage for each tab can be found in their respective Python files.

## Contributing

Contributions are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. For more details, refer to the `LICENSE.md` file.

## Contact

For inquiries or issues, please contact <philipdiegel@gmail.com>.
