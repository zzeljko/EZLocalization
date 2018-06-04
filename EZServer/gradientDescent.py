import numpy as np

def gradient_descent_runner(points, starting_m, starting_b, learning_rate, num_iterations):
	m = starting_m
	b = starting_b
	
	for i in range(num_iterations):
		m, b = step_gradient(m, b, np.array(points), learning_rate)

	return m, b

def step_gradient(current_m, current_b, points, learning_rate):
	#gradient descent
	m_gradient = 0
	b_gradient = 0

	#Calculate optimal values for model

	#To calculate the gradient we need to calculate 
	#the partial derivative of m and b
	n = float(len(points))

	sum_m = 0
	sum_b = 0

	for point in points:
		sum_m += -1 * point[0] * (point[1] - (current_m * point[0] + current_b))
		sum_b += -1 * (point[1] - (current_m * point[0] + current_b))

	m_gradient = (2 / n) * sum_m
	b_gradient = (2 / n) * sum_b

	m_new = current_m - (learning_rate * m_gradient)
	b_new = current_b - (learning_rate * b_gradient)
	
	return m_new, b_new

def compute_error_for_given_points(m, b, points):
	#sum of squared errors
	sum_error = 0
	for i in range(len(points)):
		point = points[i]
		sum_error += (point[1] - (m * point[0] + b)) ** 2

	return sum_error / float(len(points))


def run():
	points = np.genfromtxt("data.csv", delimiter=",")

	#Hyperparameter - Tuning knobs in ML for our model

	#Learning rate is how fast our model learn
	#Too low is will be slow to converge
	#Too high it will never converge
	#Converge means finding the optimal values for our function
	learning_rate = 0.0001 

	#y = mx + b (slope formula). m = slope and b = y-intercept
	initial_b = 0
	initial_m = 0
	initial_error = compute_error_for_given_points(initial_m, initial_b, points)

	print("Starting gradient descent m=", initial_m, " and b=", initial_b, " with an error=", initial_error)

	#Depends on the size of the dataset
	num_iterations = 1000

	[m, b] = gradient_descent_runner(points, initial_m, initial_b, learning_rate, num_iterations)

	error = compute_error_for_given_points(m, b, points)

	print("After 1000 iterations m=", m, " and b=", b, " with an error=", error)


if __name__ == "__main__":
	print("Opening from Terminal")
	run()