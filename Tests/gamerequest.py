from test import Test

class Gamerequest(Test):

	short_title = "Server Game Information Request"
	title = "Attempts to get information on a game from the server."

	GAME_ID = 1

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "games" + "/" + str(self.GAME_ID) +"?apikey="+ self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "name" in content and "id" in content:
			if content['id'] == self.GAME_ID:
				self.inform = "Game Info Received - id: "+str(content['id'])+" - name:  "+content['name']
				return True
			else:
				self._reason = "The server did not return the same game as request "+str(self.GAME_ID)+" != "+str(content['id'])
				return False
		elif self._status == 404:
			self._reason = "The game at the ID of "+str(self.GAME_ID)+" does not exist"
			return False
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False