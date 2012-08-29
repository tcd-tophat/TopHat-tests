from test import Test

class Alive(Test):

	short_title = "Server Player Alive Information Request"
	title = "Attempts to see if a player is alive"

	PLAYER_ID = 1

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "alive" + "/" + str(self.PLAYER_ID) +"?apitoken=" + self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "alive" in content:
			self.inform = "Alive: " + str(content["alive"])
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False