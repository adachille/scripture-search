"""Module defining the DataCollector class."""

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from scripture_search.logger import get_logger


class DataCollector(ABC):
    """Class to collect data from a website."""

    save_location: Path

    def __init__(self, save_location: Path):
        self.save_location = save_location
        self.logger = get_logger(__name__)

    def get_data(self, force_refresh: bool = False) -> pd.DataFrame:
        """Collect data from the website or load from file."""
        if self.save_location.exists() and not force_refresh:
            self.logger.info("Loading data from %s", self.save_location)
            return pd.read_csv(self.save_location)

        self.logger.info(
            "Data not found at %s or force_refresh is True, collecting data...",
            self.save_location,
        )
        data = self._collect_data()
        self.logger.info("Saving data to %s", self.save_location)
        self.save_data(data)
        return data

    def save_data(self, data: pd.DataFrame) -> None:
        """Save data to a file."""
        data.to_csv(self.save_location)

    @abstractmethod
    def _collect_data(self) -> pd.DataFrame:
        """Collect data from the website."""
        raise NotImplementedError("Subclasses must implement this method.")
