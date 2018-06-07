# multiproc_test.py

import random
from multiprocessing import Manager, Pool 

manager = Manager()
shared_list = manager.list()

def list_append(count):
	"""
	Creates an empty list and then appends a
	random number to the list 'count' number
	of times. A CPU-heavy operation!
	"""
	global shared_list
	for i in range(count):
		shared_list.append(random.random())

if __name__ == "__main__":
	size = 10000000   # Number of random numbers to add
	procs = 1   # Number of processes to create

	# # Create a list of jobs and then iterate through
	# # the number of processes appending each process to
	# # the job list
	# jobs = []

	# out_list = list()
	# for i in range(0, procs):
	# 	process = multiprocessing.Process(target=list_append,
	# 		                              args=(size / procs, i, out_list))
	# 	jobs.append(process)

	# # Start the processes (i.e. calculate the random number lists)
	# for j in jobs:
	# 	j.start()

	# # Ensure all of the processes have finished
	# for j in jobs:
	# 	j.join()

	# print len(out_list)


	pool = Pool(processes=procs)
	inputList = []
	for i in xrange(procs):
		inputList.append(size / procs)

	pool.map(list_append, inputList)
	pool.close()

	print len(shared_list)