from typing import Tuple, List, Dict

class UserInputHandler:
    def __init__(self, band_data: dict):
        """
        Initializes the UserInputHandler with the band data dictionary.
        """
        self.band_data = band_data

def get_band_and_songs_from_user() -> Dict[str, Dict[str, int]]:
    """
    Prompts the user to enter a band name and a comma-separated list of songs. Returns the band name and the list of songs.
    """
    band = input("Enter a band name: ")
    songs = input("Enter a comma-separated list of songs: ").split(",")
    return {band: {song.strip(): 1 for song in songs}}
