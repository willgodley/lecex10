
from requests_oauthlib import OAuth1Session
import secrets

client_key = secrets.client_key
client_secret = secrets.client_secret

# STEP 1: GET A REQUEST TOKEN
# We have to start by obtaining a 'request' token
# We will supply our client key and client secret
# ...otherwise no token -- you can't even get in the door!
#
# At this point we have provided our application's credentials
# so that we have the privelege to do more stuff, like request
# authorization for a particular user.
request_token_url = 'https://api.twitter.com/oauth/request_token'

oauth = OAuth1Session(client_key, client_secret=client_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')


# STEP 2: GET AUTHORIZATION FROM THE USER
# Now we have "request privileges." What will we do with all that power?
# We will send our user over to the service provider (Twitter, in this case)
# to log in. After they do, Twitter will generate a special URL,
# unique to this operation (THIS request for THIS user by THIS application).
# Our application can then go to that URL to get the very special
# verification token that we can use to retreive THIS user's data for use
# in THIS application
base_authorization_url = 'https://api.twitter.com/oauth/authorize'

# authorize_url = base_authorization_url + '?oauth_token='
# authorize_url = authorize_url + resource_owner_key
# print ('Please go here and authorize,', authorize_url)
# verifier = input('Please input the verifier')

authorization_url = oauth.authorization_url(base_authorization_url)
print ('Please go here and authorize,', authorization_url)
verifier = input('Paste the verification code here: ')



# STEP 3: Now we have verification from the user. It's a special code that
# will let us get an access token that we can use to get the actual data that
# we have been trying to hard to get.
# Wait, what? We still don't have access to the user's data? Nope.
# What we have now is an "opaque" token that will give us access to their data
# (remember, that we could only get this token after the user logged in and
# retreived it).
#
# Aside: when we created our API key, we asked for specific permissions.
#        For Twitter they're not that interesting--either Read or Read/Write.
#        Point is, those permissions matter--they're going to be encoded in
#        the access token we get next. We can only access the stuff our
#        application specifically asked for
#
# OK, back to work: now we need the access token so we can get some actual
# data. There is yet another URL we need to hit to get this.
access_token_url = 'https://api.twitter.com/oauth/access_token'

oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
oauth_tokens = oauth.fetch_access_token(access_token_url)

resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

print(resource_owner_key, resource_owner_secret)

# STEP 4: And here we go. Finally we can get the user's data, using the
# access token (in two parts: the token, and the secret)
# Note that we have to pass in our client key and secret (this belongs to
# our application) and the "resource owner" key and secret (this belongs
# to the user that we just logged in)
protected_url = 'https://api.twitter.com/1.1/account/settings.json'

oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
r = oauth.get(protected_url)
print (r.text)

protected_url = 'https://api.twitter.com/1.1/search/tweets.json'
params = {'q':'food'}
r = oauth.get(protected_url, params=params)
print (r.text)
