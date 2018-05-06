import socket
import sys
import json
import sqlite3
from EZWifi import WifiScan
 
def create_table():
	
	conn = sqlite3.connect('samples.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS wifisamples (bssId varchar(25), signalStrength integer, channel integer, timestamp bigint)")

	return conn

def add_to_db(wifiScan, conn):

	c = conn.cursor()
	for ap in wifiScan.wifiAPList:
		c.execute("insert into wifisamples values (?, ?, ?, ?)", [ap.bssId, ap.signal, ap.channel, wifiScan.timestamp])
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
    jsonWifiScan = conn.recv(3000)
    jsonWifiScan = jsonWifiScan[2:len(jsonWifiScan)]

    jsonDecoder = json.loads(jsonWifiScan)
    wifiScan = WifiScan(addr[0] + ':' + str(addr[1]), jsonDecoder)
    add_to_db(wifiScan, connection_to_db)
    # print str(wifiScan)

print 'Connection closed'
conn.close()
s.close()