import json
import os
from ytmusicapi import YTMusic

def get_user_playlists():
    ytmusic = YTMusic('oauth.json')  # Make sure this path points to your OAuth credentials
    playlists = ytmusic.get_library_playlists(limit=None)  # Fetch all playlists
    
    for index, playlist in enumerate(playlists, 1):
        print(f"{index}. {playlist['title']}")
    
    return playlists


def sanitize_folder_name(name):
    """
    Remove characters that are forbidden in Windows directory names.
    """
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in forbidden_chars:
        name = name.replace(char, '')
    return name

def get_playlist_contents(playlist_id):
    ytmusic = YTMusic('oauth.json')
    tracks = ytmusic.get_playlist(playlist_id, limit=None)['tracks']

    songs = []
    skipped_songs = []

    for track in tracks:
        if track['artists'] and track['artists'][0]['name']:  # Check if the artist is not None
            song = {
                'artist': track['artists'][0]['name'],
                'song_title': track['title']
            }
            songs.append(song)
        else:
            # Append just the song title to skipped songs if artist is None
            skipped_songs.append(track['title'])

    return songs, skipped_songs

def main():
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

            print(f"\nContents saved to {filename} and skipped songs saved to {skipped_filename}")
        else:
            print(f"\nContents saved to {filename}")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()