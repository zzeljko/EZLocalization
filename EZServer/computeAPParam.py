import sqlite3
import random
import math

MIN_PATH_LOSS = 2
MAX_PATH_LOSS = 10

MIN_PI0 = -90
MAX_PI0 = -30

MIN_LATITTUDE = 44
MAX_LATITUDE = 45

MIN_LONGITUDE = 26
MAX_LONGITUDE = 27

SAME_PLACE_INTERVAL = 2000

SOLUTIONS_PER_GENERATION = 1000

class Solution():

	def __init__(self, JEZ, observationList):
		self.JEZ = JEZ
		self.observationList = observationList

class AccessPoint():

	def __init__(self, name, apPij, path_loss, Pi0, latitude, longitude):
		self.name = name
		self.path_loss = path_loss
		self.Pi0 = Pi0
		self.lat = latitude
		self.long = longitude
		self.apPij = apPij

	def __str__(self):
		return "\nMAC: " + str(self.name) + "\nPI0: " + str(self.Pi0) + "\nPathLoss: " + str(self.path_loss) + "\nLat: " + str(self.lat) + "\nLong: " + str(self.long) 

class DeviceObservation():

	def __init__(self, timestamp, latitude, longitude, gps_granted, access_points):
		self.timestamp = timestamp
		self.latitude = latitude
		self.longitude = longitude
		self.gps_granted = gps_granted
		self.access_points = access_points

	def __str__(self):
		return "\nAt timestamp: " + str(self.timestamp) + "\nLat: " + str(self.latitude) + "\nLong: " + str(self.longitude)

def compute_JEZ(observationList):
	
	s = 0
	N = 0

	for observation in observationList:
		for ap in observation.access_points:
			dij = math.sqrt((observation.latitude - ap.lat) ** 2 + (observation.longitude - ap.long) ** 2)
			s = s + abs(ap.apPij - ap.Pi0 + 10 * ap.path_loss * math.log(dij, 2))
			N = N + 1

	return s / N * 1.0

def generate_new_solution(observationList):

	for observation in observationList:
		if not observation.gps_granted:
			observation.latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			observation.longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

		for ap in observation.access_points:
			ap.path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
			ap.pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
			ap.latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			ap.longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

	JEZ = compute_JEZ(observationList)
	return Solution(JEZ, observationList)

conn = sqlite3.connect('samples.db')
c = conn.cursor()

c.execute("SELECT * from wifi_samples")

rows = c.fetchall()

c.execute("SELECT * from gps_samples")
gps_rows = c.fetchall()

observationList = []

for row in rows:
	apName = row[0]
	apPij = row[1]
	timestamp = row[2]

	observationExists = False
	for observation in observationList:
		if abs(observation.timestamp - timestamp) < SAME_PLACE_INTERVAL:
			observationExists = True

			path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
			pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
			latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			observation.access_points.append(AccessPoint(apName, apPij, path_loss, pi0, latitude, longitude))

	if not observationExists:

		path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
		pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
		ap_latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
		ap_longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

		for gps_sample in gps_rows:
			gps_timestamp = gps_sample[3]
			if abs(timestamp - gps_timestamp) < SAME_PLACE_INTERVAL:
				latitude = gps_sample[1]
				longitude = gps_sample[2]

				observationList.append(DeviceObservation(gps_timestamp, latitude, longitude, True, 
					[AccessPoint(apName, apPij, path_loss, pi0, ap_latitude, ap_longitude)]))
				
				observationExists = True
				break

		if not observationExists:
			latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			observationList.append(DeviceObservation(timestamp, latitude, longitude, False, 
				[AccessPoint(apName, apPij, path_loss, pi0, ap_latitude, ap_longitude)]))

# for observation in observationList:
# 	for ap in observation.access_points:
# 		print ap
# 	print "====="

JEZ = compute_JEZ(observationList)
solutions = [Solution(JEZ, observationList)]

for i in xrange(SOLUTIONS_PER_GENERATION):

	solutions.append(generate_new_solution(observationList))

print [solution.JEZ for solution in solutions]