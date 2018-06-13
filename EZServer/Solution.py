class Solution():

	def __init__(self, JEZ, observationList):
		self.JEZ = JEZ
		self.observationList = observationList

	def __str__(self):
		return str(self.JEZ)

class AccessPointGPSFingerprint():

	def __init__(self, name):
		self.name = name
		self.gpsObservationList = []
		self.wasSolved = False

	def addObservation(self, gpsObservation):
		self.gpsObservationList.append(gpsObservation)

class AccessPoint():

	def __init__(self, name):
		self.name = name
		self.count = 1

	def newFingerprint(self):
		self.count = self.count + 1

class AccessPointObservation():

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

class Mock():

	def __init__(self, bla):
		self.bla = bla