class Solution():

	def __init__(self, JEZ, observationList, apList):
		self.JEZ = JEZ
		self.observationList = observationList
		self.apList = apList
		self.taken = False

	def getApList(self):
		return self.apList

	def getObservationList(self):
		return self.observationList

	def __str__(self):
		return str(self.JEZ)

class SignalAtObservation():

	def __init__(self, latitude, longitude, Pij):
		self.latitude = latitude
		self.longitude = longitude
		self.Pij = Pij

class AccessPoint():

	def __init__(self, name, loss, Pi0, latitude, longitude, numberOfObservations):
		self.name = name
		self.loss = loss
		self.Pi0 = Pi0
		self.latitude = latitude
		self.longitude = longitude
		self.numberOfObservations = numberOfObservations

	def isSeen(self):
		self.numberOfObservations = self.numberOfObservations + 1 

	def __str__(self):
		return "\nMAC: " + str(self.name) + "\nPI0: " + str(self.Pi0) + "\nPathLoss: " + str(self.loss) + "\nLat: " + str(self.latitude) + "\nLong: " + str(self.longitude) 

class DeviceObservation():

	def __init__(self, timestamp, latitude, longitude, gpsGranted, apFingerprintList):
		self.timestamp = timestamp
		self.latitude = latitude
		self.longitude = longitude
		self.gpsGranted = gpsGranted
		self.apFingerprintList = apFingerprintList

	def __str__(self):
		return "\nAt timestamp: " + str(self.timestamp) + "\nLat: " + str(self.latitude) + "\nLong: " + str(self.longitude)

class APFingerprint:

	def __init__(self, ap, Pij):
		self.ap = ap
		self.Pij = Pij

	def __str__(self):
		return "\nMAC: " + self.ap.name + "\nlatitude: " + str(self.ap.latitude) + "\nlongitude: " + str(self.ap.longitude)