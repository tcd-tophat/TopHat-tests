from test import Test

class Playerrequest(Test):

	short_title = "Server Player Information Request"
	title = "Attempts to get information on a game from the server."

	PLAYER_ID = 1

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "players" + "/" + str(self.PLAYER_ID)+"?apikey=" + self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "name" in content and "id" in content:
			if content['id'] == self.PLAYER_ID:
				self.inform = "Player Info Received - id: "+str(content['id'])+" - name:  "+content['name']
				return True
			else:
				self._reason = "The server did not return the same game as request "+str(self.PLAYER_ID)+" != "+str(content['id'])
				return False
		elif self._status == 404:
			self._reason = "The player at the ID of "+str(self.PLAYER_ID)+" does not exist"
			return False
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False