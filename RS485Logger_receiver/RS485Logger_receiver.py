#!/usr/bin/python
import socket
import sys
import time
import os
import logging
import logging.handlers
import sys, traceback
import unicodedata
from datetime import datetime, timedelta
from ConfigParser import SafeConfigParser

###########################
# PERSONAL CONFIG FILE READ
###########################

parser = SafeConfigParser()
parser.read('RS485Logger.ini')

# Read config params
LOG_FILENAME = parser.get('config', 'log_filename')
#SERVER_IP = parser.get('config', 'server_ip')
LISTEN_PORT = parser.getint('config', 'listen_port')

REF_DATA_HEX = parser.get('config', 'reference_data_hex')
ExpectedData=[]
if (REF_DATA_HEX!=""):
	ExpectedData = [int(e.strip(),16) for e in parser.get('config', 'reference_data_hex').split(',')]

doNotCheckMessage = False
if (len(ExpectedData)==0):
	doNotCheckMessage = True

#################
#  LOGGING SETUP
#################
#logging.basicConfig()

LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
#handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)

# Handler writing to a file, rotating the file every 50MB
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=25000000, backupCount=999)
# Format each log message like this
#formatter = logging.Formatter('%(asctime)s %(message)s')
formatter = logging.Formatter("%(asctime)s %(message)s", "%d/%m %H:%M:%S")

# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
	def __init__(self, logger, level):
		"""Needs a logger and a logger level."""
		self.logger = logger
		self.level = level

	def write(self, message):
		# Only log if there is a message (not just a new line)
		if message.rstrip() != "":
			self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info('Starting RS485 logger')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_address = (SERVER_IP, LISTEN_PORT)
# Passing '' as the IP address will listen on all local IP addresses, so no need to care which broadcast address to use.
server_address = ('', LISTEN_PORT)
logger.info('starting up on %s port %s' % server_address, )
sock.bind(server_address)

try:
	while True:
		try:
			data, address = sock.recvfrom(256)
			recvList = data.split(':');
			timestamp = recvList[0]
			msgIndex = recvList[1]
			payload_as_charlist = ''.join(recvList[2:])
			payload= [ord(elem) for elem in payload_as_charlist]
			cmp_list = payload

			if (doNotCheckMessage):
				logger.info( '%s:%s:%s' % (timestamp, msgIndex, ','.join(x.encode('hex') for x in payload_as_charlist)))
			elif cmp(payload, ExpectedData) == 0:
				logger.info( '%s:%s:OK' % (timestamp,msgIndex))
			else:
				logger.info( '%s:%s:!!!!!!ERROR!!!!!!:%s' % (timestamp, msgIndex, ','.join(x.encode('hex') for x in payload_as_charlist)))
		except KeyboardInterrupt:
			raise
		except:
			logger.info("*****Exception in main loop******")
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)	
			del exc_traceback
			logger.info('LOOPING after exception in 10 seconds')
			time.sleep(10)
			pass

except KeyboardInterrupt:
	logger.info("manually interrupted")
except NameError as n:
	print("[ERROR] NameError %s" % n)
except:
	exc_type, exc_value, exc_traceback = sys.exc_info()
	traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)	
	del exc_traceback
