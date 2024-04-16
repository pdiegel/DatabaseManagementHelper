# DatabaseManagementHelper

This repository contains a Python-based suite designed to automate and streamline various tasks in database management. The suite offers multiple functionalities such as data entry, query management, and file handling automation.

## Overview

The aim of this project is to provide an all-in-one Python interface for database operations, benefiting database administrators and users who handle significant amounts of data. The suite features multiple tabs, each catering to specific database management needs:

1. **Query Executor**: Utilizes `close_job_search.py` to perform fuzzy searches within a Microsoft Access database.
2. **Data Entry**: Powered by `file_entry.py`, this allows direct data entries into the database.
3. **Report Generator**: Uses `intake_sheet.py` to generate reports and send them via email.
4. **Data Search**: Facilitated by `website_search.py`, it automates searches for data across various websites.
5. **File Management**: `cad_opener.py` and `dwg_file_opener.py` facilitate the management and opening of various file types.

The suite leverages various helper modules like `data_collection.py`, `encryption_manager.py`, and `settings_manager.py` to provide a seamless user experience.

## Usage

To utilize the suite, follow these steps:

1. **Clone the repository and navigate to its root directory.**

    ``` bash
    git clone https://github.com/pdiegel/DatabaseManagementHelper.git
    cd DatabaseManagementHelper
    ```

2. **Install the necessary dependencies.**

    ``` bash
    pip install -r requirements.txt
    ```

3. **Run the main script.**

    ``` bash
    python -m DatabaseManager.main
    ```

Detailed usage for each tab can be found in their respective Python files.

## Contributing

Contributions are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. For more details, refer to the `LICENSE.md` file.

## Contact

For inquiries or issues, please contact <philipdiegel@gmail.com>.
