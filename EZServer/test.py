from sympy import symbols, diff, log10, sqrt

xPi0, xloss, xobsLat, xobsLong, xapLat, xapLong = symbols('xPi0 xloss xobsLat xobsLong xapLat xapLong', real=True)
	
Pij = 1.3
f = abs(Pij - xPi0 + 10 * xloss * log10(sqrt((xobsLat - xapLat)**2 + (xobsLong - xapLong) ** 2)))

d1 = diff(f, xPi0)
d2 = diff(f, xloss)
d3 = diff(f, xobsLat)
d4 = diff(f, xobsLong)
d5 = diff(f, xapLat)
d6 = diff(f, xapLong)

print d1
print "=============="
print d2
print "=============="
print d3
print "=============="
print d4
print "=============="
print d5
print "=============="
print d6
print "=============="