import json

class GpsScan():
	def __init__(self, client, json_dict):
		self.jsonDict = json_dict
		self.client = client
		self.latitude = self.jsonDict["gr"]["la"]
		self.longitude = self.jsonDict["gr"]["lo"]
		self.timestamp = self.jsonDict["gr"]["t"]

	def __str__(self):
		return "Latitude: " + self.latitude + "\nLongitude: " + self.longitude + "\nTimestamp: " + self.timestamp