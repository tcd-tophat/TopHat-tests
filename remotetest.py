import httplib2
import argparse
import sys

"""
remotetest

	Script for remote testing for the TopHat server.

"""


__author__ = "Ian Connolly (ian@tophat.ie, connolim@tcd.ie)"
__license__ = "MIT"
__version__ = "0.0.1"

# Login, API token, Create/Delete user, Create/Delete game, Time requests for user data, game data etc. 
# Try to break server... Bad HTTP, bad JSON

parser = argparse.ArgumentParser(description="Test suite for TopHat server")
parser.add_argument("-s",  "--server", help="MANDATORY: Server on  which TopHat platform is running on", dest="server")
parser.add_argument("-u", "--user", help="Provide username to login with", dest="user")
parser.add_argument("-p", "--password", help="Provide password to login with", dest="password")
args  = parser.parse_args()


def main ():

	if args.server is None: 
		print "You must supply a server to test\n"
		sys.exit(-1)


	# Hello world test
	#h = httplib2.Http(disable_ssl_certificate_validation=True) # Commented out cos lol
	h = httplib2.Http(".cache") 
	(resp_headers, content) = h.request(args.server, "GET")
	print str(resp_headers) + str(content)
		






if __name__ == '__main__':
	main()