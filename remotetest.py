import httplib2
import argparse
import sys
from colorama import init
from termcolor import colored

"""
remotetest

	Script for remote testing for the TopHat server.

"""


__author__ = "Ian Connolly (ian@tophat.ie, connolim@tcd.ie)"
__license__ = "MIT"
__version__ = "0.0.1"

# Login, API token, Create/Delete user, Create/Delete game, Time requests for user data, game data etc. 
# Try to break server... Bad HTTP, bad JSON
SANITY_URL = "http://www.google.com/ "

init()
parser = argparse.ArgumentParser(description="Test suite for TopHat server")
parser.add_argument("-s",  "--server", help="MANDATORY: Server on  which TopHat platform is running on", dest="server")
parser.add_argument("-u", "--user", help="Provide username to login with", dest="user")
parser.add_argument("-p", "--password", help="Provide password to login with", dest="password")
parser.add_argument("--noverify", help="Turn off SSL validation", action="store_true")
parser.add_argument("-t", "--testpath", help="Optionally provide path from root of test request, defaults to jsontest/",  default="jsontest/", dest="testpath")
args  = parser.parse_args()



def main ():

	testcount = 1
	successful = 0
	failed = 0
	
	if args.server is None: 
		print colored("\nYou must supply a server to test!!", "red")
		print "\nExpected server URL to be supplied"
		print "Closing....\n"
		sys.exit(-1)
	print colored("\nPARAMS:", "blue")
	print  "Server: " + colored(args.server, "blue") 
	if args.user is not None:
		print "Username: "  + colored(args.user, "blue")
	if args.password is not None:
		print "Password: "  + colored(args.password, "blue")
	print  "\n\n\n"

	h = httplib2.Http()
	try:
		(resp_headers, content) = h.request(SANITY_URL, "GET") # sanity check
	except:
		print colored("FAILED: Sanity check", "red") + ": "  + "Could not connect to " + SANITY_URL + ", check your internet connection"
		print "Closing...."
		sys.exit(-1)

	# Hello world test
	print "TEST " + colored(testcount, "blue") + ": "  + "Attempting 'Hello, world' test..."
	try:
		if args.noverify:
			h = httplib2.Http(disable_ssl_certificate_validation=True)
		else:
			h = httplib2.Http()
		(resp_headers, content) = h.request(args.server + args.testpath, "GET")
		print "TEST " + colored(testcount, "blue") + ": "  + colored("Successful", "green")
		successful = successful + 1
	except:
		print colored("FAILED", "red")
		print colored("REASON: ", "red")  + colored(sys.exc_info()[:2], "red")
		failed = failed + 1


	print "\n\n === TESTS COMPLETE ===\n"
	print "Tests ran: " + colored(testcount, "blue")
	print "Successful: " + colored(successful, "green")
	print  "Failed: " + colored(failed, "red")


if __name__ == '__main__':
	main()