import math
import sympy
from sympy import symbols, diff, log, sqrt
from multiprocessing import Manager, Pool 
from Solution import Solution, DeviceObservation, AccessPointObservation
from cmath import phase
from math import sqrt, sin, atan2, log, sin, cos

PROCS = 8

def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x

def compute_JEZ(observationList):
	
	s = 0.0
	N = 0

	for observation in observationList:
		for ap in observation.access_points:
			dij = math.sqrt((observation.latitude - ap.lat) ** 2 + (observation.longitude - ap.long) ** 2)
			step = abs(ap.apPij - ap.Pi0 + 10 * ap.path_loss * math.log(dij))
			# print "============"
			# print observation.latitude
			# print observation.longitude
			# print ap.lat
			# print ap.long
			# print dij
			# print ap.apPij
			# print ap.Pi0
			# print ap.path_loss
			# print "============"
			s = s + step
			N = N + 1
			# print step

	return s / N * 1.0

def multiprocessing_gradient_descent(solution):
	global newSolutionList

	newObservationList = []
	count = 0
	for observation in solution.observationList:
		xobsLat = obsLat = observation.latitude
		xobsLong = obsLong = observation.longitude

		apList = []
		for ap in observation.access_points:
			Pij = ap.apPij
			xPi0 = Pi0 = ap.Pi0
			xloss = loss = ap.path_loss
			xapLat = apLat = ap.lat
			xapLong = apLong = ap.long

			while True:
				g = (xPi0 - 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) - Pij)/abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + Pij)
				Pi0 = Pi0 - alpha * g
				s = g * g

				g = (100*xloss*phase(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2 + 10*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + Pij)*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))))/abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + Pij)
				loss = loss - alpha * g
				s = s + g * g

				g = 10*xloss*((-2*xapLat + 2*xobsLat)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (-2*xapLat + 2*xobsLat)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + Pij)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + Pij)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
				apLat = apLat - alpha * g
				s = s + g * g

				g = 10*xloss*((-2*xapLong + 2*xobsLong)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (-2*xapLong + 2*xobsLong)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + Pij)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + Pij)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
				apLong = apLong - alpha * g
				s = s + g * g

				if not observation.gps_granted:
					g = 10*xloss*((2*xapLat - 2*xobsLat)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (2*xapLat - 2*xobsLat)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + Pij)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + Pij)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
					obsLat = obsLat - alpha * g
					s = s + g * g

					g = 10*xloss*((2*xapLong - 2*xobsLong)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (2*xapLong - 2*xobsLong)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + Pij)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + Pij)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
					obsLong = obsLong - alpha * g
					s = s + g * g
				# print "==========="
				# print Pi0
				# print loss
				# print apLat
				# print apLong
				# print obsLat
				# print obsLong
				# print "=========="
				norm = sqrt(s)
				# print alpha * norm
				# print epsilon
				# print "====="
				if alpha * norm <= epsilon:
					break

				xPi0 = Pi0
				xloss = loss
				xapLat = apLat
				xapLong = apLong
				xobsLat = obsLat
				xobsLong = obsLong


			# print "broken"
			# print count
			# count = count + 1
			apList.append(AccessPointObservation(ap.name, Pij, loss, Pi0, apLat, apLong))

		newObservationList.append(DeviceObservation(observation.timestamp, obsLat, obsLong, observation.gps_granted, apList))
	
	newSolutionList.append(Solution(compute_JEZ(newObservationList), newObservationList))

def gradient_descent(solutionList):
	
	global alpha, epsilon, count, ctPij
	
	global newSolutionList
	manager = Manager()
	newSolutionList = manager.list()

	alpha = 0.0001
	epsilon = 0.1
	count = 0
	ctPij = -60
	# newSolutionList = []

	pool = Pool(processes=PROCS)
	pool.map(multiprocessing_gradient_descent, solutionList, chunksize = len(solutionList) / PROCS)
	pool.close()

	return newSolutionList
