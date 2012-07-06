from test import Test

class Gamerequest(Test):

	short_title = "Server Game Information Request"
	title = "Attempts to get information on a game from the server."

	game_id = 1

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "games" + "/" + self.game_id, "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "name" in content and "id" in content:
			if content['id'] == self.game_id:
				self.inform = "Game Info Received - id: "+str(content['id'])+" - name:  "+content['name']
				return True
			else:
				self._reason = "The server did not return the same game as request "+str(self.game_id)+" != "+str(content['id'])
				return False
		elif self._status == 404:
			self._reason = "The game at the ID of "+str(self.game_id)+" does not exist"
			return False
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False