#! /usr/bin/env python

def parseargs():
	"""Parse the arguments"""
	import argparse
	parser = argparse.ArgumentParser(description='Records Network activity in a pcap file', epilog='Usually used to record a network trace (pcap) file.')
	parser.add_argument('-o', '--out', dest='output_file', required=True, help='The output file to save.')
	parser.add_argument('-i', '--interface', default=None, help='The interface to use (usualy en0 or eth0)')
	end_action = parser.add_mutually_exclusive_group(required=True)
	end_action.add_argument('-c', '-n', '--count', dest='output_count', default=None, help='The count of packets to save.')
	end_action.add_argument('-t', '--timeout', default=3600, dest='output_time', help='timeout in seconds.')
	data_action = parser.add_mutually_exclusive_group()
	data_action.add_argument('-e', '-p', '--everything', default=True, action='store_true', dest='whore_mode', help='Promiscuous data recording. This is probably what you want for better record. Gather anything on the network, mine and yours and others too. This is default. Overrides --self.')
	data_action.add_argument('--self', action='store_false', dest='whore_mode', help='Bare minimum data recording. Use this if in doubt about what is recorded. Overrides --everything')
	theResult = parser.parse_args()
	return theResult

def get_username():
	"""get the current user name"""
	import os
	import pwd
	return pwd.getpwuid( os.getuid() )[0]

def recordPCAPFile(theFilePath, theRecordMode, count=100, interface=None):
	"""record a network capture in the given file"""
	import base64
	import os
	import subprocess
	theResult=None
	if theFilePath is None:
		theFilePath=str("/tmp/pcap_content_SWAP.pcap")
	user_name = str(get_username())
	tail_cmd = str("ip or not ip")
	if theRecordMode is True:
		if interface is not None:
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-c", str(count), "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-p", "-i", str(interface), tail_cmd])
			except Exception:
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
		else:
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-c", str(count), "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-p", tail_cmd])
			except Exception:
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
	else:
		if interface is not None:
			interface_cmd = str("-i "+str(interface))
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-c", str(count), "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-i", str(interface), tail_cmd])
			except Exception as err:
				print(str(err.args[0]))
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
		else:
			try:
				theResult = subprocess.check_output(["tcpdump", "-K", "-Z", str(user_name), "-f", "-c", str(count), "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", tail_cmd])
			except Exception as err:
				print(str(err.args[0]))
				theResult = "an error occured while reading the pcap file, check the path and try sudo"
	return theResult

class Command(object):
	def __init__(self):
		self.process = None
	
	def run(self, theFilePath, theRecordMode, timeout, interface=None):
		import base64
		import os
		import subprocess
		import threading
		theResult=None
		if theFilePath is None:
			theFilePath=str("/tmp/pcap_content_SWAP.pcap")
		user_name = str(get_username())
		tail_cmd = str("ip or not ip")
		process = None
		if theRecordMode is True:
			if interface is not None:
				try:
					def target():
						print(str("Trace Thread started"))
						self.process = subprocess.Popen(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-p", "-i", str(interface), tail_cmd])
						self.process.communicate()
						print(str("Trace Thread finished"))
				except Exception:
					theResult = "an error occured while reading the pcap file, check the path and try sudo"
			else:
				try:
					def target():
						print(str("Trace Thread started"))
						self.process = subprocess.Popen(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", "-p", tail_cmd])
						self.process.communicate()
						print(str("Trace Thread finished"))
				except Exception:
					theResult = "an error occured while reading the pcap file, check the path and try sudo"
		else:
			if interface is not None:
				interface_cmd = str("-i "+str(interface))
				try:
					def target():
						print(str("Trace Thread started"))
						self.process = subprocess.Popen(["tcpdump", "-K", "-Z", str(user_name), "-f", "-i", str(interface), "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", tail_cmd])
						self.process.communicate()
						print(str("Trace Thread finished"))
				except Exception as err:
					print(str(err.args[0]))
					theResult = "an error occured while reading the pcap file, check the path and try sudo"
			else:
				try:
					def target():
						print(str("Trace Thread started"))
						self.process = subprocess.Popen(["tcpdump", "-K", "-Z", str(user_name), "-f", "-n", "-S", "-U", "-w", str(theFilePath), "-vvv", tail_cmd])
						self.process.communicate()
						print(str("Trace Thread finished"))
				except Exception as err:
					print(str(err.args[0]))
					theResult = "an error occured while reading the pcap file, check the path and try sudo"	

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			print(str("Terminating process"))
			self.process.terminate()
			thread.join()
		print(str(self.process.returncode))


if __name__ == '__main__':
	args = parseargs()
	try:
		interface = args.interface
		output_file = args.output_file
		count = args.output_count
		timelimit = int(args.output_time)
		whore_mode = args.whore_mode
		if (output_file is None):
			print(str("record_pcap: grumble....grumble: OUTPUT_FILE is set to None! Nothing to save. Nothing to do."))
			exit(3)
		if output_file is not None:
			if interface is None:
				if count is None:
					cmd = Command()
					cmd.run(output_file, whore_mode, timelimit)
				else:
					recordPCAPFile(output_file, whore_mode, count)
			else:
				if count is None:
					cmd = Command()
					cmd.run(output_file, whore_mode, timelimit, interface)
				else:
					recordPCAPFile(output_file, whore_mode, count, interface)
	except Exception as main_err:
		print(str("record_pcap: REALLY BAD ERROR: ACTION will not be compleated! ABORT!"))
		print(str(main_err.args[0]))
		exit(5)
	exit(0)
