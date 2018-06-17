import math
from math import sqrt, sin, cos, sqrt, atan2, radians
import random
from scipy.optimize import fsolve
from sympy import symbols
from models import Solution, SignalAtObservation
import copy

PROCS = 4

MIN_PATH_LOSS = 1.5
MAX_PATH_LOSS = 6.0

MIN_PI0 = -50
MAX_PI0 = -1

MIN_LATITTUDE = 44.426878
MAX_LATITUDE = 44.428410

MIN_LONGITUDE = 26.048199
MAX_LONGITUDE = 26.051075

LAT_DEG_TO_METERS = 111200
LONG_DEG_TO_METERS = 79990

def signature():
	if random.randint(-1, 1) < 0:
		return -1
	return 1

def computeJEZ(observationList):
	
	s = 0.0
	N = 0
	for observation in observationList:
		for apFingerprint in observation.apFingerprintList:

			R = 6373.0

			lat1 = radians(observation.latitude)
			lon1 = radians(observation.longitude)
			lat2 = radians(apFingerprint.ap.latitude)
			lon2 = radians(apFingerprint.ap.longitude)

			dlon = lon2 - lon1
			dlat = lat2 - lat1

			a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			dij = R * c * 1000
			step = abs(apFingerprint.Pij - apFingerprint.ap.Pi0 + 10 * apFingerprint.ap.loss * math.log(dij))
			s = s + step
			N = N + 1

	return s / N * 1.0

def getRandAPParam():
	
	loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
	pi0 = random.uniform(MIN_PI0, MAX_PI0)
	latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
	longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

	return loss, pi0, latitude, longitude

def getRandObservationCoordinates():

	latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
	longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

	return latitude, longitude

def getGPSSeenAPList(observationList, apList):

	gpsSeenAPList = []
	for obs in observationList:
		if obs.gpsGranted:
			for ap in apList:
				if not ap in gpsSeenAPList:
					gpsSeenAPList.append(ap)

	return gpsSeenAPList

def solveEqL45(apUnknown, equationList):
	unknown = apUnknown
	apLat, apLong, Pi0, loss = symbols('apLat apLong Pi0 loss', real=True)
	equations = ()
	for eq in equationList:
		equations = equations + (eq.subs([(apLat, unknown[0]), (apLong, unknown[1]), 
			(Pi0, unknown[2]), (loss, unknown[3])]),)
	return equations

def solveEqL3(apUnknown, equationList):
	unknown = apUnknown
	apLat, apLong, Pi0 = symbols('apLat apLong Pi0', real=True)
	equations = ()
	for eq in equationList:
		equations = equations + (eq.subs([(apLat, unknown[0]), (apLong, unknown[1]), 
			(Pi0, unknown[2])]),)
	return equations

def solveEqL12(apUnknown, equationList):
	unknown = apUnknown
	apLat, apLong = symbols('apLat apLong', real=True)
	equations = ()
	for eq in equationList:
		equations = equations + (eq.subs([(apLat, unknown[0]), (apLong, unknown[1])]),)
	return equations

def APRandomInit(l, O):

	# if l >= 4:

	# 	apLat, apLong, Pi0, loss = symbols('apLat apLong Pi0 loss', real=True)
	# 	eq = []
	# 	for signalAtObs in O:
	# 		obsLat = signalAtObs.latitude
	# 		obsLong = signalAtObs.longitude
	# 		Pij = signalAtObs.Pij

	# 		eq.append((obsLat - apLat) ** 2 + (obsLong - apLong) ** 2 - 10 ** (((Pi0 - Pij) / 10 * loss)))
	# 		if len(eq) == l:
	# 			break

	# 	initialGuess = (random.uniform(MIN_LATITTUDE, MAX_LATITUDE), 
	# 		random.uniform(MIN_LONGITUDE, MAX_LONGITUDE), random.uniform(MIN_PI0, MAX_PI0), 
	# 		random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS))

	# 	eqLen = len(eq) - 4
	# 	for i in xrange(eqLen):
	# 		initialGuess = initialGuess + (5,)
	# 	sol = fsolve(solveEqL45, initialGuess, eq)
	# 	return sol[0], sol[1], sol[2], sol[3]

	# if l == 3:

	# 	loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
	# 	apLat, apLong, Pi0 = symbols('apLat apLong Pi0', real=True)
	# 	eq = []
	# 	for signalAtObs in O:
	# 		obsLat = signalAtObs.latitude
	# 		obsLong = signalAtObs.longitude
	# 		Pij = signalAtObs.Pij

	# 		eq.append((obsLat - apLat) ** 2 + (obsLong - apLong) ** 2 - 10 ** (((Pi0 - Pij) / 10 * loss)))

	# 		if len(eq) == 3:
	# 			break

	# 	initialGuess = (random.uniform(MIN_LATITTUDE, MAX_LATITUDE), 
	# 		random.uniform(MIN_LONGITUDE, MAX_LONGITUDE), random.uniform(MIN_PI0, MAX_PI0))

	# 	eqLen = len(eq) - 3
	# 	for i in xrange(eqLen):
	# 		initialGuess = initialGuess + (5,)
	# 	sol = fsolve(solveEqL3, initialGuess, eq)
	# 	return sol[0], sol[1], sol[2], loss

	# if l == 1 or l == 2:

	# 	Pi0 = random.uniform(MIN_PI0, MAX_PI0)
	# 	loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
	# 	apLat, apLong = symbols('apLat apLong', real=True)
	# 	eq = []
	# 	for signalAtObs in O:
	# 		obsLat = signalAtObs.latitude
	# 		obsLong = signalAtObs.longitude
	# 		Pij = signalAtObs.Pij

	# 		eq.append((obsLat - apLat) ** 2 + (obsLong - apLong) ** 2 - 10 ** (((Pi0 - Pij) / 10 * loss)))
	# 		if len(eq) == 3:
	# 			break

	# 	initialGuess = (random.uniform(MIN_LATITTUDE, MAX_LATITUDE), 
	# 		random.uniform(MIN_LONGITUDE, MAX_LONGITUDE))

	# 	eqLen = len(eq) - 3
	# 	for i in xrange(eqLen):
	# 		initialGuess = initialGuess + (5,)
	# 	sol = fsolve(solveEqL12, initialGuess, eq)
	# 	return sol[0], sol[1], Pi0, loss

	loss, pi0, latitude, longitude = getRandAPParam()
	return latitude, longitude, pi0, loss

def ERSGA(LDone, CDone, O, l, base, observationList, apList):

	change = False
	while not change:

		m = len(apList)
		for i in xrange(0, m):

			ap = apList[i]
			if ap not in CDone:
				O = []
				for knownObs in LDone:
					for apFingerprint in knownObs.apFingerprintList:
						if ap.name == apFingerprint.ap.name:
							O.append(SignalAtObservation(knownObs.latitude, knownObs.longitude, apFingerprint.Pij))
							break
				if len(O) >= l:
					ap.latitude, ap.longitude, ap.Pi0, ap.loss = APRandomInit(l, O)
					CDone.append(ap)
					change = True
					if l < base:
						return True

		if not change:
			if l > 0:
				change = ERSGA(LDone, CDone, O, l - 1, base, observationList, apList)
				if l < base:
					return change
			else:
				return change

		n = len(observationList)
		for j in xrange(0, n):
			obs = observationList[j]
			if obs not in LDone:
				if len(obs.apFingerprintList) >= 3:
					obs.latitude, obs.longitude = trilaterate(obs.apFingerprintList)
					LDone.append(obs)
					change = True
	return change

def generateNewRandSol(observationList, apList):

	LDone = []
	for obs in observationList:
		if obs.gpsGranted:
			LDone.append(obs)
	CDone = []
	O = []
	if len(LDone) >= 5:
		base = 5
	else:
		base = len(LDone)

	l = base
	ERSGA(LDone, CDone, O, l, base, observationList, apList)
	return Solution(computeJEZ(observationList), copy.deepcopy(observationList), copy.deepcopy(apList))

def solveTrilat(obsCoord, d):
	unknown = obsCoord
	obsLat, obsLong = symbols('obsLat obsLong', real=True)
	equations = ()
	for eq in d:
		equations = equations + (eq.subs([(obsLat, unknown[0]), (obsLong, unknown[1])]),)
	return equations

def trilaterate(apFingerprintList):

	obsLat, obsLong = symbols('obsLat obsLong', real=True)
	eq = []
	numberOfEq = 0
	for apFingerprint in apFingerprintList:
		Pi = apFingerprint.ap.Pi0
		loss = apFingerprint.ap.loss
		Pij = apFingerprint.Pij
		knownLat = apFingerprint.ap.latitude
		knownLong = apFingerprint.ap.longitude
				
		d = 10 ** ((Pi - Pij) / (10 * loss))
		eq.append((LAT_DEG_TO_METERS * (knownLat - obsLat)) ** 2 + (LONG_DEG_TO_METERS * (knownLong - obsLong)) ** 2 - d ** 2)
		numberOfEq = numberOfEq + 1
		if numberOfEq == 3:
			break

	initialGuess = (random.uniform(MIN_LATITTUDE, MAX_LATITUDE), random.uniform(MIN_LONGITUDE, MAX_LONGITUDE), 5)
	eqLen = len(eq) - 3
	for i in xrange(eqLen):
		initialGuess = initialGuess + (5,)

	obsCoordinates = fsolve(solveTrilat, initialGuess, eq)
	return obsCoordinates[0], obsCoordinates[1]

def generateRandAVector(n, m):

	a = []
	length = 4 * m + 2 * n
	for i in xrange(0, length):
		a.append(random.uniform(0, 1))

	return a