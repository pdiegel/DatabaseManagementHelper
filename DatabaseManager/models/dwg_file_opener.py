"""This module contains the DWGFiles class, which handles all the file
 information of a specified DWG File."""
import os
import time
import subprocess


class DWGFiles:
    """Handles search and path functions in regards to DWG files."""

    file_number_length = 8
    dwg_path = os.path.join(r"\\server", "dwg")

    def __init__(self, file_number: str) -> None:
        self.file_number = file_number
        if not self.verify_file_number():
            return
        self.year = self.file_number[:2]
        self.month = self.get_month()
        self.file_directory = self.get_file_directory()
        self.short_file_number = self.get_short_file_number()
        self.file_list = self.get_file_list()
        self.file_dict = self.get_file_dict()
        self.newest_file = self.get_newest_file()

    def verify_file_number(self) -> bool:
        """Returns True if the specified file number is valid.
        Returns False if invalid."""
        if len(self.file_number) == DWGFiles.file_number_length:
            return True
        else:
            raise ValueError("Invalid Job Number")

    def get_month(self) -> str:
        """Returns the month of a given file number."""
        month = self.file_number[2:4]

        if 99 > int(self.year) > 90:
            if int(month) < 10:
                month = self.file_number[3]
        return month

    def get_first_four(self) -> str:
        """Returns the first four numbers of a given file number."""
        first_four = f"{self.year}{self.month}"
        return first_four

    def get_short_file_number(self) -> str:
        """Returns a shortened version of a file number, based on
        historical file handling."""
        first_four = self.get_first_four()
        short_file_number = f"{first_four}{self.file_number[5:8]}"
        return short_file_number

    def get_file_directory(self) -> os.path:
        """Returns a file's directory."""
        return os.path.join(DWGFiles.dwg_path, f"{self.year}dwg", self.month)

    def get_file_name(self, file_path: os.path) -> str:
        """Returns the file name of a given file path, as a string."""
        # fn_index = file_path.index(self.file_number)
        try:
            fn_index = file_path.index(self.file_number)
        except ValueError:
            fn_index = file_path.index(self.short_file_number)

        if fn_index:
            file_name = file_path[fn_index:]
            return file_name

    def get_file_list(self) -> list:
        """Returns a list of dwg file paths based on the provided file
        number."""
        file_list = []
        for directory, _, files in os.walk(self.file_directory, topdown=True):
            for file in files:
                is_dwg_file = file.lower().endswith(".dwg")
                if not is_dwg_file:
                    continue
                current_file_path = os.path.join(directory, file)
                if file.startswith((self.file_number, self.short_file_number)):
                    file_list.append(current_file_path)

        if file_list:
            return file_list

    def get_file_dict(self) -> dict:
        """Returns a dictionary containing the file name as the key,
        with the file date and file directory as values."""
        file_list = self.get_file_list()
        file_dict = {}
        for file_path in file_list:
            file_date = self.get_file_date(file_path)
            file_name = self.get_file_name(file_path)
            file_directory = file_path.split(file_name)[0]
            file_dict[file_name] = [file_date, file_directory]
        return file_dict

    def get_newest_file(self) -> os.path:
        """Returns the path of the most recently modified dwg file."""
        newest_creation_time = 0
        newest_file = ""
        for file in self.file_list:
            file_creation_time = os.path.getmtime(file)
            if file_creation_time > newest_creation_time:
                newest_creation_time = file_creation_time
                newest_file = file

        return newest_file

    def get_file_date(self, file_path: os.path) -> str:
        """Returns a formatted file date of the latest file
        modification, given the file path."""
        file_date = os.path.getmtime(file_path)
        local_file_date = time.localtime(file_date)
        formatted_file_date = time.strftime("%m/%d/%Y, %I%p", local_file_date)
        file_hour = formatted_file_date[-4:-2]
        if int(file_hour) < 10:
            formatted_file_date = (
                formatted_file_date[:12] + formatted_file_date[13:]
            )
        return formatted_file_date

    def get_file_path(self, file_name: str) -> os.path:
        """Returns the file path of a given file name."""
        file_path = self.file_dict[file_name][1]
        return file_path

    def open_dwg_with_powershell(
        self, file_path: os.path, file_name: str
    ) -> None:
        """Runs the windows powershell commands to change directory, and
        open the given DWG file."""

        # Start a new PowerShell process
        powershell = subprocess.Popen(
            ["powershell.exe", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
        )

        # Run multiple PowerShell commands
        powershell.stdin.write(f"cd {file_path}\n")
        powershell.stdin.write(f'.\\"{file_name}"\n')
        powershell.stdin.write("Exit\n")

    def open_file(self, file) -> None:
        """Opens a DWG file using windows powershell,
        given the file number."""
        if not file:
            return "Error"
        file_name = file.split(" | ")[0]
        file_path = self.get_file_path(file_name)

        self.open_dwg_with_powershell(file_path, file_name)

    def sort_dwg_files(self, dwg_files: list) -> list:
        """Returns a sorted list of DWG files. the list of files must be
        in this format: ['21080360.dwg | 00/00/2023, 0PM']"""
        sorted_files = []
        for file in dwg_files:
            file_name, date = file.split(" | ")
            year = int(date.split(",")[0][-4:])
            month = int(date.split(",")[0][:2])
            day = int(date.split(",")[0][3:5])
            sorted_files.append((day, month, year, file))

        # Sort by day, month and year in descending order
        for i in range(3):
            sorted_files.sort(key=lambda tup: tup[i], reverse=True)

        return sorted_files
