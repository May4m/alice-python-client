from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
import urllib


def start_alice():
	def _success(req, response):
		Logger.info("Alice engine successfuly started")
	UrlRequest('http://alice-foundery-experimental.herokuapp.com/alice/restart', _success)


def alice_request(query, on_success):
	query = urllib.urlencode({'question': query})
	url = 'http://alice-foundery-experimental.herokuapp.com/alice/ask?' + query
	req = UrlRequest(url, on_success)