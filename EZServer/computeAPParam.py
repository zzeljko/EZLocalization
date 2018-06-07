import sqlite3
import random
import math
import numpy
from grad import DeviceObservation, AccessPoint, Solution, gradient_descent, compute_JEZ

MIN_PATH_LOSS = 2
MAX_PATH_LOSS = 10

MIN_PI0 = -90
MAX_PI0 = -30

MIN_LATITTUDE = 44
MAX_LATITUDE = 45

MIN_LONGITUDE = 26
MAX_LONGITUDE = 27

SAME_PLACE_INTERVAL = 2000

SOLUTIONS_PER_GENERATION = 100

TEN_PERCENT = 10 / 100.0
SIXTY_PERCENT = 60 / 100.0
TWENTY_PERCENT = 20 / 100.0

def generate_new_random_solution(observationList):

	newObservationList = []
	for observation in observationList:
		if not observation.gps_granted:
			observation.latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			observation.longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

		apList = []
		for ap in observation.access_points:
			ap.path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
			ap.pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
			ap.latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			ap.longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			apList.append(AccessPoint(ap.name, ap.apPij, ap.path_loss, ap.pi0, ap.latitude, ap.longitude))
		
		newObservationList.append(DeviceObservation(observation.timestamp, observation.latitude, 
			observation.longitude, observation.gps_granted, apList))
	
	JEZ = compute_JEZ(newObservationList)

	return Solution(JEZ, newObservationList)

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

for row in rows:
	apName = row[0]
	apPij = row[1]
	timestamp = row[2]

	observationExists = False
	for observation in observationList:
		if abs(observation.timestamp - timestamp) < SAME_PLACE_INTERVAL:
			observationExists = True

			path_loss = random.uniform(MIN_PATH_LOSS, MAX_PATH_LOSS)
			pi0 = random.randint(MIN_PI0, MAX_PI0 + 1)
			latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			observation.access_points.append(AccessPoint(apName, apPij, path_loss, pi0, latitude, longitude))

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

				observationList.append(DeviceObservation(gps_timestamp, latitude, longitude, True, 
					[AccessPoint(apName, apPij, path_loss, pi0, ap_latitude, ap_longitude)]))
				
				observationExists = True
				break

		if not observationExists:
			latitude = random.uniform(MIN_LATITTUDE, MAX_LATITUDE) 
			longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)

			observationList.append(DeviceObservation(timestamp, latitude, longitude, False, 
				[AccessPoint(apName, apPij, path_loss, pi0, ap_latitude, ap_longitude)]))

JEZ = compute_JEZ(observationList)
oldSolutions = [Solution(JEZ, observationList)]

for i in xrange(SOLUTIONS_PER_GENERATION - 1):
	oldSolutions.append(generate_new_random_solution(observationList))

oldSolutions = gradient_descent(oldSolutions)
for sol in oldSolutions:
	print sol.JEZ

count = 0
oldSolutionToCompare = oldSolutions[1:int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)]
while True:
	newSolutions = []
	newSolutionToCompare = []
	for i in xrange(int(TEN_PERCENT * SOLUTIONS_PER_GENERATION)):
		best = min([x.JEZ for x in oldSolutions])

		for x in oldSolutions:
			if x.JEZ == best:
				oldObservationList = x.observationList[:]
				oldSolutions.remove(x)
				newSolutionToCompare.append(x)
				break

		newSolutions.append(Solution(best, oldObservationList))

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
		newSolutions.append(generate_new_random_solution(observationList))

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

			accessPointList = []
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
				accessPointList.append(AccessPoint(ap.name, ap.apPij, new_path_loss, new_pi0, new_latitude, new_longitude))

				ap_index = ap_index + 1

			new_obs_lat = a_obs_lat * obs.latitude + (1 - a_obs_lat) * oldObservationListS2[obs_index].latitude
			new_obs_long = a_obs_long * obs.longitude + (1 - a_obs_long) * oldObservationListS2[obs_index].longitude
			newObservationList.append(DeviceObservation(obs.timestamp, new_obs_lat, new_obs_long, obs.gps_granted, accessPointList))

			obs_index = obs_index + 1

		combinedNewSolutions.append(Solution(compute_JEZ(newObservationList), newObservationList))

	combinedNewSolutions = gradient_descent(combinedNewSolutions)
	newSolutions = newSolutions + combinedNewSolutions

	combinedNewSolutions = []
	for i in xrange(int(TWENTY_PERCENT * SOLUTIONS_PER_GENERATION)):
		newS1 = random.choice(oldSolutions)

		oldObservationListS1 = newS1.observationList
		newObservationList = []
		for obs in oldObservationListS1:

			e_obsLat = numpy.random.exponential() * signature()
			e_obsLong = numpy.random.exponential() * signature()

			apList = []
			for ap in obs.access_points:
				e_ap_path_loss = numpy.random.exponential() * signature()
				e_ap_pi0 = numpy.random.exponential() * signature()
				e_ap_lat = numpy.random.exponential() * signature()
				e_ap_long = numpy.random.exponential() * signature()

				apList.append(AccessPoint(ap.name, ap.apPij, ap.path_loss + e_ap_path_loss, ap.Pi0 + e_ap_pi0,
					ap.lat + e_ap_lat, ap.long + e_ap_long))

			newObservationList.append(DeviceObservation(obs.timestamp, obs.latitude + e_obsLat, 
				obs.longitude + e_obsLong, obs.gps_granted, apList))

		combinedNewSolutions.append(Solution(compute_JEZ(newObservationList), newObservationList))

	combinedNewSolutions = gradient_descent(combinedNewSolutions)
	newSolutions = newSolutions + combinedNewSolutions
	oldSolutions = newSolutions[:]
	oldSolutionToCompare = newSolutionToCompare[:]

for sol in newSolutions:
	print sol.JEZ
for obs in newSolutions[0].observationList:
	print obs