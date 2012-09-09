from test import Test
from urllib import urlencode

class Playercreate(Test):

	short_title = "Create Player Request"
	title = "Attempts to create a new player on the server"

	def _test(self):
		url = self.args.server + "players/?apitoken=" + self._getApiToken()
		dict_ = {}
		dict_["data"] = "{\"name\":\"Player MAN!\", \"game\": {\"id\":1}, \"qrcode\":\"R45454\"}"
		data = urlencode(dict_)
		(headers, content) = self.h.request(url, method="POST", body=data, headers={'Content-type': 'application/x-www-form-urlencoded'})
		self.headers = headers
		self.content = content	

	def _request_ok(self, content):
		if self._status == 201 and "name" in content and "id" in content:
			self.inform = "The game was created successfully"
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False