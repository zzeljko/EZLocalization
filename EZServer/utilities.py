import math
from math import sqrt
import random
from scipy.optimize import fsolve
from sympy import symbols
from models import Solution, SignalAtObservation
import copy

MIN_PATH_LOSS = 1.5
MAX_PATH_LOSS = 6.0

MIN_PI0 = -50
MAX_PI0 = -1

MIN_LATITTUDE = 44.426878
MAX_LATITUDE = 44.428410

MIN_LONGITUDE = 26.048199
MAX_LONGITUDE = 26.051075

def computeJEZ(observationList):
	
	s = 0.0
	N = 0

	for observation in observationList:
		for apFingerprint in observation.apFingerprintList:
			dij = sqrt((observation.latitude - apFingerprint.ap.latitude) ** 2 + (observation.longitude - apFingerprint.ap.longitude) ** 2)
			step = abs(apFingerprint.Pij - apFingerprint.ap.Pi0 + 10 * apFingerprint.ap.loss * math.log(dij))
			s = s + step
			N = N + 1

	return s / N * 1.0

def getRandAPParam():
	loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
	pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
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

def APRandomInit(l, O):

	if l == 0:
		loss, pi0, latitude, longitude = getRandAPParam()
		return latitude, longitude, pi0, loss

def ERSGA(LDone, CDone, O, l, base, observationList, apList):

	change = False
	while not change:

		m = len(apList):
		for i in xrange(0, m):

			ap = apList[i]
			if ap not in CDone:
				O = []
				for knownObs in LDone:
					for apFingerprint in knownObs.apFingerprintList:
						if ap.name == apFingerprint.name:
							O.append(SignalAtObservation(knownObs.latitude, knownObs.longitude, apFingerprint.Pij))
							break
				if len(O) >= l:
					# see if LDone needed in function call
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
				O = []
				for apFingerprint in obs.apFingerprintList:
					O.append(SignalAtObservation(apFingerprint.ap.latitude, apFingerprint.ap.longitude, apFingerprint.Pij))
				if len(O) >= 3:
					obs.latitude, obs.longitude = betaTrilaterate(O)
					LDone.append(obs)
					change = True
	return change

def betaGenerateNewRandSol(observationList, apList):

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

# paralelizare?
def generateNewRandSol(observationList, apList):

	for ap in apList:
		ap.loss, ap.Pi0, ap.latitude, ap.longitude = getRandAPParam() 

	for obs in observationList:

		for apFingerprint in obs.apFingerprintList:
			for knownAp in apList:
				if apFingerprint.ap.name == knownAp.name:
					ap = knownAp
					break

		if obs.gpsGranted:
			continue

		if len(obs.apFingerprintList) < 3:
			obs.latitude, obs.longitude = getRandObservationCoordinates()
		else:
			obs.latitude, obs.longitude = trilaterate(obs.apFingerprintList)

	JEZ = computeJEZ(copy.deepcopy(observationList))

	return Solution(JEZ, copy.deepcopy(observationList), copy.deepcopy(apList))

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
		eq.append((knownLat - obsLat) ** 2 + (knownLong - obsLong) ** 2 - d)
		numberOfEq = numberOfEq + 1
		# if numberOfEq == 3:
		# 	break

	initialGuess = (random.uniform(MIN_LATITTUDE, MAX_LATITUDE), random.uniform(MIN_LONGITUDE, MAX_LONGITUDE), 5)
	eqLen = len(eq) - 3
	for i in xrange(eqLen):
		initialGuess = initialGuess + (5,)
	sol = fsolve(solveTrilat, initialGuess, eq)
	# print sol[0], sol[1]
	return sol[0], sol[1]

def generateRandAVector(n, m):

	a = []
	length = 4 * m + 2 * n
	for i in xrange(0, length):
		a.append(random.uniform(0, 1))

	return a