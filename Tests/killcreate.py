from test import Test
from urllib import urlencode

class Killcreate(Test):

	short_title = "Create Kill Request"
	title = "Attempts to create a new kill on the server"

	def _test(self):
		url = self.args.server + "kills/?apitoken=" + self._getApiToken()
		dict_ = {}
		dict_["data"] = '{"killer": {"id": 1}, "victim_qrcode": "RCcEKo"}'
		data = urlencode(dict_)
		(headers, content) = self.h.request(url, method="POST", body=data, headers={'Content-type': 'application/x-www-form-urlencoded'})
		self.headers = headers
		self.content = content	

	def _request_ok(self, content):
		if self._status == 201 and "killer" in content and "id" in content:
			self.inform = "The game was created successfully"
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False