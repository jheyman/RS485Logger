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

# Read path to log file
LOG_FILENAME = parser.get('config', 'log_filename')
SERVER_IP = parser.get('config', 'server_ip')
LISTEN_PORT = parser.getint('config', 'listen_port')

#################
#  LOGGING SETUP
#################
logging.basicConfig()

LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=5)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
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
server_address = (SERVER_IP, LISTEN_PORT)
logger.info('starting up on %s port %s' % server_address, )
sock.bind(server_address)

try:

	while True:
		data, address = sock.recvfrom(256)
		logger.info( '%s' % data)

except:
	logger.info("*****Exception in main loop******")
	exc_type, exc_value, exc_traceback = sys.exc_info()
	traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)	
	del exc_traceback
	logger.info('EXITING RS485 logger')
