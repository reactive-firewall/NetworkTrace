#! /usr/bin/env python

def parseargs():
	""""parse the arguments"""
	import argparse
	parser = argparse.ArgumentParser(description='Decodes the content of a pcap file', epilog="Usually used to extract the file data from the a network trace (pcap) file. Remember last option wins.")
	parser.add_argument('-o', '--out', dest='output_file', required=True, help='The output file to save.')
	parser.add_argument('-i', '--interface', default=None, help='The interface to use (usualy en0 or eth0)')
	data_action = parser.add_mutually_exclusive_group()
	data_action.add_argument('-e', '-p', '--everything', default=True, action='store_true', dest='whore_mode', help='Promiscuous data recording. This is probably what you want for better record. Gather anything on the network, mine and yours and others too. This is default. Overrides --self.')
	data_action.add_argument('--self', action='store_false', dest='whore_mode', help='Bare minimum data recording. Use this if in doubt about what is recorded. Overrides --everything')
	return parser.parse_args()

def get_username():
	""""get the current user name"""
	import os
	import pwd
	return pwd.getpwuid( os.getuid() )[ 0 ]

#def writeFile(somefile, somedata):
#	import os
#	if somefile is None:
#		return False
#	elif somedata is None:
#		return False
#	theWritePath = str(somefile)
#	try:
#		with open(theWritePath, 'w') as f:
#			read_data = f.write(somedata)
#		f.close()
#	except Exception:
#		try:
#			f.close()
#		except Exception:
#			return False
#		return False
#	return True

def recordPCAPFile(theFilePath, theRecordMode, interface=None):
	""""record a network capture in the given file"""
	import base64
	import os
	import subprocess
	if theFilePath is None:
		theFilePath=str("/tmp/pcap_content_*SWAP.pcap")
	user_name = str(get_username())
	tail_cmd = str("ip or not ip")
	if theRecordMode is True:
		if interface is not None:
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-p", "-i", str(interface), tail_cmd])
			except Exception:
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
		else:
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-p", tail_cmd])
			except Exception:
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
	else:
		if interface is not None:
			interface_cmd = str("-i "+str(interface))
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-i", str(interface), tail_cmd])
			except Exception:
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
		else:
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", tail_cmd])
			except Exception:
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
	return theResult

# just data mode not implemented (why drop the headers?)
#def readPCAPFileData(theFilePath):
#	import base64
#	import os
#	import subprocess
#	if theFilePath is None:
#		theFilePath=str("/tmp/pcap_content_*SWAP.pcap")
#	try:
#		p1 = subprocess.Popen(["tcpdump", "-K", "-Z", str(get_username()), "-n", "-S", "-l", "-r", str(theFilePath), "-XX", "ip or not ip"], stdout=subprocess.PIPE)
#		p2 = subprocess.Popen(["fgrep", "0x"], stdin=p1.stdout, stdout=subprocess.PIPE)
#		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
#		theResult = p2.communicate()[0]
#	except Exception:
#		theResult = "an error occured while reading the pcap file, check the path and try sudo"
#	return theResult

if __name__ == '__main__':
	args = parseargs()
	try:
		interface = args.interface
		output_file = args.output_file
		whore_mode = args.whore_mode
		if (output_file is None):
			print(str("record_pcap: grumble....grumble: OUTPUT_FILE is set to None! Nothing to save. Nothing to do."))
			exit(3)
		if output_file is not None:
			if interface is None:
				recordPCAPFile(output_file, whore_mode)
			else:
				recordPCAPFile(output_file, whore_mode, interface)
	except Exception:
		print(str("record_pcap: REALLY BAD ERROR: ACTION will not be compleated! ABORT!"))
		exit(5)
	exit(0)
