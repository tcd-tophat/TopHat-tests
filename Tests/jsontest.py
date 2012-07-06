from test import Test

class Jsontest(Test):

	short_title = "JsonTest"
	title = "Tries to call the sample test method on the server"

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "jsontest", "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "message" in content:
			if content["message"] == "Test Call completed successfully":
				return True
			else:
				return False
		else:
			self._reason = "Missing JSON or Invalid Status Code"
			return False