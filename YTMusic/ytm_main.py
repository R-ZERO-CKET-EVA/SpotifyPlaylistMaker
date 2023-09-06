import json
import os
from ytmusicapi import YTMusic
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_user_playlists():
    ytmusic = YTMusic('oauth.json')  # Make sure this path points to your OAuth credentials
    playlists = ytmusic.get_library_playlists(limit=None)  # Fetch all playlists
    
    for index, playlist in enumerate(playlists, 1):
        print(f"{index}. {playlist['title']}")
    
    return playlists


## If we need the snippet info containing publishedAt (date added to playlist) we need to use google's auth
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "secrets.json"
scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    flow.redirect_uri = "https://localhost:8080"
    auth_url, __ = flow.authorization_url(prompt="consent")
    print('Please go to this URL: {}'.format(auth_url))
    code = input('Enter the authorization code: ')
    flow.fetch_token(code=code)
    youtube = build(
    api_service_name, api_version, credentials=flow.credentials)
    return youtube


def sanitize_folder_name(name):
    """
    Remove characters that are forbidden in Windows directory names.
    """
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in forbidden_chars:
        name = name.replace(char, '')
    return name

def main():
    choice = input("Do you need the dates that songs were added to the playlist? (Y/N): ")

    if choice.lower() == 'y': #the user needs dates, so we need to access yt api ourselves
        print('We will need extra Youtube Authentication to get dates')
        youtube_service = authenticate()
        print("Fetching your playlists...")
        playlists = get_user_playlists()
        choice = int(input("\nSelect the number of the playlist you'd like to get the contents of: ")) - 1
        if 0 <= choice < len(playlists):
            selected_playlist = playlists[choice]
            contents, skipped = get_yt_playlist_with_dates(youtube_service,selected_playlist['playlistId'])
            
            # Prepare the directory structure
            sanitized_folder_name = sanitize_folder_name(selected_playlist['title'])
            output_dir = os.path.join('outputs', sanitized_folder_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Write the contents to a .json file inside the specified directory
            filename = os.path.join(output_dir, f"{sanitized_folder_name}.json")
            with open(filename, 'w') as file:
                json.dump(contents, file, indent=4)

            # If there are skipped songs, write them to a .txt file
            if skipped:
                skipped_filename = os.path.join(output_dir, f"Skipped-{sanitized_folder_name}.json")
                with open(skipped_filename, 'w') as file:
                    for title in skipped:
                        json.dump(skipped, file, indent=4)

                print(f"\nContents saved to {filename} and skipped songs saved to {skipped_filename}")
            else:
                print(f"\nContents saved to {filename}")
        else:
            print("Invalid choice!")
    else: #the user does not need dates
        print("Fetching your playlists...")
        playlists = get_user_playlists()
        
        choice = int(input("\nSelect the number of the playlist you'd like to get the contents of: ")) - 1
        if 0 <= choice < len(playlists):
            selected_playlist = playlists[choice]
            contents, skipped = get_playlist_contents(selected_playlist['playlistId'])
            
            # Prepare the directory structure
            sanitized_folder_name = sanitize_folder_name(selected_playlist['title'])
            output_dir = os.path.join('outputs', sanitized_folder_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Write the contents to a .json file inside the specified directory
            filename = os.path.join(output_dir, f"{sanitized_folder_name}.json")
            with open(filename, 'w') as file:
                json.dump(contents, file, indent=4)

            # If there are skipped songs, write them to a .txt file
            if skipped:
                skipped_filename = os.path.join(output_dir, f"Skipped-{sanitized_folder_name}.txt")
                with open(skipped_filename, 'w') as file:
                    for title in skipped:
                        file.write(f"{title}\n")

                print(f"\nContents saved to {filename} and songs with no artist data saved to {skipped_filename}")
            else:
                print(f"\nContents saved to {filename}")
        else:
            print("Invalid choice!")


def get_yt_playlist_with_dates(youtube, playlist_id: str):
    # Initialize variables
    all_items = []
    page_token = None
    
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()
        for item in response.get('items', []):
            title = item['snippet']['title']
            published_at = item['snippet']['publishedAt']
            print(item)
            # Assuming artist and song title are separated by '-'
            parts = title.split(' - ')
            if len(parts) == 2:
                artist, song_title = parts
                all_items.append({
                    'videoId': item['snippet']['resourceId']['videoId'],
                    'artist': artist.strip(),
                    'song_title': song_title.strip(),
                    'publishedAt': published_at,
                    'spotifyURI': ''
                })
            else:
                all_items.append({
                    'id': item['snippet']['resourceId']['videoId'],
                    'song_title': title,
                    'publishedAt': published_at,
                    'spotifyURI': ''
                })
        
        page_token = response.get('nextPageToken')
        if not page_token:
            return all_items
def get_playlist_contents(playlist_id):
    ytmusic = YTMusic('oauth.json')
    tracks = ytmusic.get_playlist(playlist_id, limit=None)['tracks']

    songs = []
    skipped_songs = []

    for track in tracks:
        if track['artists'] and track['artists'][0]['name']:  # Check if the artist is not None
            song = {
                'artist': track['artists'][0]['name'],
                'song_title': track['title'],
                'videoId':track['videoId'],
                'uri':''
            }
            songs.append(song)
        else:
            # Append just the song title to skipped songs if artist is None
            skipped_songs.append(track['title'])

    return songs, skipped_songs


if __name__ == "__main__":
    main()