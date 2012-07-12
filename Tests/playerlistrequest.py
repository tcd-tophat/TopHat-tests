from test import Test

class Playerlistrequest(Test):

	short_title = "Server Player Listings Information"
	title = "Attempts to get a list of games from the server."

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "players" + "/"+"?apitoken=" + self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "players" in content:
			self.inform = "PLayers Listings Received - Amount of Available Games: "+str(len(content["players"]))
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False