import sqlite3
import random
import math
import numpy
from grad import DeviceObservation, AccessPointObservation, Solution, gradient_descent, compute_JEZ
from Solution import AccessPoint, AccessPointGPSFingerprint, Solution, DeviceObservation, AccessPointObservation
from trilat import trilat
from scipy.optimize import fsolve
from sympy import symbols

MIN_PATH_LOSS = 1.5
MAX_PATH_LOSS = 6.0

MIN_PI0 = -50
MAX_PI0 = -1

MIN_LATITTUDE = 44.426878
MAX_LATITUDE = 44.428410

MIN_LONGITUDE = 26.048199
MAX_LONGITUDE = 26.051075

SAME_PLACE_INTERVAL = 2000

SOLUTIONS_PER_GENERATION = 100

TEN_PERCENT = 10 / 100.0
SIXTY_PERCENT = 60 / 100.0
TWENTY_PERCENT = 20 / 100.0

# def ERSGA(LDone, CDone, O, l, base, apList):
# 	change = False
# 	while not change:
# 		for apName in apList:
# 			if apName not in CDone:
# 				setO = []
# 				for observation in LDone:
# 					for ap in observation.access_points:
# 						if ap.name == apName:
# 							setO.append(ap.apPij)
# 							break
# 				if len(O) >= l:




# def generate_new_random_solution_beta(O):
# 	LDone = []
# 	apList = []
# 	for observation in O:
# 		if observation.gps_granted:
# 			LDone.append(observation)
# 		for ap in observation.access_points:
# 			if ap.name not in apList:
# 				apList.append(ap.name)

# 	CDone = []
# 	if len(LDone) >= 5:
# 		base = 5
# 	else:
# 		base = len(LDone)

# 	l = base
# 	ERSGA(LDone, CDone, O, l, base, apList)

def trilaterate(accessPointFingerprint):

	apLat, apLong = symbols('apLat apLong', real=True)
	eq = []
	numberOfEq = 0
	for obs in accessPointFingerprint.gpsObservationList:
		Pi = 0
		loss = 0
		Pij = 0
		for ap in obs.access_points:
			if ap.name == accessPointFingerprint.name:
				Pi = ap.apPij
				Pi0 = ap.Pi0
				loss = ap.path_loss
				break
				
		d = 10 ** ((Pi - Pij) / (10 * loss))
		eq.append((obs.latitude - apLat) ** 2 + (obs.longitude - apLong) ** 2 - d)
		numberOfEq = numberOfEq + 1
		if numberOfEq == 3:
			break

	initialGuess = (43.0, 27.0, 5)
	eqLen = len(eq) - 3
	for i in xrange(eqLen):
		initialGuess = initialGuess + (5,)

	sol = fsolve(trilat, initialGuess, eq)
	# xapLat = sol[0]
	# xapLong = sol[1]
	# print sol[0], sol[1]
	return sol[0], sol[1]

def generate_new_random_solution(observationList, GPSSeenAPList):

	# newObservationList = []
	for observation in observationList:
		if not observation.gps_granted:
			observation.latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			observation.longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

		# apList = []
		for ap in observation.access_points:
			ap.path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
			ap.pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)

			gpsInterestingAP = None
			# print GPSSeenAPList
			for gpsAP in GPSSeenAPList:
				# print gpsAP.name
				if ap.name == gpsAP.name and len(gpsAP.gpsObservationList) >= 3 and not gpsAP.wasSolved:
					gpsInterestingAP = gpsAP
					gpsAP.wasSolved = True
					break

			# print gpsInterestingAP
			if gpsInterestingAP == None:
				ap.latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
				ap.longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)
			else:
				ap.latitude, ap.longitude = trilaterate(gpsInterestingAP)
			# apList.append(AccessPointObservation(ap.name, ap.apPij, ap.path_loss, ap.pi0, ap.latitude, ap.longitude))
		
		# newObservationList.append(DeviceObservation(observation.timestamp, observation.latitude, 
		# 	observation.longitude, observation.gps_granted, apList))
	
	JEZ = compute_JEZ(observationList)

	return Solution(JEZ, observationList)

def signature():
	if random.randint(-1, 1) < 0:
		return -1
	return 1

conn = sqlite3.connect('samples.db')
c = conn.cursor()

c.execute("SELECT * from wifi_samples")

rows = c.fetchall()

c.execute("SELECT * from gps_samples")
gps_rows = c.fetchall()

observationList = []
GPSSeenAPList = []
for row in rows:
	apName = row[0]

	apPij = row[1]
	timestamp = row[2]

	observationExists = False
	for observation in observationList:
		if observation.timestamp == timestamp:
			observationExists = True

			path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
			pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
			latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			observation.access_points.append(AccessPointObservation(apName, apPij, path_loss, pi0, latitude, longitude))

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

				deviceObservation = DeviceObservation(gps_timestamp, latitude, longitude, True, 
					[AccessPointObservation(apName, apPij, path_loss, pi0, ap_latitude, ap_longitude)])
				currentAP = None
				for gpsAP in GPSSeenAPList:
					if gpsAP.name == apName:
						currentAP = gpsAP
				if currentAP == None:
					currentAP = AccessPointGPSFingerprint(apName)
					GPSSeenAPList.append(currentAP)

				currentAP.addObservation(deviceObservation)

				observationList.append(deviceObservation)
				
				observationExists = True
				break

		if not observationExists:
			latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			observationList.append(DeviceObservation(timestamp, latitude, longitude, False, 
				[AccessPointObservation(apName, apPij, path_loss, pi0, ap_latitude, ap_longitude)]))

keepAPList = []
for obs in observationList:
	for ap in obs.access_points:
		newAP = True
		for existingAP in keepAPList:
			if existingAP.name == ap.name:
				newAP = False
				existingAP.newFingerprint()
				break
		if newAP:
			keepAPList.append(AccessPoint(ap.name))

# print len(keepAPList)
for ap in keepAPList:
	if ap.count < 5:
		keepAPList.remove(ap)
# print len(keepAPList)
# for ap in keepAPList:
# 	print ap.name
for obs in observationList:
	for ap in obs.access_points:
		keep = False
		for keepAP in keepAPList:
			if ap.name == keepAP.name:
				keep = True
				break
		if not keep:
			obs.access_points.remove(ap)

keepAPList = []
for obs in observationList:
	for ap in obs.access_points:
		newAP = True
		for existingAP in keepAPList:
			if existingAP.name == ap.name:
				newAP = False
				existingAP.newFingerprint()
				break
		if newAP:
			keepAPList.append(AccessPoint(ap.name))

# print len(keepAPList)
JEZ = compute_JEZ(observationList)
oldSolutions = [Solution(JEZ, observationList)]
# print JEZ

# print len(GPSSeenAPList)
for i in xrange(SOLUTIONS_PER_GENERATION - 1):
	oldSolutions.append(generate_new_random_solution(observationList, GPSSeenAPList))

for sol in oldSolutions:
	print sol.JEZ

print "========"
oldSolutions = gradient_descent(oldSolutions)[:]

for sol in oldSolutions:
	print sol.JEZ

print "========"
count = 0
oldSolutionToCompare = oldSolutions[0:int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)]

while True:
	newSolutions = []
	newSolutionToCompare = []
	# print count
	for i in xrange(int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)):
		best = 1000.0
		for sol in oldSolutions:
			if sol.JEZ < best:
				best = sol.JEZ

		for sol in oldSolutions:
			if sol.JEZ == best:
				oldObservationList = sol.observationList[:]
				oldSolutions.remove(sol)
				newSolutionToCompare.append(sol)
				break

		newSolutions.append(Solution(best, oldObservationList))

	for sol in newSolutionToCompare:
		print sol

	print "\n\n"

	solLen = len(newSolutions)
	isBetter = False

	for j in xrange(solLen):
		if newSolutions[j].JEZ < oldSolutionToCompare[j].JEZ:
			isBetter = True
			break
	if not isBetter:
		count = count + 1
		print count
	else:
		count = 0
	if count == 10:
		break

	for i in xrange(int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)):
		newSolutions.append(generate_new_random_solution(observationList, GPSSeenAPList))

	combinedNewSolutions = []
	for i in xrange(int(SIXTY_PERCENT * SOLUTIONS_PER_GENERATION)):
		newS1 = random.choice(oldSolutions)
		newS2 = random.choice(oldSolutions)

		oldObservationListS1 = newS1.observationList
		oldObservationListS2 = newS2.observationList

		newObservationList = []
		obs_index = 0
		for obs in oldObservationListS1:
			a_obs_lat = random.uniform(0, 1) 
			a_obs_long = random.uniform(0, 1)

			AccessPointObservationList = []
			ap_index = 0
			for ap in obs.access_points:
				a_ap_path_loss = random.uniform(0, 1)
				a_ap_pi0 = random.uniform(0, 1)
				a_ap_lat = random.uniform(0, 1) 
				a_ap_long = random.uniform(0, 1)

				old_s2_ap = oldObservationListS2[obs_index].access_points[ap_index]
				new_path_loss = a_ap_path_loss * ap.path_loss + (1 - a_ap_path_loss) * old_s2_ap.path_loss
				new_pi0 = a_ap_pi0 * ap.Pi0 + (1 - a_ap_pi0) * old_s2_ap.Pi0
				new_latitude = a_ap_lat * ap.lat + (1 - a_ap_lat) * old_s2_ap.lat
				new_longitude = a_ap_long * ap.long + (1 - a_ap_long) * old_s2_ap.long  
				AccessPointObservationList.append(AccessPointObservation(ap.name, ap.apPij, new_path_loss, new_pi0, new_latitude, new_longitude))

				ap_index = ap_index + 1

			if obs.gps_granted:
				new_obs_lat = obs.latitude
				new_obs_long = obs.longitude
			else:
				if oldObservationListS2[obs_index].gps_granted:
					new_obs_lat = oldObservationListS2[obs_index].latitude
					new_obs_long = oldObservationListS2[obs_index].longitude
				else:
					new_obs_lat = a_obs_lat * obs.latitude + (1 - a_obs_lat) * oldObservationListS2[obs_index].latitude
					new_obs_long = a_obs_long * obs.longitude + (1 - a_obs_long) * oldObservationListS2[obs_index].longitude
			
			newObservationList.append(DeviceObservation(obs.timestamp, new_obs_lat, new_obs_long, obs.gps_granted, AccessPointObservationList))

			obs_index = obs_index + 1

		combinedNewSolutions.append(Solution(compute_JEZ(newObservationList), newObservationList))

	combinedNewSolutions = gradient_descent(combinedNewSolutions)[:]
	# print "GD"
	newSolutions = newSolutions + combinedNewSolutions
	combinedNewSolutions = []
	for i in xrange(int(TWENTY_PERCENT * SOLUTIONS_PER_GENERATION)):
		newS1 = random.choice(oldSolutions)

		oldObservationListS1 = newS1.observationList
		newObservationList = []
		for obs in oldObservationListS1:

			if obs.gps_granted:
				e_obsLat = 0
				e_obsLong = 0
			else:
				e_obsLat = numpy.random.exponential() * signature()
				e_obsLong = numpy.random.exponential() * signature()

			apList = []
			for ap in obs.access_points:
				e_ap_path_loss = numpy.random.exponential() * signature()
				e_ap_pi0 = numpy.random.exponential() * signature()
				e_ap_lat = numpy.random.exponential() * signature()
				e_ap_long = numpy.random.exponential() * signature()

				apList.append(AccessPointObservation(ap.name, ap.apPij, ap.path_loss + e_ap_path_loss, ap.Pi0 + e_ap_pi0,
					ap.lat + e_ap_lat, ap.long + e_ap_long))

			newObservationList.append(DeviceObservation(obs.timestamp, obs.latitude + e_obsLat, 
				obs.longitude + e_obsLong, obs.gps_granted, apList))

		combinedNewSolutions.append(Solution(compute_JEZ(newObservationList), newObservationList))

	combinedNewSolutions = gradient_descent(combinedNewSolutions)[:]
	# print "GD2"
	newSolutions = newSolutions + combinedNewSolutions
	
	# solLen = len(newSolutions)
	# isBetter = False
	# for j in xrange(solLen):
	# 	if newSolutions[j].JEZ < oldSolutions[j].JEZ:
	# 		isBetter = True
	# 		break

	# if not isBetter:
	# 	count = count + 1
	# else:
	# 	count = 0
	# # print count
	# if count == 10:
	# 	break
	# for sol in newSolutions:
	# 	print sol
	oldSolutions = newSolutions[:]
	oldSolutionToCompare = newSolutionToCompare[:]

for sol in newSolutions:
	print sol.JEZ
# for obs in newSolutions[0].observationList:
# 	print obs
	# for ap in obs.access_points:
	# 	print ap