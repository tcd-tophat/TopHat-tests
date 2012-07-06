from test import Test

class Anonapi(Test):

	short_title = "Anonymous API Token Request"
	title = "Attempts to get an anonymous API token from the server."

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "apitokens" + "/", "POST", 'data={}', headers={'content-type':'application/x-www-form-urlencoded'})

	def _request_ok(self, content):
		if self._status == 201 and "apitoken" in content:
			self.inform = "API Token Received: "+content['apitoken']
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code"
			return False