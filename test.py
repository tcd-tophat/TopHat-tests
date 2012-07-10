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
	_requests = []
	_errors = []

	def __init__(self, args):
		self.args = args
		self.h = httplib2.Http()

	def _test(self):
		pass

	def runTest(self):
		try:
			self._requests = []
			self._errors = []

			self._setup()

			self._test()

			if len(self._requests) == 0:
				self._requests.append({"headers": self.headers, "content": self.content, "func": "_request_ok"})

			for request in self._requests:

				request["content"] = request["content"].rstrip() 

				# Legacy tests
				self._status = request["headers"].status

				if request["headers"].status >= 500:
					self._reason = "Error Code "+request["headers"].status
					self.error = "Internal Server Error"
					self._tearUp()
					return False
				else:

					ret = getattr(self, request["func"])(load(StringIO(request["content"])))
					self._tearUp()
					print request["content"]
					print ret
					return ret
		except:
			self._error = "Except occurred in processing"
			self._reason = sys.exc_info()[:2]
			self._tearUp()
			return False

	def _setup(self):
		pass

	def _tearUp(self):
		pass

	def getError(self):
		return self._error

	def getReason(self):
		return self._reason

	# Checks is succeeded
	def succeeded(self):
		return self._error is None