__author__ = 'Sam Carton'

import pprint
import spotipy
import sam_oauth_util
import spotify_data

'''
This is a piece of code that adds a new playlist to a user's spotify account. (It does not add tracks, but the basis of this could be used to do so, with some finagling.)
It uses sam_oauth_util, which is a utility file. In order for this to work,
you will have to pip install two Python libraries (could be in a virtual environment): tornado and spotipy.

Again, this code does not employ caching -- but any caching setup would need to implement code such that all this, to make a request, would happen only if there weren't already data.

For post requests like this one -- to create a playlist -- caching doesn't necessarily make sense, because the data is saved on your spotify account!

You could consider, however, not adding a playlist if it already existed...

Program design is full of tradeoffs!
'''

client_id = spotify_data.client_id
client_secret = spotify_data.client_secret
redirect_uri = 'http://localhost:8888' # Local server URL -- must be saved in your Spotify app console -- add AND SAVE
port = 8888
scopes = ['playlist-modify-private','playlist-read-private','playlist-modify-public'] # Scopes vary dependent on the API

print("Getting access token from Spotify API...")
# For this to work, you have to have redirect_uri as a registered redirect URI for your spotify
# Also, the port has to match the last 4 numbers in the redirect URI!
access_token = sam_oauth_util.get_spotify_access_token(client_id, client_secret, scopes,redirect_uri, port)

input("Access token retrieved. Press any key and enter to continue: ")

username = input('Please enter your spotify username: ')
playlist_name = 'test_playlist_3' # For this to work,
# Must have the correct scope in the scopes variable above, whcih is being relied on above -- the access token is specific to which scopes access you are requesting from the service.

sp = spotipy.Spotify(auth=access_token)
playlists = sp.user_playlist_create(username, playlist_name)
pprint.pprint(playlists)

print("Done! Added new playlist {} to your account.".format(playlist_name))
