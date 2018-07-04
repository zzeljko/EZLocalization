import math
import sympy
from sympy import symbols, diff, log
from multiprocessing import Manager, Pool 
from models import Solution, DeviceObservation, APFingerprint, AccessPoint
from cmath import phase
from math import sqrt, sin, atan2, log, sin, cos
from utilities import computeJEZ
import copy

PROCS = 4

def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x

def multiprocessingGradientDescent(solution):
	global newSolutionList

	newObservationList = []
	newApList = []

	for observation in solution.observationList:
		xobsLat = obsLat = observation.latitude
		xobsLong = obsLong = observation.longitude

		newAPFingerprintList = []
		for apFingerprint in observation.apFingerprintList:
			apExists = False
			for ap in newApList:
				if ap.name == apFingerprint.ap.name:
					apExists = True
					break
			if not apExists:
				newApList.append(apFingerprint.ap)

			Pij = apFingerprint.Pij
			xPi0 = Pi0 = apFingerprint.ap.Pi0
			xloss = loss = apFingerprint.ap.loss
			xapLat = apLat = apFingerprint.ap.latitude
			xapLong = apLong = apFingerprint.ap.longitude
			while True:
				g = (xPi0 - 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) - Pij)*sqrt((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2)/(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2
				Pi0 = Pi0 - alpha * g
				s = g * g

				g = 10*sqrt((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2)*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)*log(10))
				loss = loss - alpha * g
				s = s + g * g

				g = 10*xloss*(-xapLat + xobsLat)*sqrt((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2)/(((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)*(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)*log(10))
				apLat = apLat - alpha * g
				s = s + g * g

				g = 10*xloss*(-xapLong + xobsLong)*sqrt((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2)/(((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)*(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)*log(10))
				apLong = apLong - alpha * g
				s = s + g * g

				if not observation.gpsGranted:
					g = 10*xloss*(xapLat - xobsLat)*sqrt((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2)/(((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)*(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)*log(10))
					obsLat = obsLat - alpha * g
					s = s + g * g

					g = 10*xloss*(xapLong - xobsLong)*sqrt((-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)**2)/(((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)*(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2))/log(10) + Pij)*log(10))
					obsLong = obsLong - alpha * g
					s = s + g * g

				norm = sqrt(s)
				if alpha * norm <= epsilon:
					break

				xPi0 = Pi0
				xloss = loss
				xapLat = apLat
				xapLong = apLong
				xobsLat = obsLat
				xobsLong = obsLong

			# apFingerprint.ap.Pi0 = Pi0
			# apFingerprint.ap.loss = loss
			# apFingerprint.ap.latitude = apLat
			# apFingerprint.ap.longitude = apLong
			

			newAPFingerprintList.append(APFingerprint(AccessPoint(apFingerprint.ap.name, loss, Pi0, 
				apLat, apLong, apFingerprint.ap.numberOfObservations), Pij))

		newObservationList.append(DeviceObservation(observation.timestamp, obsLat, obsLong, observation.gpsGranted, newAPFingerprintList))
	
	newSolutionList.append(Solution(computeJEZ(copy.deepcopy(newObservationList)), copy.deepcopy(newObservationList), copy.deepcopy(newApList)))

def gradientDescent(solutionList):
	
	global alpha, epsilon
	
	global newSolutionList

	manager = Manager()
	newSolutionList = manager.list()

	alpha = 0.000000001
	epsilon = 0.1

	pool = Pool(processes=PROCS)
	pool.map(multiprocessingGradientDescent, solutionList, chunksize = len(solutionList) / PROCS)
	pool.close()
	return newSolutionList
