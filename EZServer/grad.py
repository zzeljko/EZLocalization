import math
import sympy
from sympy import symbols, diff, log, sqrt

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

class Solution():

	def __init__(self, JEZ, observationList):
		self.JEZ = JEZ
		self.observationList = observationList

	def __str__(self):
		return str(self.JEZ)

def compute_JEZ(observationList):
	
	s = 0
	N = 0

	for observation in observationList:
		for ap in observation.access_points:
			dij = math.sqrt((observation.latitude - ap.lat) ** 2 + (observation.longitude - ap.long) ** 2)
			s = s + abs(ap.apPij - ap.Pi0 + 10 * ap.path_loss * math.log(dij, 2))
			N = N + 1

	return s / N * 1.0

def gradient_descent(solutionList):
	alpha = 0.0001
	epsilon = 0.1
	newSolutionList = []
	count = 0
	ctPij = -60

	xPi0, xloss, xobsLat, xobsLong, xapLat, xapLong = symbols('xPi0 xloss xobsLat xobsLong xapLat xapLong', real=True)				
	function = abs(ctPij - xPi0 + 10 * xloss * log(sqrt((xobsLat - xapLat) ** 2 + (xobsLong - xapLong) ** 2)))
	
	derivative1 = diff(function, xPi0)
	derivative2 = diff(function, xloss)
	derivative3 = diff(function, xapLat)
	derivative4 = diff(function, xapLong)
	derivative5 = diff(function, xobsLat)
	derivative6 = diff(function, xobsLong)
	
	for solution in solutionList:
		newObservationList = []
		for observation in solution.observationList:
			obsLat = observation.latitude
			obsLong = observation.longitude

			apList = []
			for ap in observation.access_points:
				Pij = ap.apPij
				Pi0 = ap.Pi0
				loss = ap.path_loss
				apLat = ap.lat
				apLong = ap.long

				while True:
					g = derivative1.subs({xPi0:Pi0, xloss:loss, xobsLat:obsLat, xobsLong:obsLong, xapLat:apLat, xapLong:apLong})
					Pi0 = Pi0 - alpha * g
					s = g * g

					g = derivative2.subs({xPi0:Pi0, xloss:loss, xobsLat:obsLat, xobsLong:obsLong, xapLat:apLat, xapLong:apLong})
					loss = loss - alpha * g
					s = s + g * g

					g = derivative3.subs({xPi0:Pi0, xloss:loss, xobsLat:obsLat, xobsLong:obsLong, xapLat:apLat, xapLong:apLong})
					apLat = apLat - alpha * g
					s = s + g * g

					g = derivative4.subs({xPi0:Pi0, xloss:loss, xobsLat:obsLat, xobsLong:obsLong, xapLat:apLat, xapLong:apLong})
					apLong = apLong - alpha * g
					s = s + g * g

					if not observation.gps_granted:
						g = derivative5.subs({xPi0:Pi0, xloss:loss, xobsLat:obsLat, xobsLong:obsLong, xapLat:apLat, xapLong:apLong})
						obsLat = obsLat - alpha * g
						s = s + g * g

						g = derivative6.subs({xPi0:Pi0, xloss:loss, xobsLat:obsLat, xobsLong:obsLong, xapLat:apLat, xapLong:apLong})
						obsLong = obsLong - alpha * g
						s = s + g * g

					norm = sqrt(s)
					# print alpha * norm
					# print epsilon
					# print "====="
					if alpha * norm <= epsilon:
						break

				# print "broken"
				# print count
				# count = count + 1
				apList.append(AccessPoint(ap.name, Pij, loss, Pi0, apLat, apLong))

			newObservationList.append(DeviceObservation(observation.timestamp, obsLat, obsLong, observation.gps_granted, apList))
		
		newSolutionList.append(Solution(compute_JEZ(newObservationList), newObservationList))			

	return newSolutionList
