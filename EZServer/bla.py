def test(a):
	a.append(1)
	a[0] = 2
	a = [3, 4]
# global a
a = [5, 5]
test(a)
print a