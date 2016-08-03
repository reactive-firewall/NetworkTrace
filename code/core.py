#! /usr/bin/env python -c
# -*- coding: utf-8 -*-

import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import helpers

def parseArgs():
	parser = argparse.ArgumentParser(description='Process some public online blacklists.')
	parser.add_argument('--dry-run', default=False, action='store_true', help='only show what would be done')
	parser.add_argument('--config', default='/etc/fetch_blacklist.cfg', help='where is the config file')
	parser.add_argument('--tmp-dir', default=False, action='store_true', help='where should temp files go')
	parser.add_argument('--hosts-deny', default=False, action='store_true', help='generate a host.deny file from the ip list')
	parser.add_argument('--snort-deny', default=False, action='store_true', help='enable snort blacklist ip reputation file')
	parser.add_argument('--nginx-deny', default=False, action='store_true', help='enable EXPERIMENTAL nginx blacklist ip file')
	parser.add_argument('--splunk-deny', default=False, action='store_true', help='enable splunk blacklist ip file')
	parser.add_argument('--iptables-deny', default=False, action='store_true', help='enable a list of iptables blacklist rules')
	parser.add_argument('--iptables-blacklist', default='/etc/blacklist.rules', help='iptables-save style list of iptables blacklist rules')
	parser.add_argument('--snort-blacklist', default='/etc/snort/rules/black_list.rules', help='where to put the snort blacklist ip reputation file')
	parser.add_argument('--display', default=False, action='store_true', help='just print the ip list')
	args = parser.parse_args()
	return args	

def readFile(somefile):
	import os
	read_data = None
	theReadPath = str(somefile)
	with open(theReadPath, 'r') as f:
		read_data = f.read()
	f.close()
	return read_data

def writeFile(somefile, somedata):
	import os
	theWritePath = str(somefile)
	try:
		with open(theWritePath, 'r+') as f:
			read_data = f.write(somedata)
		f.close()
	except:
		try:
			f.close()
		except:
			return False
		return False
	return True

def appendFile(somefile, somedata):
	import os
	theWritePath = str(somefile)
	try:
		with open(theWritePath, 'a') as f:
			f.write(somedata)
			f.write('\n')
		f.close()
	except:
		try:
			f.close()
		except:
			return False
		return False
	return True

def getBlackList(someURL, outFile):
	import urllib
	tempfile = urllib.FancyURLopener()
	tempfile.retrieve(someURL, outFile)
	return True

# TODO MOVE THIS TO A PY LIB
def extractRegexPattern(theInput_Str, theInputPattern):
	import re
	sourceStr = str(theInput_Str)
	prog = re.compile(theInputPattern)
	theList = prog.findall(sourceStr)
	return theList

def extractIPv4Addr(theInputStr):
	return extractRegexPattern(theInputStr, "(?:(?:[[:print:]]*){0,1}(?P<IP>(?:(?:[0-9]{1,3}[\.]{1}){3}(?:[0-9]{1,3}){1}){1})+(?:[[:print:]]*){0,1})+")

def extractMacAddr(theInputStr):
	return extractRegexPattern(theInputStr, "(?:(?:[[:print:]]*){0,1}(?P<Mac>(?:(?:[0-9a-fA-F]{1,2}[\:]{1}){5}(?:[0-9a-fA-F]{1,2}){1}){1})+(?:[[:print:]]*){0,1})+")

def extractConfigItem(someSection='URL Sources', theInputKey=None, thePath='/etc/fetch_blacklist.cfg'):
	import ConfigParser
	config = ConfigParser.ConfigParser()
	try:
		config.read(thePath)
		return config.get(someSection, theInputKey)
	except:
		return None
	return None

def extractConfigBool(someSection='Options', theInputKey=None, thePath='/etc/fetch_blacklist.cfg'):
	import ConfigParser
	config = ConfigParser.ConfigParser()
	try:
		config.read(thePath)
		return config.getbloolean(someSection, theInputKey)
	except:
		return False
	return False

def hasConfigItem(someSection='Options', theInputKey=None, thePath='/etc/fetch_blacklist.cfg'):
	import ConfigParser
	config = ConfigParser.ConfigParser()
	try:
		config.read(thePath)
		return config.has_option(someSection, theInputKey)
	except:
		return False
	return False

def extractBlackList(someSourceFile):
	tempfiledata = readFile(someSourceFile)
	return extractIPv4Addr(tempfiledata)

def handleBlackListURL(someURL, temp_dir):
	import os
	cachefile = os.path.join(temp_dir, "blacklist_download.tmp")
	getBlackList(someURL, cachefile)
	return extractBlackList(cachefile)

def compactList(list, intern_func=None):
   if intern_func is None:
	   def intern_func(x): return x
   seen = {}
   result = []
   for item in list:
	   marker = intern_func(item)
	   if marker in seen: continue
	   seen[marker] = 1
	   result.append(item)
   return result

def printFlatIPBlacklistFile(manyIP):
	for ip in manyIP:
		print str(ip)
	return None

def writeFlatIPBlacklistFile(manyIP, denyFile):
	first_text = False
	for ip in manyIP:
		if first_text is False:
			writeFile(denyFile, str(ip))
			first_text = True
		else:
			appendFile(denyFile, str(ip))
	return None

def generateIPDenyHostEntry(someIP, someService='ALL'):
	theResult = str(someService)
	theResult += str(': ')
	theResult += someIP
	return theResult

def printIPDenyHostEntry(someIP, someService='ALL'):
	print generateIPDenyHostEntry(someIP, someService)
	return None

def generateIPDenyHostFile(manyIP):
	manyEntry = [generateIPDenyHostEntry(ip) for ip in manyIP]
	return manyEntry
	
def printIPDenyHostFile(manyIP, someService='ALL'):
	for ip in manyIP:
		print generateIPDenyHostEntry(ip, someService)
	return None

def writeIPDenyHostFile(manyIP, someService='ALL', denyFile='/etc/hosts.deny'):
	for ip in manyIP:
		appendFile(denyFile, generateIPDenyHostEntry(ip, someService))
	return None

def printSnortIPBlacklistFile(manyIP):
	for ip in manyIP:
		print str(ip)
	return None

def writeSnortIPBlacklistFile(manyIP, denyFile='/etc/snort/rules/black_list.rules'):
	first_text = False
	for ip in manyIP:
		if first_text is False:
			writeFile(denyFile, str(ip))
			first_text = True
		else:
			appendFile(denyFile, str(ip))
	return None

def generateIPDenyNginxEntryLine(someIP):
	theResult += str('deny ')
	theResult += someIP
	theResult += str(';\n')
	return theResult


def generateIPDenyNginxEntry(someIP, someLocation='/'):
	theResult = str("location ")
	theResult += str(someLocation)
	theResult += str('{\n\tdeny ')
	theResult += someIP
	theResult += str(';\n} ')
	return theResult

def printIPDenyNginxEntry(someIP, someLocation='/'):
	print generateIPDenyNginxEntry(someIP, someLocation)
	return None

# EXPERIMENTAL
def printNginxIPBlacklistFile(manyIP, someLocation='/'):
	theNginxResult = str("location ")
	theNginxResult += str(someLocation)
	theNginxResult += str('{\n')
	for ip in manyIP:
		theNginxResult += generateIPDenyNginxEntryLine(ip)
	theNginxResult += str('\n} ')
	print theNginxResult
	return None

# EXPERIMENTAL
def writeNginxIPBlacklistFile(manyIP, someLocation='/', denyFile='/etc/nginx/conf/raw_blacklist.conf'):
	theNginxResult = str("location ")
	theNginxResult += str(someLocation)
	theNginxResult += str('{\n')
	for ip in manyIP:
		theNginxResult += generateIPDenyNginxEntryLine(ip)
	theNginxResult += str('\n} ')
	writeFile(denyFile, str(theNginxResult))
	return None

# iptables
def generateIPTablesDenyEntry(someIP, someChain='INPUT', someTarget='DROP'):
	theResult = str('-A ')
	theResult += str(someChain)
	theResult += str(' -s ')
	theResult += str(someIP)
	theResult += str(' -j ')
	theResult += str(someTarget)
	return theResult

def printIPTablesDenyEntry(someIP, someChain='INPUT', someTarget='DROP'):
	print generateIPTablesDenyEntry(someIP, someChain, someTarget)
	return None

def generateIPTablesDenyFile(manyIP):
	manyEntry = [generateIPTablesDenyEntry(ip) for ip in manyIP]
	return manyEntry

def printIPTablesDenyFile(manyIP, someChain='INPUT', someTarget='DROP', printHeaders=False):
	if printHeaders:
		print '*filter\n'
		print ':'
		print str(someChain)
		print ' - [0:0]'
	for ip in manyIP:
		print generateIPTablesDenyEntry(ip, someChain, someTarget)
	if printHeaders:
		print 'COMMIT'
		print ''
	return None

def writeIPTablesDenyFile(manyIP, denyFile='/etc/blacklist.rules', someChain='INPUT', someTarget="DROP", printHeaders=False):
	first_text = False
	if printHeaders:
		appendFile(denyFile, '*filter\n:')
		appendFile(denyFile, str(someChain))
		appendFile(denyFile, ' - [0:0]')
		first_text = True
		for ip in manyIP:
			if first_text is False:
				writeFile(denyFile, generateIPTablesDenyEntry(ip, someChain, SomeTarget))
				first_text = True
			else:
				appendFile(denyFile, generateIPTablesDenyEntry(ip, someChain, SomeTarget))
		if printHeaders:
			appendFile(denyFile, 'COMMIT')
			print ''
		return None

def printEximIPBlacklistFile(manyIP):
	for ip in manyIP:
		print str(ip)
	return None

def writeEximIPBlacklistFile(manyIP, denyFile='/etc/exim4/local_host_blacklist'):
	first_text = False
	for ip in manyIP:
		if first_text is False:
			writeFile(denyFile, str(ip))
			first_text = True
		else:
			appendFile(denyFile, str(ip))
	return None

def main():
	args = parse_my_args()

	if args.dry_run is True:
		print str("dry run")

	if args.config is not None:
		tmp_dir="/tmp/"
		temp_url_list = extractConfigItem('URL Sources', 'urls', args.config).split(",")

		if hasConfigItem('Options', 'hosts_deny_enabled', args.config) is True:
			active_hosts_deny = extractConfigBool('Options', 'hosts_deny_enabled', args.config)
		else:
			active_hosts_deny = args.hosts_deny

		if hasConfigItem('Options', 'snort_deny_enabled', args.config) is True:
			active_snort_deny = extractConfigBool('Options', 'snort_deny_enabled', args.config)
		else:
			active_snort_deny = args.snort_deny

		if hasConfigItem('Options', 'nginx_deny_enabled', args.config) is True:
			active_nginx_deny = extractConfigBool('Options', 'nginx_deny_enabled', args.config)
		else:
			active_nginx_deny = args.nginx_deny

		if hasConfigItem('Options', 'iptables_deny_enabled', args.config) is True:
			active_iptables_deny = extractConfigBool('Options', 'iptables_deny_enabled', args.config)
			if hasConfigItem('Options', 'iptables_deny_file', args.config) is True:
				active_iptables_file = extractConfigBool('Options', 'iptables_deny_file', args.config)
			else:
				active_iptables_file = args.iptables_blacklist
		else:
			active_iptables_deny = args.iptables_deny

		temp_list = None
		for nURL in temp_url_list:
			print "now on "
			print "URL ", nURL
			if temp_list is None:
				temp_list = handleBlackListURL(nURL, tmp_dir)
			else:
				temp_list += handleBlackListURL(nURL, tmp_dir)
			temp_list = helpers.compress_ip_list_to_cidr(compactList(temp_list))
		if args.display is True:
			if active_hosts_deny is True:
				print '#'
				print '# /etc/hosts.deny file'
				print '#'
				printIPDenyHostFile(temp_list, 'ALL')
				print ''
			if active_snort_deny is True:
				print '#'
				print '# snort blacklist file'
				print '#'
				printSnortIPBlacklistFile(temp_list)
				print ''
			if active_nginx_deny is True:
				print '#'
				print '# nginx blacklist file'
				print '#'
				printNginxIPBlacklistFile(temp_list)
				print ''
			if active_iptables_deny is True:
				print '#'
				print '# nginx blacklist file'
				print '#'
				printIPTablesDenyFile(temp_list)
				print ''
		if args.dry_run is False:
			if active_hosts_deny is True:
				writeIPDenyHostFile(temp_list, 'ALL', '/etc/hosts.deny')
			if active_snort_deny is True:
				writeSnortIPBlacklistFile(temp_list, args.snort_blacklist)
			if active_nginx_deny is True:
				writeNginxIPBlacklistFile(temp_list, args.nginx_blacklist)
			if active_iptables_deny is True:
				writeIPTablesDenyFile(temp_list, active_iptables_file)
			print temp_list
	else:
		print str("nothing to do")

	exit(0)
