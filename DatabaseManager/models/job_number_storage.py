import datetime
from DatabaseManager.models.access_database import AccessDB


class JobNumberStorage:
    def __init__(self, database: AccessDB):
        self.database = database
        self.now = datetime.datetime.now()
        self.year = self.now.year % 100
        self.month = self.now.month

    def get_job_number_prefix(self, num_previous_months: int = 0) -> str:
        month = self.month
        if num_previous_months > 0 and month > 1:
            month -= num_previous_months
            if month < 1:
                month += 12

        job_number_prefix = f"{self.year:02d}{month:02d}"
        return job_number_prefix

    @property
    def unused_job_number(self) -> str:
        num_previous_months = 0
        while num_previous_months < 12:
            prefix = self.get_job_number_prefix(num_previous_months)
            job_numbers = [
                number
                for number in self.get_current_year_job_numbers()
                if number.startswith(prefix)
            ]
            if len(job_numbers) == 0:
                num_previous_months += 1
            else:
                highest_existing_fn = max(job_numbers)
                last_four_digits = str(int(highest_existing_fn[4:8]) + 1).zfill(
                    4
                )
                new_fn = self.get_job_number_prefix() + last_four_digits
                break
        else:
            new_fn = self.get_job_number_prefix() + "0100"

        return new_fn

    @property
    def current_year_job_numbers(self) -> set[str]:
        current_year_jobs = self.database.execute_generic_query(
            f"SELECT [Job Number] FROM [Existing Jobs] WHERE [Job Number] LIKE\
 '{self.year}%'"
        )
        job_numbers = [job_number[0] for job_number in current_year_jobs]
        return set(job_numbers)

    @property
    def existing_job_numbers(self) -> set[str]:
        existing_jobs = self.database.execute_generic_query(
            "SELECT [Job Number] FROM [Existing Jobs]"
        )
        job_numbers = [job_number[0] for job_number in existing_jobs]
        return set(job_numbers)

    @property
    def active_job_numbers(self) -> set[str]:
        active_jobs = self.database.execute_generic_query(
            "SELECT [Job Number] FROM [Active Jobs]"
        )
        job_numbers = [job_number[0] for job_number in active_jobs]
        return set(job_numbers)

    def add_job_number(self, job_number: str):
        self.existing_job_numbers.add(job_number)
        self.active_job_numbers.add(job_number)

    def remove_job_number(self, job_number: str):
        self.existing_job_numbers.remove(job_number)

    def add_existing_job_numbers(self, job_numbers: tuple):
        # Pulling from access database as a tuple, with job number being
        # the first element.
        job_numbers = [job_number[0] for job_number in job_numbers]
        self.existing_job_numbers.update(job_numbers)

    def add_active_job_numbers(self, job_numbers: tuple):
        # Pulling from access database as a tuple, with job number being
        # the first element.
        job_numbers = [job_number[0] for job_number in job_numbers]
        self.active_job_numbers.update(job_numbers)

    def add_current_year_job_numbers(self, job_numbers: tuple):
        # Pulling from access database as a tuple, with job number being
        # the first element.
        job_numbers = [job_number[0] for job_number in job_numbers]
        self.current_year_job_numbers.update(job_numbers)

    def clear_job_numbers(self):
        self.existing_job_numbers.clear()
        self.active_job_numbers.clear()

    def get_existing_job_numbers(self) -> list[str]:
        return self.existing_job_numbers

    def get_active_job_numbers(self) -> list[str]:
        return self.active_job_numbers

    def get_current_year_job_numbers(self) -> list[str]:
        return self.current_year_job_numbers

    def add_unused_job_number(self, job_number: str):
        self.unused_job_number = job_number
