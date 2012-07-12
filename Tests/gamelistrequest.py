from test import Test
from json import load
from StringIO import StringIO

class Gamelistrequest(Test):

	short_title = "Server Game Listings Information"
	title = "Attempts to get a list of games from the server."

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "games" + "/?apitoken=" + self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "games" in content:
			self.inform = "Game Listings Received - Amount of Available Games: "+str(len(content["games"]))
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False