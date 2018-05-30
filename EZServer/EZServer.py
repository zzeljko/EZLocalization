import socket
import sys
import json
import sqlite3
from EZWifi import WifiScan
from EZGPS import GpsScan
 
MAX_CONNECTION_TYPE = 4
wifiFingerprint = "WIFI"
gpsFingerprint = "GPS"
ACK = "ACK"

def create_table():
	
	conn = sqlite3.connect('samples.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS wifi_samples (bssId varchar(25), signalStrength integer, channel integer, timestamp bigint)")
	c.execute("CREATE TABLE IF NOT EXISTS gps_samples (client varchar(25), latitude double precision, longitude double precision, timestamp bigint)")
	return conn

def add_to_db(scanType, scan, conn):
	c = conn.cursor()

	if scanType == wifiFingerprint:
		for ap in scan.wifiAPList:
			c.execute("insert into wifi_samples values (?, ?, ?, ?)", [ap.bssId, ap.signal, ap.channel, scan.timestamp])
			conn.commit()
	else:
		c.execute("insert into gps_samples values (?, ?, ?, ?)", [scan.client, scan.latitude, scan.longitude, scan.timestamp])
		conn.commit()

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
	jsonWifiScanPart = conn.recv(4096)
	while len(jsonWifiScanPart):
		jsonWifiScan = jsonWifiScan + jsonWifiScanPart
		jsonWifiScanPart = conn.recv(4096)

	jsonDecoder = json.loads(jsonWifiScan)
	
	if fingerprintType == wifiFingerprint:
		wifiScan = WifiScan(addr[0] + ':' + str(addr[1]), jsonDecoder)
		add_to_db(fingerprintType, wifiScan, connection_to_db)
	else:
		gpsScan = GpsScan(addr[0], jsonDecoder)
		add_to_db(fingerprintType, gpsScan, connection_to_db)


print 'Connection closed'
conn.close()
s.close()