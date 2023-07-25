import spotipy
from spotipy.oauth2 import SpotifyOAuth

def initialize_spotify():
    # Authenticate with Spotify API
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        redirect_uri='http://localhost:8000',
        scope=scope
    ))
    return sp

def get_user_playlists(sp):
    # Get user's playlists
    playlists = sp.current_user_playlists()
    return playlists

def get_playlist_tracks(sp, playlist_id):
    # Get all tracks from the playlist
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    return tracks

def find_duplicate_songs(sp, playlist_id):
    playlist_tracks = get_playlist_tracks(sp, playlist_id)
    track_info_set = set()
    duplicate_tracks = []

    for track in playlist_tracks:
        track_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]  # Assuming the first artist represents the main artist

        # Create a tuple of track name and artist name and check if it's already in the set
        track_info = (track_name, artist_name)
        if track_info in track_info_set:
            duplicate_tracks.append((track_name, artist_name))
        else:
            track_info_set.add(track_info)

    return duplicate_tracks

if __name__ == "__main__":
    sp = initialize_spotify()

    playlists = get_user_playlists(sp)

    if playlists:
        print("Your playlists:")
        for idx, playlist in enumerate(playlists["items"], 1):
            print(f"{idx}. {playlist['name']} (ID: {playlist['id']})")

        playlist_choice = int(input("Select a playlist number: ")) - 1
        selected_playlist_id = playlists["items"][playlist_choice]["id"]

        duplicates = find_duplicate_songs(sp, selected_playlist_id)

        if duplicates:
            print("\nDuplicate songs found in the selected playlist:")
            for song_name, song_id in duplicates:
                print(f"Song: {song_name} (ID: {song_id})")
        else:
            print("\nNo duplicate songs found in the selected playlist.")
    else:
        print("No playlists found for the user.")
