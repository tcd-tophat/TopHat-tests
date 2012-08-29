from test import Test
from urllib import urlencode

class Gamecreate(Test):

	short_title = "Server Create Game Request"
	title = "Attempts to create a new game on the server"

	def _test(self):
		url = self.args.server + "games/?apitoken=" + self._getApiToken()
		data = dict(name="Joe Bush League Tournament #2")
		(headers, content) = self.h.request(url, method="POST", body=urlencode(data), headers={'Content-type': 'application/x-www-form-urlencoded'})
		print headers
		print content
		self.headers = headers
		self.content = content	

	def _request_ok(self, content):
		if self._status == 201 and "alive" in content:
			self.inform = "The game was created successfully"
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False