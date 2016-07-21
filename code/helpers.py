#! /usr/bin/env python -c
# I know, kluge like a burning bus >.<
# http://xkcd.com/1695/

# IP string conversion 00000000000000000000000000000000 <-> 0.0.0.0

DEFAULT_IPV4="0.0.0.0"
DEFAULT_IP="00000000000000000000000000000000"
CIDR_LEN_VALUES = [2147483648, 1073741824, 536870912, 268435456, 134217728, 67108864, 33554432, 16777216, 8388608, 4194304, 2097152, 1048576, 524288, 262144, 131072, 65536, 32768, 16384, 8192, 4096, 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]

print CIDR_LEN_VALUES

def IPv4_to_IP(someIPv4=DEFAULT_IPV4):
	temp_num = ""
	for octet in str(someIPv4).split("."):
		temp_num +="{0:08b}".format(int(octet))
	return temp_num

def IP_to_IPv4(someIP="00000000000000000000000000000000"):
	theResult = str(int(someIP[0:8], 2))+"."+str(int(someIP[8:16], 2))+"."+str(int(someIP[16:24], 2))+"."+str(int(someIP[24:32], 2))
	return theResult

# IP int conversion 0 <-> 00000000000000000000000000000000b <-> 0.0.0.0

def int_to_IP(someInt="0"):
	theResult = str("{0:032}".format(int( "{0:032b}".format(int(someInt)), 10)))
	return theResult

def int_to_IPv4(someInt="0"):
	return IP_to_IPv4( int_to_IP(someInt) )

def IPv4_to_int(someIP=DEFAULT_IPV4):
	temp_num = ""
	if someIP is None:
		the_result = None
	else:
		for octet in someIP.split("."):
			temp_num +="{0:08b}".format(int(octet))
		the_result = int(temp_num, 2)
	return the_result

def IP_to_int(someIP="00000000000000000000000000000000"):
	theResult = int(someIP, 2)
	return theResult

# array conversions [00000000000000000000000000000000] <-> [0.0.0.0]

def IPv4s_to_IPs(someIPs=[DEFAULT_IPV4]):
	the_list = [IPv4_to_IP(someIP) for someIP in someIPs]
	return the_list

def IPs_to_IPv4s(someIPs=["00000000000000000000000000000000"]):
	the_list = [IP_to_IPv4(someIP) for someIP in someIPs]
	return the_list

def IPv4s_to_ints(someIPs=[DEFAULT_IPV4]):
	the_list = [IPv4_to_int(someIP) for someIP in someIPs]
	return the_list

def IPs_to_ints(someIPs=["00000000000000000000000000000000"]):
	the_list = [IP_to_int(someIP) for someIP in someIPs]
	return the_list

def ints_to_IPs(someInts=["0"]):
	the_list = [int_to_IP(someInt) for someInt in someInts]
	return the_list

def ints_to_IPv4s(someInts=["0"]):
	the_list = [int_to_IPv4(someInt) for someInt in someInts]
	return the_list

# useful utilities to find subnets and CIDR approximations

def Extract_Runs(someArray, gap=1):
	run = []
	result = [run]
	next_item = None
	for item in someArray:
		if (item == next_item) or (next_item is None):
			run.append(item)
		else:
			run = [item]
			result.append(run)
		next_item = item + gap
	return result

def chunk_array_to_size(unchunked_array, chunk_size):
	if chunk_size is None:
		chunk_size=1
	chunked_array = [unchunked_array[i:i+chunk_size] for i in range(0,len(unchunked_array),chunk_size)]
	return chunked_array

def chunk_IP_array_to_subnets(unchunked_ip_array):
	lastSize = None
	for i in CIDR_LEN_VALUES:
		if lastSize is None:
			lastSize = i
			continue 
		if (len(unchunked_ip_array) >= lastSize) is False:
			lastSize = i
			if (len(unchunked_ip_array) >= i):
				chunked_array = chunk_array_to_size(unchunked_ip_array, i)
	return chunked_array

def Extract_IPv4_Runs(someIPv4Array, gap=1):
	result_ints = Extract_Runs(IPv4s_to_ints(someIPv4Array), gap)
	the_result_IPv4_runs = [ints_to_IPv4s(someInt) for someInt in result_ints]
	the_result = [chunk_IP_array_to_subnets(some_subnet) for some_subnet in the_result_IPv4_runs]
	x = []
	for somenet in the_result:
		for somehost in somenet:
			x.append(somehost)
	return x

def get_IP_bit(someIP="00000000000000000000000000000000", some_bit=0):
	theResult = str( int(someIP[0:some_bit], 2) )
	return theResult

def get_IPv4_bit(someIPv4=DEFAULT_IPV4, some_bit=0):
	theResult = get_IP_bit( IPv4_to_IP(someIPv4), some_bit )
	return theResult


def IP_to_CIDR(someIP="00000000000000000000000000000000", some_mask_bit=0):
	theResult = str(someIP)
	if some_mask_bit is not 32:
		theResult = str( someIP[0:int(some_mask_bit)] ) + "{0:032b}".format(int(0))[int(some_mask_bit):32]
	return str( IP_to_IPv4(theResult)+"/"+str(some_mask_bit) )

def IPv4_to_CIDR(someIP=DEFAULT_IPV4, some_mask_bit=0):
	theResult = IP_to_CIDR(IPv4_to_IP(someIP), some_mask_bit)
	return theResult

def no_op():
	return None

def IPRange_to_CIDR(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
	match_bit = 32
	for somebit in range(1, 32):
		if IPv4_to_CIDR(startIPv4, int(somebit)) == IPv4_to_CIDR(endIPv4, int(somebit)):
			match_bit = somebit
	subnet = IPv4_to_CIDR(startIPv4, match_bit)
	return subnet

def IPRange_to_valid_CIDR(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
	match_bit = 32
	for somebit in range(1, 32):
		if IPv4_to_CIDR(startIPv4, int(somebit)) == IPv4_to_CIDR(endIPv4, int(somebit)):
			if int(IPv4_to_int(endIPv4) - IPv4_to_int(startIPv4)) == pow(2, (32 - int(somebit))):
				match_bit = somebit
	subnet = IPv4_to_CIDR(startIPv4, match_bit)
	return subnet

def IPRange_to_best_mask(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
	match_bit = 32
	for somebit in range(1, 32):
		if IPv4_to_CIDR(startIPv4, int(somebit)) == IPv4_to_CIDR(endIPv4, int(somebit)):
			if int(IPv4_to_int(endIPv4) - IPv4_to_int(startIPv4)) == pow(2, (32 - int(somebit))):
				match_bit = somebit
	return match_bit

def IPRange_to_mask(startIPv4=DEFAULT_IPV4, endIPv4=DEFAULT_IPV4):
	match_bit = 32
	for somebit in range(1, 32):
		if IPv4_to_CIDR(startIPv4, int(somebit)) == IPv4_to_CIDR(endIPv4, int(somebit)):
			match_bit = somebit
	return match_bit

def getNetAddrforIPv4(startIPv4=DEFAULT_IPV4, net_mask_bit=32):
	theResult = IPv4_to_CIDR(startIPv4, int(net_mask_bit))
	offset = -1 - len(str(net_mask_bit))
	return theResult[0:offset]

def compress_ip_list_to_cidr(someIPList=[DEFAULT_IPV4]):
	temp_list = Extract_IPv4_Runs(someIPList)
	theResult = None
	for somelist in temp_list:
		someResult = None
		if (somelist is None or somelist is []) is False:
			someResult = IPv4_to_CIDR(somelist[0], IPRange_to_mask(somelist[0], somelist[-1]))
			if someResult is None:
				someResult = [IPv4_to_CIDR(someItem, 32) for someItem in somelist]
			if theResult is None:
				theResult = [someResult]
			else:
				theResult.append(someResult)
	return theResult

# not implemented
def getBcastAddrforIPv4():
	no_op()
	return False

#test function DO NOT USE
def TEST_IP_UTIL_PY_DEBUG():
	print IPRange_to_mask("1.2.3.0", "1.2.3.6")
	the_IP=IPv4_to_IP("1.2.2.249")
	print(the_IP)
	print(IP_to_IPv4(the_IP))
	for mask in range(0, 32):
		print "/" + str(mask+1)
		print(getNetAddrforIPv4(IP_to_IPv4(the_IP), mask+1))
	
	test_list = ["1.2.3.1", "1.2.3.2", "1.2.3.3", "1.2.3.4", "1.2.3.5", "1.2.3.6", "5.6.7.8", "8.7.6.5", "1.2.2.250", "41.2.2.251", "1.2.2.252", "1.2.2.253", "1.2.2.254" , "1.2.2.255"]
	print Extract_IPv4_Runs(test_list)
	print compress_ip_list_to_cidr(test_list)
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
