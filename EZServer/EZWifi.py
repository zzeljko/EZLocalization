import json

class WifiAP():
	def __init__(self, json_dict):
		self.jsonDict = json_dict
		self.bssId = self.jsonDict["b"]
		self.signal = self.jsonDict["s"]
		self.channel = self.jsonDict["c"]

	def __str__(self):
		return "AP MAC: " + self.bssId + '\n' + "Signal Strength: " + self.signal + '\n' + "Channel: " + self.channel  

class WifiScan():
	def __init__(self, client, json_dict):
		self.jsonDict = json_dict
		self.client = client
		self.timestamp = json_dict["t"]

		self.wifiAPList = []
		for decodedAP in self.jsonDict["wr"]:
			ap = WifiAP(decodedAP)
			str(ap)
			self.wifiAPList.append(ap)

	def __str__(self):
		result = ''

		for ap in self.wifiAPList:
			result = result + str(ap) + '\n'

		return result