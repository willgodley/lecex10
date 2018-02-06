__author__ = 'Sam Carton'

import tornado.ioloop
import tornado.web
import webbrowser
import requests_oauthlib

AUTHORIZATION_BASE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_spotify_access_token(client_id, client_secret, scopes, redirect_uri, port):
	'''
	This function gets a spotify access token
	:param client_id:
	:param client_secret:
	:param scopes:
	:param redirect_uri:
	:param port:
	:return:
	'''
	authorization_url = AUTHORIZATION_BASE_URL + '?scope='+'+'.join(scopes)
	oauth= requests_oauthlib.OAuth2Session(client_id, redirect_uri= redirect_uri)
	authorization_url, state= oauth.authorization_url(authorization_url)
	webbrowser.open(authorization_url)
	code = listen_on_port(port)
	token_response = oauth.fetch_token(TOKEN_URL, code=code, client_secret=client_secret)

	access_token = token_response['access_token']
	return access_token

class CodeListener(tornado.web.RequestHandler):
	'''
	This handler listens for a GET request and then shuts down the server the first time one is recieved.
	'''
	def get(self):
		# print('Received a hit on port! Stopping the server.')
		token = self.get_argument("code", None, True)
		self.write("Access token received. Please return to the Python application")
		self.application.code = token
		tornado.ioloop.IOLoop.current().stop()


def listen_on_port(port):
	application = tornado.web.Application([
		(r"/", CodeListener),
	])
	application.code = None
	application.listen(port)
	# print('Starting to listen on port',port)
	tornado.ioloop.IOLoop.current().start()
	# print('Stopped listening on port. Returning code.')
	return application.code
