from test import Test

class Version(Test):

	short_title = "Server Version"
	title = "Tries to get the version of the server from the server"

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "version" + "/", "GET", '{ "os":"android", "version":"2.3.5","appversion":"0.1"}')

	def _request_ok(self, content):
		if self._status == 200 and "version" in content:
			self.inform = "Server is at version: "+content['version']
			return True
		else:
			self._reason = "Missing JSON or Invalid Status Code"
			return False