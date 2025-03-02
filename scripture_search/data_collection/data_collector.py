"""Module defining the DataCollector class."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from scripture_search.logger import get_logger

import pandas as pd


class DataCollector(ABC):
    """Class to collect data from a website."""

    save_location: Path

    def __init__(self, save_location: Path):
        self.save_location = save_location
        self.logger = get_logger(__name__)

    def get_data(self, force_refresh: bool = False) -> pd.DataFrame:
        """Collect data from the website or load from file."""
        if self.save_location.exists() and not force_refresh:
            self.logger.info(f"Loading data from {self.save_location}")
            return pd.read_csv(self.save_location)

        self.logger.info(f"Data not found at {self.save_location} or force_refresh is True, collecting data...")
        data = self._collect_data()
        self.logger.info(f"Saving data to {self.save_location}")
        self.save_data(data)
        return data

    def save_data(self, data: pd.DataFrame) -> None:
        """Save data to a file."""
        data.to_csv(self.save_location)

    @abstractmethod
    def _collect_data(self) -> pd.DataFrame:
        """Collect data from the website."""
        raise NotImplementedError("Subclasses must implement this method.")

   
