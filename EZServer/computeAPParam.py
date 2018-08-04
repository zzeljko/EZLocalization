import sqlite3
import random
import numpy
from models import Solution, AccessPoint, APFingerprint, DeviceObservation
from utilities import computeJEZ, getRandAPParam, getGPSSeenAPList, getRandObservationCoordinates
from grad import gradientDescent
import copy
from utilities import signature, generateRandAVector, trilaterate, generateNewRandSol
from numpy.random import exponential

SAME_PLACE_INTERVAL = 2000

SOLUTIONS_PER_GENERATION = 100

TEN_PERCENT = 10 / 100.0
SIXTY_PERCENT = 60 / 100.0
TWENTY_PERCENT = 20 / 100.0	

conn = sqlite3.connect('samples.db')
c = conn.cursor()

c.execute("SELECT * from wifi_samples_precis")

rows = c.fetchall()

c.execute("SELECT * from gps_samples_precis")
gps_rows = c.fetchall()

observationList = []
allAPList = []
for row in rows:
	apName = row[0]

	Pij = row[1]
	timestamp = row[2]

	observationExists = False
	for observation in observationList:
		if observation.timestamp == timestamp:
			
			observationExists = True
			
			currentAP = None
			for ap in allAPList:
				if ap.name == apName:
					currentAP = ap
					break

			if currentAP == None:		
				path_loss, pi0, latitude, longitude = getRandAPParam()
				currentAP = AccessPoint(apName, path_loss, pi0, latitude, longitude, 1)
				allAPList.append(currentAP)
			else:
				currentAP.isSeen()			
			
			observation.apFingerprintList.append(APFingerprint(currentAP, Pij))

	if not observationExists:

		currentAP = None
		for ap in allAPList:
			if ap.name == apName:
				currentAP = ap
				break

		if currentAP == None:		
			path_loss, pi0, latitude, longitude = getRandAPParam()
			currentAP = AccessPoint(apName, path_loss, pi0, latitude, longitude, 1)
			allAPList.append(currentAP)
		else:
			currentAP.isSeen()

		gpsAvail = False
		for gps_sample in gps_rows:

			gps_timestamp = gps_sample[3]
			if abs(timestamp - gps_timestamp) < SAME_PLACE_INTERVAL:

				latitude = gps_sample[1]
				longitude = gps_sample[2]

				gpsAvail = True
				break

		if not gpsAvail:
			latitude, longitude = getRandObservationCoordinates()

		deviceObservation = DeviceObservation(timestamp, latitude, longitude, gpsAvail, 
			[APFingerprint(currentAP, Pij)])
		observationList.append(deviceObservation)

apToKeep = []
for obs in observationList:
	fingerprintToKeepList = []
	for apFingerprint in obs.apFingerprintList:
		if apFingerprint.ap.numberOfObservations >= 5:
			fingerprintToKeepList.append(apFingerprint)
			if not apFingerprint.ap in apToKeep:
				apToKeep.append(apFingerprint.ap)
	obs.apFingerprintList = copy.deepcopy(fingerprintToKeepList)

oldSolutions = []

for i in xrange(SOLUTIONS_PER_GENERATION):
	oldSolutions.append(generateNewRandSol(copy.deepcopy(observationList), copy.deepcopy(apToKeep)))

for sol in oldSolutions:
	print sol

for obs in oldSolutions[0].getObservationList():
	if not obs.gpsGranted:
		print obs

oldSolutions = copy.deepcopy(gradientDescent(copy.deepcopy(oldSolutions)))

for sol in oldSolutions:
	print sol.JEZ

for obs in oldSolutions[0].getObservationList():
	if not obs.gpsGranted:
		print obs

bestOldSolutions = copy.deepcopy([oldSolutions[i] for i in xrange(0, int(TEN_PERCENT * SOLUTIONS_PER_GENERATION))])
a = generateRandAVector(len(observationList), len(apToKeep))
while True:

	newSolutions = []
	for i in xrange(0, int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)):
		best = 1000
		for oldSolution in oldSolutions:
			if oldSolution.JEZ < best:
				bestSolution = oldSolution
				best = oldSolution.JEZ
		newSolutions.append(copy.deepcopy(bestSolution))
		oldSolutions.remove(bestSolution)

	for sol in newSolutions:
		print sol
	print '\n'
	# for obs in newSolutions[0].getObservationList():
	# 	if not obs.gpsGranted:
	# 		print obs
	# print '\n'

	isBetter = False
	index = 0
	for solution in newSolutions:
		if solution.JEZ < bestOldSolutions[index].JEZ:
			isBetter = True
			break
		index = index + 1

	if not isBetter:
		print count
		count = count + 1
	else:
		count = 0

	if count == 10:
		break

	for i in xrange(0, int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)):
		newSolutions.append(generateNewRandSol(copy.deepcopy(observationList), copy.deepcopy(apToKeep)))

	combinedSolList = []
	for i in xrange(0, int(SIXTY_PERCENT * SOLUTIONS_PER_GENERATION)):
		S1 = copy.deepcopy(random.choice(oldSolutions))
		S2 = copy.deepcopy(random.choice(oldSolutions))

		S1ApList = copy.deepcopy(S1.getApList())
		S2ApList = copy.deepcopy(S2.getApList())

		newApList = []
		apIndex = 0
		aIndex = 0
		combinedApList = []
		for ap in S1ApList:
			newLatitude = a[aIndex] * ap.latitude + (1 - a[aIndex]) * S2ApList[apIndex].latitude
			newLongitude = a[aIndex + 1] * ap.longitude + (1 - a[aIndex + 1]) * S2ApList[apIndex].longitude
			newLoss = a[aIndex + 2] * ap.loss + (1 - a[aIndex + 2]) * S2ApList[apIndex].loss
			newPi0 = a[aIndex + 3] * ap.Pi0 + (1 - a[aIndex + 3]) * S2ApList[apIndex].Pi0

			combinedApList.append(AccessPoint(ap.name, copy.deepcopy(newLoss), copy.deepcopy(newPi0), 
				copy.deepcopy(newLatitude), copy.deepcopy(newLongitude), ap.numberOfObservations))

			aIndex = aIndex + 4
			apIndex = apIndex + 1

		S1ObsList = copy.deepcopy(S1.getObservationList())
		S2ObsList = copy.deepcopy(S2.getObservationList())

		obsIndex = 0
		combinedObsList = []
		for obs in S1ObsList:
			if not obs.gpsGranted:
				newLatitude = a[aIndex] * obs.latitude + (1 - a[aIndex]) * S2ObsList[obsIndex].latitude
				newLongitude = a[aIndex + 1] * obs.longitude + (1 - a[aIndex + 1]) * S2ObsList[obsIndex].longitude
			else:
				newLatitude = obs.latitude
				newLongitude = obs.longitude

			aIndex = aIndex + 2
			obsIndex = obsIndex + 1
			for fingerprint in obs.apFingerprintList:
				for newAp in combinedApList:
					if fingerprint.ap.name == newAp.name:
						fingerprint.ap = newAp
						break
			combinedObsList.append(DeviceObservation(obs.timestamp, copy.deepcopy(newLatitude), 
				copy.deepcopy(newLongitude), obs.gpsGranted, copy.deepcopy(obs.apFingerprintList)))

		newSolutionObsList = copy.deepcopy(combinedObsList)
		newSolutionApList = copy.deepcopy(combinedApList)
		combinedSolList.append(Solution(computeJEZ(newSolutionObsList), newSolutionObsList, newSolutionApList))

	combinedSolList = copy.deepcopy(gradientDescent(copy.deepcopy(combinedSolList)))
	newSolutions = newSolutions + combinedSolList

	combinedSolList = []
	for i in xrange(0, int(TWENTY_PERCENT * SOLUTIONS_PER_GENERATION)):
		SRand = copy.deepcopy(random.choice(oldSolutions))

		SApList = copy.deepcopy(SRand.getApList())
		SObsList = copy.deepcopy(SRand.getObservationList())

		randApList = []
		for ap in SApList:
			randApList.append(AccessPoint(ap.name, copy.deepcopy(ap.loss + signature() * exponential()), 
				copy.deepcopy(ap.Pi0 + signature() * exponential()), copy.deepcopy(ap.latitude) + signature() * exponential(),
				copy.deepcopy(ap.longitude) + signature() * exponential(), ap.numberOfObservations))

		randObsList = []
		for obs in SObsList:
			for fingerprint in obs.apFingerprintList:
				for ap in randApList:
					if fingerprint.ap.name == ap.name:
						fingerprint.ap = ap
						break
			if obs.gpsGranted:
				latitude = obs.latitude
				longitude = obs.longitude
			else:
				latitude = obs.latitude + signature() * exponential()
				longitude = obs.longitude + signature() * exponential()

			randObsList.append(DeviceObservation(obs.timestamp, copy.deepcopy(latitude), 
				copy.deepcopy(longitude), obs.gpsGranted, copy.deepcopy(obs.apFingerprintList)))

		newSolutionObsList = copy.deepcopy(randObsList)
		newSolutionApList = copy.deepcopy(randApList)
		combinedSolList.append(Solution(computeJEZ(randObsList), randObsList, randApList))

	combinedSolList = copy.deepcopy(gradientDescent(copy.deepcopy(combinedSolList)))
	newSolutions = newSolutions + combinedSolList
	bestOldSolutions = copy.deepcopy(newSolutions[0:int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)])
	oldSolutions = copy.deepcopy(newSolutions)

for sol in newSolutions:
	print sol.JEZ
for obs in newSolutions[0].getObservationList():
	print obs

conn = sqlite3.connect('samples.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS ap_loc_precis (bssId varchar(25), Pi0 double precision, path_loss double precision, latitude double precision, longitude double precision)")

for ap in newSolutions[0].getApList():
	c.execute("insert into ap_loc_precis values (?, ?, ?, ?, ?)", [ap.name, ap.Pi0, ap.loss, ap.latitude, ap.longitude])
	conn.commit()

