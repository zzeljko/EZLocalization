import math
import sympy
from sympy import symbols, diff, log
from multiprocessing import Manager, Pool 
from models import Solution, DeviceObservation, APFingerprint, AccessPoint
from cmath import phase
from math import sqrt, sin, atan2, log, sin, cos
from utilities import computeJEZ
import copy

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

def multiprocessing_gradient_descent(solution):
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
				g = (xPi0 - 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) - 1.7)/abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + 1.7)
				Pi0 = Pi0 - alpha * g
				s = g * g

				g = (100*xloss*phase(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2 + 10*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + 1.7)*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))))/abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + 1.7)
				loss = loss - alpha * g
				s = s + g * g

				g = 10*xloss*((-2*xapLat + 2*xobsLat)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (-2*xapLat + 2*xobsLat)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + 1.7)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + 1.7)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
				apLat = apLat - alpha * g
				s = s + g * g

				g = 10*xloss*((-2*xapLong + 2*xobsLong)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (-2*xapLong + 2*xobsLong)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + 1.7)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + 1.7)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
				apLong = apLong - alpha * g
				s = s + g * g

				if not observation.gpsGranted:
					g = 10*xloss*((2*xapLat - 2*xobsLat)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (2*xapLat - 2*xobsLat)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + 1.7)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + 1.7)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
					obsLat = obsLat - alpha * g
					s = s + g * g

					g = 10*xloss*((2*xapLong - 2*xobsLong)*sin(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2 + (2*xapLong - 2*xobsLong)*cos(atan2(0, xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)**2*sign(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2)/2)*(-xPi0 + 10*xloss*log(abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))) + 1.7)/(abs(-xPi0 + 10*xloss*log(sqrt((-xapLat + xobsLat)**2 + (-xapLong + xobsLong)**2)) + 1.7)*abs(sqrt(xapLat**2 - 2*xapLat*xobsLat + xapLong**2 - 2*xapLong*xobsLong + xobsLat**2 + xobsLong**2))**2)
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
			newAPFingerprintList.append(APFingerprint(AccessPoint(apFingerprint.ap.name, loss, Pi0, 
				apLat, apLong, apFingerprint.ap.numberOfObservations), Pij))

		newObservationList.append(DeviceObservation(observation.timestamp, obsLat, obsLong, observation.gpsGranted, newAPFingerprintList))
	
	newSolutionList.append(Solution(computeJEZ(copy.deepcopy(newObservationList)), copy.deepcopy(newObservationList), copy.deepcopy(newApList)))

def gradient_descent(solutionList):
	
	global alpha, epsilon
	
	global newSolutionList

	manager = Manager()
	newSolutionList = manager.list()

	alpha = 0.00001
	epsilon = 0.1

	pool = Pool(processes=PROCS)
	pool.map(multiprocessing_gradient_descent, solutionList, chunksize = len(solutionList) / PROCS)
	pool.close()
	return newSolutionList
