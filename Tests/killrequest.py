from test import Test

class Killrequest(Test):

	short_title = "Server Kill Information Request"
	title = "Attempts to get information on a kill from the server."

	KILL_ID = 1

	def _test(self):
		(self.headers, self.content) = self.h.request(self.args.server + "kills" + "/" + str(self.KILL_ID) +"?apitoken=" + self._getApiToken(), "GET", '')

	def _request_ok(self, content):
		if self._status == 200 and "killer" in content:
			if content['id'] == self.KILL_ID:
				self.inform = "Kill Info Received - id: "+str(content['id'])+" - victim:  "+str(content['victim']['name'])
				return True
			else:
				self._reason = "The server did not return the same kill as request "+str(self.KILL_ID)+" != "+str(content['id'])
				return False
		elif self._status == 404:
			self._reason = "The kill at the ID of "+str(self.KILL_ID)+" does not exist"
			return False
		else:
			self._reason = "Missing JSON or Invalid Status Code."
			return False