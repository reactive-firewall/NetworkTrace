# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
	from . import record_pcap
except Exception:
	import record_pcap
try:
	from . import analyze_pcap
except Exception:
	import analyze_pcap
