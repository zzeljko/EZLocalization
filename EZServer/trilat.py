from scipy.optimize import fsolve
from sympy import symbols

def trilat(apCoord, d):
	unknown = apCoord
	apLat, apLong = symbols('apLat apLong', real=True)
	# print unknown[0], unknown[1]
	# print d[0]
	# print d[1]
	# print d[2]
	equations = ()
	for eq in d:
		equations = equations + (eq.subs([(apLat, unknown[0]), (apLong, unknown[1])]),)
	return equations

# x, y = symbols('apLat apLong', real=True)
# d = [0, 0, 0]
# d[0] = (1 - x) ** 2 + (4 - y) ** 2 - 49
# d[1] = (2 - x) ** 2 + (5 - y) ** 2 - 64
# d[2] = (3 - x) ** 2 + (6 - y) ** 2 - 81
# print d[0].subs([(x, 1), (y, 2)])
# apCoord = [1, 2, 3]
# unknown[0], unknown[1], cz = apCoord
# print d[0].subs([(x, unknown[0]), (y, unknown[1])])
# print d[0]
# lat, longi, z = fsolve(trilat, (5, 5, 5), d)

# print lat, longi
