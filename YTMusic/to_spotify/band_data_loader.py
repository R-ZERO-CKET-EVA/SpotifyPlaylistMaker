from typing import List

class BandDataLoader:
    def __init__(self, data: dict):
        """
        Initializes the BandDataLoader with the band data dictionary.
        """
        self.data = data

    def get_band_names(self) -> List[str]:
        """
        Returns a list of band names from the band data.
        """
        return list(self.data.keys())

    def get_songs_for_band(self, band_name: str) -> List[str]:
        """
        Returns a list of songs associated with a band.
        """
        return list(self.data[band_name].keys())
