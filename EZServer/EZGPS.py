import json

class GpsScan():
	def __init__(self, client, json_dict):
		self.jsonDict = json_dict
		self.client = client
		self.latitude = self.jsonDict["gps_record"]["lat"]
		self.longitude = self.jsonDict["gps_record"]["long"]

	def __str__(self):
		return "Latitude: " + self.latitude + "\nLongitude: " + self.longitude