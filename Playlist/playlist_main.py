import argparse
import time
import datetime
import json

from playlist_creator import PlaylistCreator
from band_data_loader import BandDataLoader
from logger import Logger
from config_loader import ConfigLoader
from user_input_handler import UserInputHandler

def main():
    parser = argparse.ArgumentParser(description='Create Spotify playlists.')
    parser.add_argument('--singleband', action='store_true', help='Create individual playlists for each band.')
    args = parser.parse_args()

    # Read band data from the dictionary of JSON objects
    band_data =   {}
    with open("band_data.json", "r") as file:
            if file == None or file == {}:
                band_data = UserInputHandler.get_band_and_songs_from_user()
                print(band_data)
            else:
                band_data = json.load(file)

    # Create an instance of PlaylistCreator with the configuration file
    playlist_creator = PlaylistCreator("config.json")

    # Create a playlist on Spotify using the playlist title from the configuration file
    playlist_id = playlist_creator.create_playlist()

    # Iterate through the band data and add the songs to the playlist using their Spotify URIs
    for band_name in BandDataLoader(band_data).get_band_names():
        songs = BandDataLoader(band_data).get_songs_for_band(band_name)
        if args.singleband:
            single_band_playlist_id = playlist_creator.create_playlist(band_name)  # Creating a separate playlist for this band
            for song in songs:
                song_uri = playlist_creator.search_song_uri(band_name, song)
                if song_uri:
                    playlist_creator.add_song_to_playlist(single_band_playlist_id, song_uri)
                    playlist_creator.handle_rate_limit()
                else:
                    Logger("error.log").log_error(f"Song not found: {band_name} - {song}")

        for song in songs:
            artist = band_name
            track = song
            song_uri = playlist_creator.search_song_uri(artist, track)
            if song_uri:
                playlist_creator.add_song_to_playlist(playlist_id, song_uri)
                playlist_creator.handle_rate_limit()
            else:
                Logger("error.log").log_error(f"Song not found: {artist} - {track}")

    # Rest of the code remains the same

if __name__ == "__main__":
    main()
