from test import Test

class Killrequestlist(Test):

	short_title = "Server Kill Listings Information"
	title = "Attempts to get a list of kills from the server."

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "kills" + "/"+"?apikey=" + self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "kills" in content:
			self.inform = "Kill Listings Received - Amount of Available Games: "+str(len(content["kills"]))
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False