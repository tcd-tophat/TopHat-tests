import os
import httplib2
import argparse
import sys
from colorama import init
from termcolor import colored
from StringIO import StringIO
import re as regex
import json
from json import load
import timeit
import thread
from threading import Thread
import time
import pprint

"""
remotetest

	Script for remote testing for the TopHat server.

"""
__author__ = "Ian Connolly (ian@tophat.ie, connolim@tcd.ie) and Kevin Bluett (kevin@tophat.ie, bluettk@tcd.ie)"
__license__ = "MIT"
__version__ = "0.0.1"

# Login, API token, Create/Delete user, Create/Delete game, Time requests for user data, game data etc. 
# Try to break server... Bad HTTP, bad JSON
SANITY_URL = "http://www.google.com/ "

init()
parser = argparse.ArgumentParser(description="Test suite for TopHat server")
parser.add_argument("-s",  "--server", help="MANDATORY: Server on  which TopHat platform is running on", dest="server")
parser.add_argument("-u", "--user", help="Provide username to login with", dest="user", default="testuser")
parser.add_argument("-p", "--password", help="Provide password to login with", dest="password", default="test")
parser.add_argument("-n", "--number", help="Number of times to run tests", dest="number", default="1")
parser.add_argument("--noverify", help="Turn off SSL validation", action="store_true")
parser.add_argument("-t", "--testpath", help="Provide path from root of test request, defaults to jsontest/",  default="jsontest/", dest="testpath")
parser.add_argument("-j", "--json", help="Provide sample json data for Hello, World test. Defaults to platform default", default='\r{"glossary": {"title": "example glossary","GlossDiv": {"title": "S","GlossList": {"GlossEntry": {"ID": "SGML","SortAs": "SGML","GlossTerm": "Standard Generalized Markup Language","Acronym": "SGML","Abbrev": "ISO 8879:1986","GlossDef": {"para": "A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso": ["GML", "XML"]},"GlossSee": "markup"}}}}}\n', dest="test_json")
parser.add_argument("-q", "--quiet", help="Hide print messages", default=False, dest="quiet")
parser.add_argument("-th", "--threads", help="Number of threads to run", default=1, dest="threads")
args  = parser.parse_args()

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

def main():
	testcount = 0
	successful = 0
	failed = 0


	for test in tests:
		testcount += 1
		testclass = import_run_test(test)

		print "----------"

		if not args.quiet:
			print "TEST " + colored(testcount, "blue") + ": "  + "Attempting '"+testclass.short_title+"' test..."

		if testclass.runTest():
			if not args.quiet:
				print "TEST " + colored(testcount, "blue") + ": "  + colored("Successful", "green")

			if testclass.inform is not None:
				if not args.quiet:
					print "\tInfo Message: " + colored(testclass.inform, "yellow")	
			successful += 1
		else:
			if not args.quiet:
				print"TEST " + colored(testcount, "blue") + ": " + colored("Failed", "red")
				print "\tREASON: " + colored(testclass.getReason(), "red")
			if testclass.headers is not None:
				if not args.quiet:
					print "\tStatus Code: " + colored(testclass.headers.status, "yellow")	
			if testclass.content is not None:
				if not args.quiet:
					print "\tReturned JSON: " + colored(testclass.content, "yellow")
			failed += 1

	if not args.quiet:
		print "\n\n === TESTS COMPLETE ===\n"
		print "Tests ran: " + colored(testcount, "blue")
		print "Successful: " + colored(successful, "green")
		print  "Failed: " + colored(failed, "red")

def get_tests():

	mods = list()

	for root, dirs, files in os.walk('./Tests/'):
		for name in files:       
			filename = os.path.join(root, name)

			if not ".pyc" in filename:
				filename = filename.replace("./Tests/", "")
				filename = filename.replace(".py", "")

				if filename != "__init__" and filename != ".DS_Store":
					mods.append(str(filename))

	return mods

def import_run_test(test):
	mod = import_item('Tests.%s' % test.lower())

	return getattr(mod, test.title())(args)


def import_item(name):
    """Import and return bar given the string foo.bar."""

    package = '.'.join(name.split('.')[0:-1])
    obj = name.split('.')[-1]

    if package:
        module = __import__(package,fromlist=[obj])
        try:
            pak = module.__dict__[obj]
        except KeyError:
            raise ImportError('No module named %s' % obj)
        return pak
    else:
        return __import__(obj)


def thready():
	t = timeit.Timer("main()","from __main__ import main")
	print "Time for test:"  + str(t.timeit(int(args.number)))

if __name__ == '__main__':
	tests = get_tests()

	threads = []

	for x in range(0,int(args.threads)):
		print "Starting Thread "+str(x)
		t = Thread(None,thready,None)
        t.start()
        threads.append(t)
	while 1:
		for t in threads:
			if not t.isAlive():
				threads.remove(t)

		if len(threads) == 0:
			exit()

		time.sleep(1000)
