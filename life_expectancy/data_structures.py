from dataclasses import dataclass


@dataclass
class CombinedColumn:
    """Returns the index of the combined column of the DataFrame. 
    In case this index changes, you can modify it here
    """
    index: int = 0

    def get_index_of_combined_column(self) -> int:
        """Return the index of the combined column"""
        return self.index


class RegionNotFoundError(ValueError):
    """Raised when a specified region is not found in the dataset."""
    def __init__(self, region: str, valid_regions: list):
        self.region = region
        self.valid_regions = valid_regions
        self.message = (
            f"Error: The region '{self.region}' does not exist in the data. "
            f"Valid regions include: {', '.join(self.valid_regions)}."
        )
        super().__init__(self.message)
