#! /usr/bin/env python

def parseargs():
	""""parse the arguments"""
	import argparse

	parser = argparse.ArgumentParser(description='Decodes the content of a pcap file', epilog="Usually used to extract the file data from the a network trace (pcap) file. Remember last option wins.")
	parser.add_argument('-i', '--in', dest='input_file', required=True, help='The pcap file to read')
	parser.add_argument('-o', '--out', dest='output_file', required=False, help='The output file to save.')
	data_action = parser.add_mutually_exclusive_group()
	data_action.add_argument('--hex', default=False, action='store_true', dest='hex_mode', help='Output Hex Dump. Overrides --data')
	data_action.add_argument('--data', action='store_false', dest='hex_mode', help='Output data. This is probably what you want. Overrides --hex')
	return parser.parse_args()

def get_username():
	""""get the current user name"""
	import os
	import pwd
	return pwd.getpwuid( os.getuid() )[ 0 ]

def writeFile(somefile, somedata):
	""""write the somedata to the somefile"""
	import os
	if somefile is None:
		return False
	elif somedata is None:
		return False
	theWritePath = str(somefile)
	try:
		with open(theWritePath, 'w') as f:
			read_data = f.write(somedata)
		f.close()
	except Exception:
		try:
			f.close()
		except Exception:
			return False
		return False
	return True

def readPCAPFile(theFilePath):
	""""read the pcap file theFilePath"""
	import base64
	import os
	import subprocess
	if theFilePath is None:
		theFilePath=str("/tmp/pcap_content_*SWAP.pcap")
	user_name = str(get_username())
	try:
		theResult = subprocess.check_output(["tcpdump", "-K", "-Z", user_name, "-n", "-S", "-l", "-r", str(theFilePath), "-vvv", "-A", "-XX", "ip or not ip"])
	except Exception:
		theResult = "an error occured while reading the pcap file, check the path and try sudo"
	return theResult

def readPCAPFileHEX(theFilePath):
	""""read the pcap file theFilePath in hex"""
	import base64
	import os
	import subprocess
	if theFilePath is None:
		theFilePath=str("/tmp/pcap_content_*SWAP.pcap")
	user_name = str(get_username())
	try:
		p1 = subprocess.Popen(["tcpdump", "-K", "-Z", user_name, "-n", "-S", "-l", "-r", str(theFilePath), "-xx", "ip or not ip"], stdout=subprocess.PIPE)
		p2 = subprocess.Popen(["fgrep", "0x"], stdin=p1.stdout, stdout=subprocess.PIPE)
		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
		theResult = p2.communicate()[0]
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
#		p1 = subprocess.Popen(["tcpdump", "-K", "-Z", str(os.getusername()), "-n", "-S", "-l", "-r", str(theFilePath), "-XX", "ip or not ip"], stdout=subprocess.PIPE)
#		p2 = subprocess.Popen(["fgrep", "0x"], stdin=p1.stdout, stdout=subprocess.PIPE)
#		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
#		theResult = p2.communicate()[0]
#	except Exception:
#		theResult = "an error occured while reading the pcap file, check the path and try sudo"
#	return theResult

if __name__ == '__main__':
	args = parseargs()
	try:
		input_file = args.input_file
		output_file = args.output_file
		hex_mode = args.hex_mode
		if (input_file is None):
			print(str("decode_pcap: grumble....grumble: INPUT_FILE is set to None! Nothing to do."))
			exit(3)
		#	if (output_file is None) and (hex_mode is False):
		#		print(str("decode_pcap: grumble....grumble: OUTPUT_FILE is set to None! OUTPUT_MODE is data. Nothing will be saved!"))
		if input_file is not None:
			theData = None
			if hex_mode is not True:
				theData = readPCAPFile(input_file)
			else:
				theData = readPCAPFileHEX(input_file)

			if output_file is None:
				print(str(theData))
			else:
				writeFile(str(output_file), theData)
	except Exception:
		print(str("decode_pcap: REALLY BAD ERROR: ACTION will not be compleated! ABORT!"))
		exit(5)
	exit(0)
