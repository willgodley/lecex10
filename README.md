For oauth-twitter.py you will need to create a secrets.py file that looks like this:

```
client_key = <your twitter consumer key>
client_secret = <your twitter consumer secret>
```

For oauth-twitter-withkeys.py you will need to add the following to secrets.py:

```
access_token = <your twitter access token>
access_token_secret = <your twitter access token secret>
```

Don't worry, the .gitignore is already set up to ignore your secrets file.

The examples in oauth-examples may require a different format and filename for your secret data. Use at your own risk.
