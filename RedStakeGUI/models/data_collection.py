from ..constants import PARCEL_DATA_MAP, PARCEL_DATA_COUNTIES
import ttkbootstrap as ttk
from src.county_data_collectors.base_collector import BaseParcelDataCollector


class DataCollector:
    def __init__(self):
        self.county = None
        self.parcel_id = None
        self.county_data_collector = self.get_county_data_collector()

    def get_county_data_collector(self) -> BaseParcelDataCollector:
        """This method will return the specific data collector class for
        the county specified in the County dropdown menu.

        Returns:
            BaseParcelDataCollector: The data collector class for the
                county specified in the County dropdown menu.
                BaseParcelDataCollector is an abstract base class.
        """
        parcel_id = self.inputs["Parcel ID"].get().strip()
        county = self.inputs["County"].get().strip()

        if parcel_id == "" and county == "":
            self.update_info_label(3)
            return
        if parcel_id == "":
            self.update_info_label(2)
            return
        if county == "":
            self.update_info_label(1)
            return
        if county not in PARCEL_DATA_COUNTIES:
            self.update_info_label(11, county=county)
            return

        self.update_info_label(9, parcel_id=parcel_id)
        return PARCEL_DATA_MAP[county]
