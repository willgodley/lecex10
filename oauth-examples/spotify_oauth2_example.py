__author__ = "Paul Resnick"
# Edited by Jackie Cohen & Sam Carton

# To find Spotify API endpoints: https://developer.spotify.com/web-api/endpoint-reference/

import requests_oauthlib
import webbrowser
import json
import spotify_data

# CONSTANTS

CLIENT_ID = spotify_data.client_id #'get this from spotify or create a secret data file, see spotify_data.py
CLIENT_SECRET = spotify_data.client_secret #'get this from spotify or create a secret data file, see spotify_data.py

AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
# NOTE: you need to specify this same REDIRECT_URI in the Spotify API console of your application!
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth' # This is a URL we have specifically set up at UMSI to handle student requests, basically -- it is an "OAuth2 workaround". You could use any URL -- but it would be a bit rude to, because that's still a hit on someone's URL! In general, you'd use your own -- on your own server.
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Set up sessions and so on to get data via OAuth2 protocol...

oauth2inst = requests_oauthlib.OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI) # Create an instance of an OAuth2Session

authorization_url, state = oauth2inst.authorization_url(AUTHORIZATION_URL) # all we need for spotify

webbrowser.open(authorization_url) # Opening auth URL for you to sign in to the Spotify service
authorization_response = input('Authenticate and then enter the full callback URL: ').strip() # Need to get the full URL in order to parse the response

# The OAuth2Session instance has a method that extracts what we need from the url, and helps do some other back and forth with spotify
token = oauth2inst.fetch_token(TOKEN_URL, authorization_response=authorization_response, client_secret=CLIENT_SECRET)
## On a web server, this would happen on your server, but we have to pull the token out so we can use it for a request inside a script we're running on a personal computer (with connection to internet)
## Anytime we want to get new data we have to do this -- so a caching system would have to take this into account any time the data expired.
## And for that -- we'd want to think about the API rate limits, primarily!

# Now we can just use the get method on the oauth2session instance from here on out to make requests to spotify endpoints. Token will work for any endpoint, as long as it's still valid. (How long it is will depend from API to API)
r = oauth2inst.get('https://api.spotify.com/v1/me')
response_diction = json.loads(r.text)
print(json.dumps(response_diction, indent=2)) # See the response printed neatly -- uncomment

###########
## Of course, this code does not have a caching setup,
## NOR does it have a set of useful functions --
## This is simply showing the process of managing an OAuth2Session.

## HOWEVER, the process here is actually simpler than ONE (not all) of the ways to address dealing with OAuth1 Protocol, though in the background, it is more in depth.

## NOTE: If not using oauth2, and you just need to extract a code from the URL, you can try something sort of like this... it is pretty ugly parsing of a URL, but it might get the job done:
# parts = authorization_response.split('?')
# query_parts = parts[1].split('&')
# code = ""
# for part in query_parts:
#     if part[:len("access_token")] == "access_token=":
#         code = part[5:]
# print(code) # or whatever you need to use it for
