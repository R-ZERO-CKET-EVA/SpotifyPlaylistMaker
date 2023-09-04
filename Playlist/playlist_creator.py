import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List
from config_loader import ConfigLoader
from logger import Logger

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
        Searches for a song's Spotify URI based on the artist and track name. Returns the URI if found, None otherwise.
        """
        try:
            results = self.sp.search(q=f"artist:{artist} track:{track}", type="track", limit=1)
            if results["tracks"]["items"]:
                return results["tracks"]["items"][0]["uri"]
            else:
                return None
        except Exception as e:
            Logger("error.log").log_error(str(e))
            return None

    def handle_rate_limit(self) -> None:
        """
        Handles rate limit by waiting for the appropriate time before making the next request.
        """
        time.sleep(0.5)  # Wait for 0.5 seconds before making the next request
