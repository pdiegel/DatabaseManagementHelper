from RedStakeGUI.constants import PARCEL_DATA_MAP
from src.county_data_collectors.base_collector import BaseParcelDataCollector
import logging


class DataCollector:
    def __init__(self, parcel_id: str, county: str):
        self.parcel_id = parcel_id
        self.county = county
        self.parcel_data = self.get_parcel_data()

    def get_county_data_collector(self) -> BaseParcelDataCollector:
        """This method will return the specific data collector class for
        the county specified in the County dropdown menu.

        Returns:
            BaseParcelDataCollector: The data collector class for the
                county specified in the County dropdown menu.
                BaseParcelDataCollector is an abstract base class.
        """
        return PARCEL_DATA_MAP.get(self.county, None)

    def get_parcel_data(self) -> dict:
        """This method will return the parcel data dictionary for the
        parcel ID number entered in the Parcel ID field.

        Returns:
            dict: The parcel data dictionary for the parcel ID number
                entered in the Parcel ID field.
        """
        county_data_collector = self.get_county_data_collector()
        if county_data_collector is None:
            return

        try:
            parcel = county_data_collector(self.parcel_id)
        except IndexError as e:
            logging.error(e)
            raise e
        return parcel.parcel_data
