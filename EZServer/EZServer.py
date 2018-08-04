import socket
import sys
import json
import sqlite3
from EZWifi import WifiScan
from EZGPS import GpsScan
from utilities import solveTrilat
from sympy import symbols
from scipy.optimize import fsolve
import random

MAX_CONNECTION_TYPE = 4
wifiFingerprint = "WIFI"
gpsFingerprint = "GPS"
ACK = "ACK\n"

MIN_PATH_LOSS = 1.5
MAX_PATH_LOSS = 6.0

MIN_PI0 = -50
MAX_PI0 = -1

# INDOOR_LAT_MIN = 44.427560
# INDOOR_LAT_MAX = 44.427650
# INDOOR_LONG_MIN = 26.049637
# INDOOR_LONG_MAX = 26.049747

INDOOR_LAT_MIN = 44.434731
INDOOR_LAT_MAX = 44.435256
INDOOR_LONG_MIN = 26.047094
INDOOR_LONG_MAX = 26.047993

# MIN_LATITTUDE = 44.426878
MIN_LATITTUDE = 44.434161
# MAX_LATITUDE = 44.428410
MAX_LATITUDE = 44.436100

# MIN_LONGITUDE = 26.048199
MIN_LONGITUDE = 26.045321
# MAX_LONGITUDE = 26.051075
MAX_LONGITUDE = 26.050272

LAT_DEG_TO_METERS = 111200
LONG_DEG_TO_METERS = 79990

def create_table():
	
	conn = sqlite3.connect('samples.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS wifi_samples_precis (bssId varchar(25), signalStrength integer, timestamp bigint)")
	c.execute("CREATE TABLE IF NOT EXISTS gps_samples_precis (client varchar(25), latitude double precision, longitude double precision, timestamp bigint)")
	return conn

def add_to_db(scanType, scan, conn):
	c = conn.cursor()

	if scanType == wifiFingerprint:
		for ap in scan.wifiAPList:
			c.execute("insert into wifi_samples_precis values (?, ?, ?)", [ap.bssId, ap.signal, scan.timestamp])
			conn.commit()
	else:
		c.execute("insert into gps_samples_precis values (?, ?, ?, ?)", [scan.client, scan.latitude, scan.longitude, scan.timestamp])
		conn.commit()

def computeLocation(fptype, scan):
	if fptype == gpsFingerprint:
		return scan.latitude, scan.longitude

	conn = sqlite3.connect('samples.db')
	c = conn.cursor()
	
	obsLat, obsLong = symbols('obsLat obsLong', real=True)
	eq = []
	
	for ap in scan.wifiAPList:
		knownAP = c.execute("SELECT * FROM ap_loc_precis WHERE bssId = ?", (ap.bssId,)).fetchall()
		if knownAP == None or knownAP == []:
			continue

		Pi = float(knownAP[0][1])
		loss = float(knownAP[0][2])
		Pij = float(ap.signal)
		knownLat = float(knownAP[0][3])
		knownLong = float(knownAP[0][4])
				
		d = 10 ** ((Pi - Pij) / (10 * loss))
		eq.append((LAT_DEG_TO_METERS * (knownLat - obsLat)) ** 2 + (LONG_DEG_TO_METERS * (knownLong - obsLong)) ** 2 - d ** 2)

	initialGuess = (random.uniform(MIN_LATITTUDE, MAX_LATITUDE), random.uniform(MIN_LONGITUDE, MAX_LONGITUDE), 5)
	eqLen = len(eq) - 3
	for i in xrange(eqLen):
		initialGuess = initialGuess + (5,)

	obsCoordinates = fsolve(solveTrilat, initialGuess, eq)

	x = obsCoordinates[0]
	y = obsCoordinates[1]
	if x < MIN_LATITTUDE:
		x = MIN_LATITTUDE
	if x > MAX_LATITUDE:
		x = MAX_LATITUDE
	if y < MIN_LONGITUDE:
		y = MIN_LONGITUDE
	if y > MAX_LONGITUDE:
		y = MAX_LONGITUDE

	return (x * (INDOOR_LAT_MAX - INDOOR_LAT_MIN) + MAX_LATITUDE * INDOOR_LAT_MIN - MIN_LATITTUDE * INDOOR_LAT_MAX) / (MAX_LATITUDE - MIN_LATITTUDE), (y * (INDOOR_LONG_MAX - INDOOR_LONG_MIN) + MAX_LONGITUDE * INDOOR_LONG_MIN - MIN_LONGITUDE * INDOOR_LONG_MAX) / (MAX_LONGITUDE - MIN_LONGITUDE)

HOST = '' #this is your localhost
PORT = 8888

connection_to_db = create_table()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.socket: must use to create a socket.
#socket.AF_INET: Address Format, Internet = IP Addresses.
#socket.SOCK_STREAM: two-way, connection-based byte streams.
print 'socket created'
 
#Bind socket to Host and Port
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print 'Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1]
    sys.exit()
 
print 'Socket Bind Success!'
 
 
#listen(): This method sets up and start TCP listener.
s.listen(10)
print 'Socket is now listening'
 
while 1:
	conn, addr = s.accept()
	print 'Connect with ' + addr[0] + ':' + str(addr[1])
	
	fingerprintType = conn.recv(10)
	print fingerprintType
	conn.send(ACK)
	jsonWifiScan = ""
	while True:
		jsonWifiScanPart = conn.recv(4096)
		if 'z' in jsonWifiScanPart:
			jsonWifiScan = jsonWifiScan + jsonWifiScanPart[:-1]
			break
		jsonWifiScan = jsonWifiScan + jsonWifiScanPart
	
	conn.send(ACK)
	jsonDecoder = json.loads(jsonWifiScan)
	if fingerprintType == wifiFingerprint:
		wifiScan = WifiScan(addr[0] + ':' + str(addr[1]), jsonDecoder)

		latitude, longitude = computeLocation(fingerprintType, wifiScan)
		latToSend = str(latitude) + "\n"
		longToSend = str(longitude) + "\n"
		
		print "====="
		print latitude
		print longitude
		
		add_to_db(fingerprintType, wifiScan, connection_to_db)
	else:
		gpsScan = GpsScan(addr[0], jsonDecoder)

		latitude, longitude = computeLocation(fingerprintType, gpsScan)
		
		latToSend = str(latitude) + "\n"
		longToSend = str(longitude) + "\n"
		
		print "====="
		print latitude
		print longitude
		
		add_to_db(fingerprintType, gpsScan, connection_to_db)

	conn.send(latToSend)
	conn.recv(10)
	conn.send(longToSend)
	conn.recv(10)

print 'Connection closed'
conn.close()
s.close()