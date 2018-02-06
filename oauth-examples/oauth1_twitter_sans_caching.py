import requests_oauthlib
import webbrowser
import json
import secrets # need properly formatted file, see example
from datetime import datetime

CLIENT_KEY = secrets.client_key # what Twitter calls Consumer Key
CLIENT_SECRET = secrets.client_secret # What Twitter calls Consumer Secret

### Twitter-specific OAuth URLs
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
BASE_AUTH_URL = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

def get_tokens( client_key=CLIENT_KEY,
                client_secret=CLIENT_SECRET,
                request_token_url=REQUEST_TOKEN_URL,
                base_authorization_url=BASE_AUTH_URL,
                access_token_url=ACCESS_TOKEN_URL,verifier_auto=True):


    oauth_inst = requests_oauthlib.OAuth1Session(client_key,client_secret=client_secret)

    fetch_response = oauth_inst.fetch_request_token(request_token_url)

    # Using the dictionary .get method in these lines
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    auth_url = oauth_inst.authorization_url(base_authorization_url)

    # Open the auth url in browser:
    # For user to interact with & approve access of this app -- i.e., this script
    webbrowser.open(auth_url)

    # Deal with required input, which will vary by API
    if verifier_auto: # if the input is default (True), like Twitter
        verifier = input("Please input the verifier:  ")
    else:
        redirect_result = input("Paste the full redirect URL here:  ")
        # returns a dictionary -- you may want to inspect that this works and edit accordingly
        oauth_resp = oauth_inst.parse_authorization_response(redirect_result)
        verifier = oauth_resp.get('oauth_verifier')

    # Regenerate instance of oauth1session class with more data
    oauth_inst = requests_oauthlib.OAuth1Session(client_key,
                    client_secret=client_secret,
                    resource_owner_key=resource_owner_key,
                    resource_owner_secret=resource_owner_secret,
                    verifier=verifier)

    oauth_tokens = oauth_inst.fetch_access_token(access_token_url) # returns a dictionary

    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return client_key, client_secret, resource_owner_key, resource_owner_secret, verifier

def get_data_from_api(request_url,service_ident, params_diction, expire_in_days=7):

    client_key, client_secret, resource_owner_key, resource_owner_secret, verifier =  \
        get_tokens(service_ident)

    # Create a new instance of oauth to make a request with
    oauth_inst = requests_oauthlib.OAuth1Session(client_key,
        client_secret=client_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret)

    # Call the get method on oauth instance
    # Work of encoding and "signing" the request happens behind the sences, thanks to the OAuth1Session instance in oauth_inst
    resp = oauth_inst.get(request_url,params=params_diction)
    data_str = resp.text
    data = json.loads(data_str)
    return data


if __name__ == "__main__":

    # Invoke functions
    twitter_search_baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    twitter_search_params = {'q':"University of Michigan", "count":4}

    twitter_result = get_data_from_api(twitter_search_baseurl,"Twitter",twitter_search_params) # Default expire_in_days
    print(twitter_result)
