import mysql.connector
import pandas as pd
import random
import numpy as np
import math

# establishing connection to database
db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="AdCd9876*#",
	database="alfred"
)

cursor = db.cursor()

# gives the neccessary data for logisitc regression
def seperate_data():

	# gets data from mysql database
	cursor.execute("SELECT * FROM data_current")
	data = cursor.fetchall()
	data = pd.DataFrame(data)
	data = data.dropna() # removes missing values

	m = data.shape[0] # number of test
	n = data.shape[1] - 2 # number of features
	x_set = [] # x(i)
	y_set = [] # y(i)

	# iterate through each row
	for i, row in enumerate(data.values):

		x = row[2:n+1]
		x = np.array(x).tolist()
		x.insert(0, 1)
		x_set.append(x)

		y = row[n+1]
		y_set.append(y)

	x_set = np.asmatrix(x_set)
	y_set = np.asmatrix(y_set)

	cursor.execute("SELECT * FROM data_coeff")
	data = cursor.fetchall()
	data = pd.DataFrame(data)
	data = data.dropna()
	
	coeff_set = []

	for i, row in enumerate(data.values):

		coeff = row[1:n+1]
		coeff_set.append(coeff)

	coeff_set = np.asmatrix(coeff_set)

	return x_set, y_set, coeff_set, m, n

# returns value of num in the sigmoid function
def sigmoid(num):
	return (1 / (1 + math.exp(num * -1)))

# used to see if model if working properly
def cost_func(x, y, coeff, train_size):

	j = 0

	for i in range(train_size):

		actual_val = x[i].dot(coeff.transpose())
		actual_val = sigmoid(actual_val.flat[0])
		expect_val = y.flat[i]

		cost = (expect_val * math.log10(actual_val)) + ((1 - expect_val) * math.log10(1 - actual_val))
		j += cost

	j = j / (-1 * train_size)
	return j

# updates the coefficients
def update(x, y, coeff, train_size, feat_size):

	alpha = 0.001
	new_coeff = []

	for i in range(feat_size):

		val = 0

		for j in range(train_size):

			actual_val = x[j].dot(coeff.transpose())
			actual_val = sigmoid(actual_val.flat[0])
			expect_val = y.flat[j]

			cost = (actual_val - expect_val) * x[j].flat[i]
			val += cost

		val = float(coeff.flat[i]) - (alpha * val)
		new_coeff.append(val)

	new_coeff = np.asmatrix(new_coeff)
	return new_coeff

x, y, coeff, m, n = seperate_data()


for i in range(25000):
	print(cost_func(x, y, coeff, m))
	coeff = update(x, y, coeff, m, n)

# update the coefficients into database
cursor.execute("DELETE FROM data_coeff")
db.commit()
sql_temp = "INSERT INTO data_coeff (id, coeff_zero, coeff_one, coeff_two, coeff_three, coeff_four, coeff_five) VALUES (%s, %s, %s, %s, %s, %s, %s)"
row = np.array(coeff).tolist()[0]
row.insert(0, 1)
row = tuple(row)
cursor.execute(sql_temp, row)
db.commit()

print("Done Updating")
