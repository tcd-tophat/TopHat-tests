import httplib2
import argparse
import sys
from colorama import init
from termcolor import colored
from StringIO import StringIO
import re as regex
import json
from json import load

"""
remotetest

	Script for remote testing for the TopHat server.

"""
__author__ = "Ian Connolly (ian@tophat.ie, connolim@tcd.ie)"
__license__ = "MIT"
__version__ = "0.0.6"

# Login, API token, Create/Delete user, Create/Delete game, Time requests for user data, game data etc. 
# Try to break server... Bad HTTP, bad JSON
SANITY_URL = "http://www.google.com/ "

init()
parser = argparse.ArgumentParser(description="Test suite for TopHat server")
parser.add_argument("-s",  "--server", help="MANDATORY: Server on  which TopHat platform is running on", dest="server")
parser.add_argument("-u", "--user", help="Provide username to login with", dest="user", default="testuser")
parser.add_argument("-p", "--password", help="Provide password to login with", dest="password", default="test")
parser.add_argument("--noverify", help="Turn off SSL validation", action="store_true")
parser.add_argument("-t", "--testpath", help="Provide path from root of test request, defaults to jsontest/",  default="jsontest/", dest="testpath")
parser.add_argument("-j", "--json", help="Provide sample json data for Hello, World test. Defaults to platform default", default='\r{"glossary": {"title": "example glossary","GlossDiv": {"title": "S","GlossList": {"GlossEntry": {"ID": "SGML","SortAs": "SGML","GlossTerm": "Standard Generalized Markup Language","Acronym": "SGML","Abbrev": "ISO 8879:1986","GlossDef": {"para": "A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso": ["GML", "XML"]},"GlossSee": "markup"}}}}}\n', dest="test_json")
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
	print "Username: " + colored(args.user, "blue")
	print "Password: " + colored(args.password, "blue")
	print  "\n\n\n"

	h = httplib2.Http()
	try:
		(resp_headers, content) = h.request(SANITY_URL, "GET") # sanity check
	except:
		print colored("FAILED: Sanity check", "red") + ": "  + "Could not connect to " + SANITY_URL + ", check your internet connection"
		print "Closing...."
		sys.exit(-1)

	if args.noverify:
		h = httplib2.Http(disable_ssl_certificate_validation=True)
	else:
		h = httplib2.Http()

	# Hello world test
	print "TEST " + colored(testcount, "blue") + ": "  + "Attempting 'Hello, world' test..."
	try:
		(resp_headers, content) = h.request(args.server + args.testpath, "GET")	
		if content.rstrip()  in args.test_json.rstrip():
			print "TEST " + colored(testcount, "blue") + ": "  + colored("Successful", "green")
			successful += 1
		else:
			print"TEST " + colored(testcount, "blue") + ": " + colored("Failed", "red")
			print "\tREASON: " + colored("Returned JSON does not equal sample JSON", "red")
			print "\tReturned JSON: " + colored(content, "yellow")

			failed = failed + 1
	except:
		print"TEST " + colored(testcount, "blue") + ": " + colored("Failed", "red")
		print "\tREASON: " + colored(sys.exc_info()[:2], "red")
		failed = failed + 1
	
	testcount = testcount +1
	print "\nTEST " + colored(testcount, "blue") + ": " + "Attempting to get API version from server..."
	try:
		(resp_headers, content) = h.request(args.server + "version" + "/", "GET", '{ "os":"android", "version":"2.3.5","appversion":"0.1"}')
		
		if resp_headers.status == 200:
			# TO DO: How does server return API versions?

			mapped = load(StringIO(content))

			print "TEST " + colored(testcount, "blue") + ": "  + colored("Successful", "green")

			successful += 1

			if 'version' in mapped:
				print "\tServer Version: " + colored(mapped['version'], "yellow")

		elif resp_headers.status >= 400 and resp_headers.status < 500:
			print"TEST " + colored(testcount, "blue") + ": " + colored("Failed", "red")
			print "\tREASON: " + colored("Server did not understand API version request", "red")
			failed = failed + 1

		elif resp_headers.status >= 500:
			print"TEST " + colored(testcount, "blue") + ": " + colored("Failed", "red")
			print "\tREASON: " + colored("Server had encountered internal server", "red")
			failed = failed + 1
	except:
		print"TEST " + colored(testcount, "blue") + ": " + colored("Failed", "red")
		print "\tREASON: " + colored(sys.exc_info()[:2], "red")
		failed = failed + 1

	print "\n\n === TESTS COMPLETE ===\n"
	print "Tests ran: " + colored(testcount, "blue")
	print "Successful: " + colored(successful, "green")
	print  "Failed: " + colored(failed, "red")


if __name__ == '__main__':
	main()