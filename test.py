import httplib2
from json import load
from StringIO import StringIO
import sys

class Test:

	_error = None
	_reason = None
	args = None
	inform = None
	headers = None
	content = None

	def __init__(self, args):
		self.args = args
		self.h = httplib2.Http()

	def _test(self):
		pass

	def runTest(self):
		try:
			self._test()

			self._status = self.headers.status

			self.content = self.content.rstrip() 

			if self.headers.status >= 500:
				self._reason = "Error Code "+self.headers.status
				self.error = "Internal Server Error"
				return False

			else:
				return self._request_ok(load(StringIO(self.content)))
		except:
			self._error = "Except occurred in processing"
			self._reason = sys.exc_info()[:2]

			return False

	def getError(self):
		return self._error

	def getReason(self):
		return self._reason

	# Checks is succeeded
	def succeeded(self):
		return self._error is None