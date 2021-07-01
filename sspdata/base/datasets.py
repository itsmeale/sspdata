from dataclasses import dataclass


@dataclass
class BaseDataset:
    name: str
    min_year: int
    max_year: int
    event_target: str

    def is_valid_date(self, year, month):
        month_between_1_and_12 = 1 <= month <= 12
        year_between_allowed_range = self.min_year <= year <= self.max_year
        return year_between_allowed_range and month_between_1_and_12
