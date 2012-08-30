from test import Test
from urllib import urlencode

class Gamecreate(Test):

	short_title = "Server Create Game Request"
	title = "Attempts to create a new game on the server"

	def _test(self):
		url = self.args.server + "games/?apitoken=" + self._getApiToken()
		dict_ = {}
		dict_["data"] = "{\"name\":\"Joe Bush League Tournament\"}"
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