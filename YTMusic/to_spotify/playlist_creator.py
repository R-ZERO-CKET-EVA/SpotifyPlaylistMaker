import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List
from config_loader import ConfigLoader
from logger import Logger
import re

scope = "playlist-modify-public playlist-modify-private"

class PlaylistCreator:
    def __init__(self, config_file: str):
        """
        Initializes the PlaylistCreator with the configuration file path.
        """
        self.client_id = ConfigLoader(config_file).get_client_id()
        self.client_secret = ConfigLoader(config_file).get_client_secret()
        self.playlist_title = ConfigLoader(config_file).get_playlist_title()
        self.redirect_uri = ConfigLoader(config_file).get_redirect_uri()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, scope=scope, redirect_uri=self.redirect_uri))

    def create_playlist(self, band_name: str = None) -> str:
        """
        Creates a new playlist on Spotify and returns the playlist ID.
        If a band_name is provided, it's used as the playlist name, otherwise, the playlist title from the config is used.
        """
        playlist_name = band_name if band_name else self.playlist_title
        playlist = self.sp.user_playlist_create(user=self.sp.current_user()["id"], name=playlist_name, public=True)
        return playlist["id"]

    def add_song_to_playlist(self, playlist_id: str, song_uri: str) -> bool:
        """
        Adds a song to the playlist using its Spotify URI. Returns True if successful, False otherwise.
        """
        try:
            self.sp.user_playlist_add_tracks(user=self.sp.current_user()["id"], playlist_id=playlist_id, tracks=[song_uri])
            return True
        except Exception as e:
            Logger("error.log").log_error(str(e))
            return False

    def search_song_uri(self, artist: str, track: str) -> str:
        """
        Searches for a song's Spotify URI based on the artist and track name.
        Displays the top 10 results, prompts the user to select a song,
        and returns the selected song's URI. 
        The user can also choose to skip the track.
        """
        try:
            # Remove the "(feat. ...)" part from the track title
            track_cleaned = re.sub(r' \(feat\..*\)', '', track)
            
            # First, search using artist and track
            results = self.sp.search(q=f"artist:{artist} track:{track_cleaned}", type="track", limit=10)
            tracks = results["tracks"]["items"]
            
            # If no tracks were found, search again using just the track
            if not tracks:
                results = self.sp.search(q=track_cleaned, type="track", limit=10)
                tracks = results["tracks"]["items"]

            # If still no tracks found, return None
            if not tracks:
                print("No tracks found!")
                return None
            
            # If the first result matches the artist and title perfectly, auto-select it
            if tracks[0]['artists'][0]['name'].lower() == artist.lower() and tracks[0]['name'].lower() == track_cleaned .lower():
                print(f"Automatically added {artist} - {track_cleaned} to the playlist.")
                return tracks[0]["uri"]
            
            # Display the searched artist and track
            print(f"Searching for: {artist} - {track_cleaned}\n")
            
            # Display the top 10 results
            for idx, track_item in enumerate(tracks, 1):
                print(f"{idx}. {track_item['artists'][0]['name']} - {track_item['name']} ({track_item['album']['name']})")
            
            print("\n" + "-" * 50 + "\n")  # Visual separator
            
            # Prompt the user to select a song or skip
            while True:
                choice = input("Select a song (1-10) or type 's' to skip: ")
                
                if choice.isdigit() and 1 <= int(choice) <= 10:
                    selected_track = tracks[int(choice) - 1]
                    return selected_track["uri"]
                elif choice.lower() in ['s', 'skip']:
                    print("Skipping track...")
                    return None
                else:
                    print("Invalid choice. Please select a number between 1 and 10 or type 's' to skip.")
        
        except Exception as e:
            Logger("error.log").log_error(str(e))
            return None


    def handle_rate_limit(self) -> None:
        """
        Handles rate limit by waiting for the appropriate time before making the next request.
        """
        time.sleep(0.5)  # Wait for 0.5 seconds before making the next request
