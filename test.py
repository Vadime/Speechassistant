import os

def run():
    spotify= SpotifyClient(os.getenv("SPOTIFY_AUTH_TOKEN"))
    random_tracks = spotify_client.getRandomTracks()
    

if __name__ == '__main__':
    run()

